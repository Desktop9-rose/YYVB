# Main Python file for Kivy App
import os
import threading
import sqlite3
import json
from datetime import datetime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock, mainthread
from kivy.properties import StringProperty, NumericProperty, BooleanProperty
from kivy.uix.button import Button
from kivy.animation import Animation
from cryptography.fernet import Fernet

# Service Imports
from services.android_service import AndroidService
from services.ocr_service import MedicalOCR
from services.ai_service import MedicalAI

# Load UI
Builder.load_string('''
#:import hex kivy.utils.get_color_from_hex

<CommonButton>:
    background_normal: ''
    background_color: (0,0,0,0)
    canvas.before:
        Color:
            rgba: self.bg_color if self.state == 'normal' else [x*0.8 for x in self.bg_color]
            a: self.opacity_val
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [20,]
    BoxLayout:
        pos: root.pos
        size: root.size
        orientation: 'horizontal'
        padding: 20
        spacing: 20
        Image:
            source: root.icon_source
            size_hint: None, None
            size: 60, 60
            pos_hint: {'center_y': 0.5}
        Label:
            text: root.text
            font_size: '28sp'
            font_name: 'fonts/simsun.ttc'
            bold: True
            color: (1,1,1,1)
            text_size: self.size
            halign: 'left'
            valign: 'middle'

<HomeScreen>:
    canvas.before:
        Color:
            rgba: hex('#F5F5F5')
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        orientation: 'vertical'
        padding: 40
        spacing: 30

        Label:
            text: '医疗报告助手'
            font_name: 'fonts/simsun.ttc'
            font_size: '40sp'
            color: hex('#212121')
            bold: True
            size_hint_y: 0.2

        CommonButton:
            text: '拍照解读'
            icon_source: 'assets/camera.png'
            bg_color: hex('#2E7D32')
            on_release: app.on_camera_click()

        CommonButton:
            text: '相册选择'
            icon_source: 'assets/gallery.png'
            bg_color: hex('#1565C0')
            on_release: app.pick_image()

        CommonButton:
            text: '历史记录'
            icon_source: 'assets/history.png'
            bg_color: hex('#424242')
            on_release: app.root.current = 'history'

        BoxLayout:
            size_hint_y: 0.1
            Button:
                text: '设置'
                font_name: 'fonts/simsun.ttc'
                font_size: '20sp'
                color: hex('#757575')
                background_normal: ''
                background_color: (0,0,0,0)
                on_release: app.root.current = 'settings'

<CameraGuideScreen>:
    canvas.before:
        Color:
            rgba: (0, 0, 0, 0.9)
        Rectangle:
            pos: self.pos
            size: self.size
    FloatLayout:
        # Guide Box
        Widget:
            size_hint: 0.85, 0.55
            pos_hint: {'center_x': 0.5, 'center_y': 0.55}
            canvas:
                Color:
                    rgba: (1, 1, 1, 1)
                Line:
                    width: 2
                    rectangle: (self.x, self.y, self.width, self.height)
                # Corners (Green)
                Color:
                    rgba: (0, 1, 0, 1)
                Line:
                    width: 4
                    points: [self.x, self.y + 30, self.x, self.y, self.x + 30, self.y]
                Line:
                    width: 4
                    points: [self.right - 30, self.y, self.right, self.y, self.right, self.y + 30]
                Line:
                    width: 4
                    points: [self.x, self.top - 30, self.x, self.top, self.x + 30, self.top]
                Line:
                    width: 4
                    points: [self.right - 30, self.top, self.right, self.top, self.right, self.top - 30]

        Label:
            text: '请将报告文字对齐框内\n保持光线充足 · 避免反光'
            font_name: 'fonts/simsun.ttc'
            font_size: '28sp'
            halign: 'center'
            pos_hint: {'center_x': 0.5, 'y': 0.15}
            size_hint_y: None
            height: 100

<HistoryScreen>:
    BoxLayout:
        orientation: 'vertical'
        canvas.before:
            Color:
                rgba: hex('#F5F5F5')
            Rectangle:
                pos: self.pos
                size: self.size

        # Header
        BoxLayout:
            size_hint_y: None
            height: '60dp'
            padding: 10
            canvas.before:
                Color:
                    rgba: hex('#FFFFFF')
                Rectangle:
                    pos: self.pos
                    size: self.size
            Label:
                text: '历史记录 (长按分享)'
                font_name: 'fonts/simsun.ttc'
                font_size: '24sp'
                bold: True
                color: hex('#212121')
                size_hint_x: 0.8
                halign: 'left'
                text_size: self.size
            Button:
                text: '返回'
                font_name: 'fonts/simsun.ttc'
                size_hint_x: 0.2
                background_normal: ''
                background_color: hex('#757575')
                on_release: app.root.current = 'home'

        ScrollView:
            GridLayout:
                id: history_list
                cols: 1
                spacing: 10
                padding: 10
                size_hint_y: None
                height: self.minimum_height

<LongPressButton>:
    background_normal: ''
    background_color: (1,1,1,1)
    color: (0.2, 0.2, 0.2, 1)
    size_hint_y: None
    height: '100dp'
    markup: True
    halign: 'left'
    padding: (20, 10)
    font_name: 'fonts/simsun.ttc'
    canvas.after:
        Color:
            rgba: (0,0,0, 0.1)
        Line:
            points: [self.x, self.y, self.right, self.y]
            width: 1

<SettingsScreen>:
    BoxLayout:
        orientation: 'vertical'
        canvas.before:
            Color:
                rgba: hex('#F5F5F5')
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: '设置'
            font_name: 'fonts/simsun.ttc'
            font_size: '30sp'
            bold: True
            color: hex('#000000')
            size_hint_y: None
            height: '80dp'

        ScrollView:
            BoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                padding: 20
                spacing: 20

                # Speech Rate
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: '120dp'
                    canvas.before:
                        Color:
                            rgba: hex('#FFFFFF')
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [10,]
                    Label:
                        text: '语音语速'
                        font_name: 'fonts/simsun.ttc'
                        color: hex('#000000')
                        size_hint_y: 0.4
                    GridLayout:
                        cols: 3
                        padding: 10
                        spacing: 10
                        size_hint_y: 0.6
                        SpeedButton:
                            text: '极慢'
                            group: 'speed'
                            on_release: root.update_speed(0.5)
                        SpeedButton:
                            text: '慢速'
                            group: 'speed'
                            on_release: root.update_speed(0.8)
                        SpeedButton:
                            text: '中速'
                            group: 'speed'
                            on_release: root.update_speed(1.0)

                # API Keys
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: '350dp'
                    canvas.before:
                        Color:
                            rgba: hex('#FFFFFF')
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [10,]
                    Label:
                        text: 'API 密钥配置 (加密存储)'
                        font_name: 'fonts/simsun.ttc'
                        color: hex('#1565C0')
                        bold: True
                        size_hint_y: None
                        height: '40dp'

                    TextInput:
                        id: input_ali_ak
                        hint_text: '阿里云 AccessKey ID'
                        password: True
                        multiline: False
                        size_hint_y: None
                        height: '50dp'
                    TextInput:
                        id: input_ali_sk
                        hint_text: '阿里云 AccessKey Secret'
                        password: True
                        multiline: False
                        size_hint_y: None
                        height: '50dp'
                    TextInput:
                        id: input_deepseek
                        hint_text: 'DeepSeek API Key'
                        password: True
                        multiline: False
                        size_hint_y: None
                        height: '50dp'
                    TextInput:
                        id: input_tongyi
                        hint_text: '通义千问 API Key'
                        password: True
                        multiline: False
                        size_hint_y: None
                        height: '50dp'

                    Button:
                        text: '保存配置'
                        font_name: 'fonts/simsun.ttc'
                        background_color: hex('#1565C0')
                        size_hint_y: None
                        height: '60dp'
                        on_release: root.save_keys()

                # Data Management
                BoxLayout:
                    orientation: 'vertical'
                    size_hint_y: None
                    height: '160dp'
                    canvas.before:
                        Color:
                            rgba: hex('#FFFFFF')
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [10,]
                    Label:
                        text: '数据管理'
                        font_name: 'fonts/simsun.ttc'
                        color: hex('#D32F2F')
                        bold: True
                        size_hint_y: 0.3

                    Button:
                        text: '清理30天前记录'
                        font_name: 'fonts/simsun.ttc'
                        background_color: hex('#FF9800')
                        size_hint_y: 0.35
                        on_release: root.clear_history(old_only=True)

                    Button:
                        text: '清空所有记录'
                        font_name: 'fonts/simsun.ttc'
                        background_color: hex('#D32F2F')
                        size_hint_y: 0.35
                        on_release: root.clear_history(old_only=False)

        Button:
            text: '返回首页'
            font_name: 'fonts/simsun.ttc'
            size_hint_y: None
            height: '60dp'
            background_color: hex('#757575')
            on_release: app.root.current = 'home'

<SpeedButton@ToggleButton>:
    font_name: 'fonts/simsun.ttc'
    background_normal: ''
    background_down: ''
    background_color: hex('#E0E0E0') if self.state == 'normal' else hex('#2E7D32')
    color: hex('#000000') if self.state == 'normal' else hex('#FFFFFF')
''')


class SecretManager:
    def __init__(self):
        self.key_file = 'secret.key'
        self.db_path = 'secrets.db'
        self._init_key()
        self._init_db()
        self.cipher = Fernet(self._load_key())

    def _init_key(self):
        if not os.path.exists(self.key_file):
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as key_file:
                key_file.write(key)

    def _load_key(self):
        with open(self.key_file, 'rb') as key_file:
            return key_file.read()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS secrets
                     (key_name TEXT PRIMARY KEY, key_value TEXT)''')
        conn.commit()
        conn.close()

    def save_secret(self, key_name, value):
        if not value: return
        encrypted = self.cipher.encrypt(value.encode()).decode()
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO secrets VALUES (?, ?)", (key_name, encrypted))
        conn.commit()
        conn.close()

    def get_secret(self, key_name):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT key_value FROM secrets WHERE key_name=?", (key_name,))
        result = c.fetchone()
        conn.close()
        if result:
            try:
                return self.cipher.decrypt(result[0].encode()).decode()
            except:
                return None
        return None


class DatabaseManager:
    def __init__(self):
        self.db_name = 'medical_history.db'
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date_str TEXT,
                title TEXT,
                full_json TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def add_record(self, title, data_dict):
        date_str = datetime.now().strftime('%Y-%m-%d %H:%M')
        json_str = json.dumps(data_dict, ensure_ascii=False)
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO history (date_str, title, full_json) VALUES (?, ?, ?)',
                       (date_str, title, json_str))
        conn.commit()
        conn.close()

    def get_all_records(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT id, date_str, title, full_json FROM history ORDER BY id DESC')
        rows = cursor.fetchall()
        conn.close()
        return rows

    def get_record(self, record_id):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT full_json FROM history WHERE id=?', (record_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return json.loads(row[0])
        return None

    def delete_old_records(self, days=30):
        # Implementation for deleting records older than X days
        pass

    def delete_all_records(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM history')
        conn.commit()
        conn.close()


class CommonButton(Button):
    bg_color = ListProperty([0, 0, 0, 1])
    icon_source = StringProperty('')
    opacity_val = NumericProperty(1)

    def on_state(self, instance, value):
        if value == 'down':
            anim = Animation(opacity_val=0.8, duration=0.1)
        else:
            anim = Animation(opacity_val=1, duration=0.1)
        anim.start(self)


class LongPressButton(Button):
    """
    支持长按事件的按钮
    """

    def __init__(self, record_id, **kwargs):
        super().__init__(**kwargs)
        self.record_id = record_id
        self._long_press_event = None
        self._is_long_press = False

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self._is_long_press = False
            # 0.8秒后触发长按
            self._long_press_event = Clock.schedule_once(self.do_long_press, 0.8)
            return super().on_touch_down(touch)
        return False

    def on_touch_up(self, touch):
        if self._long_press_event:
            self._long_press_event.cancel()
        if self._is_long_press:
            # 如果触发了长按，这里不再触发点击(on_release)
            return True
        return super().on_touch_up(touch)

    def do_long_press(self, dt):
        self._is_long_press = True
        App.get_running_app().share_history_item(self.record_id)


class CameraGuideScreen(Screen):
    pass


class HistoryScreen(Screen):
    def on_enter(self):
        self.ids.history_list.clear_widgets()
        db = App.get_running_app().db
        records = db.get_all_records()
        if not records:
            lbl = Button(text="暂无历史记录", background_color=(0, 0, 0, 0), color=(0.5, 0.5, 0.5, 1),
                         font_name='fonts/simsun.ttc')
            self.ids.history_list.add_widget(lbl)
            return

        for r in records:
            # r: (id, date, title, json)
            btn_text = f"[size=20sp][color=#9E9E9E]{r[1]}[/color][/size]\n[size=28sp][b]{r[2]}[/b][/size]"
            # 使用 LongPressButton
            item = LongPressButton(record_id=r[0], text=btn_text)
            # 点击事件 (短按)
            item.bind(on_release=lambda x, rid=r[0]: App.get_running_app().show_history_detail(rid))
            self.ids.history_list.add_widget(item)


class SettingsScreen(Screen):
    def update_speed(self, rate):
        app = App.get_running_app()
        app.android.set_speech_rate(rate)
        app.android.speak("当前语速试听：一二三四五")
        # Save preference
        app.secrets.save_secret('speech_rate', str(rate))

    def save_keys(self):
        app = App.get_running_app()
        s = app.secrets
        s.save_secret('ali_ak', self.ids.input_ali_ak.text)
        s.save_secret('ali_sk', self.ids.input_ali_sk.text)
        s.save_secret('deepseek_key', self.ids.input_deepseek.text)
        s.save_secret('tongyi_key', self.ids.input_tongyi.text)
        app.android.toast("密钥已保存")
        # Reload services with new keys
        app.init_services()

    def clear_history(self, old_only=False):
        app = App.get_running_app()
        if old_only:
            app.db.delete_old_records(30)
            app.android.toast("已清理30天前记录")
        else:
            app.db.delete_all_records()
            app.android.toast("历史记录已清空")


class HomeScreen(Screen):
    pass


class MedicalApp(App):
    def build(self):
        self.title = 'Medical Helper'
        self.android = AndroidService()
        self.db = DatabaseManager()
        self.secrets = SecretManager()
        self.init_services()

        # Load saved settings
        saved_rate = self.secrets.get_secret('speech_rate')
        if saved_rate:
            self.android.set_speech_rate(float(saved_rate))

        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(CameraGuideScreen(name='guide'))
        sm.add_widget(HistoryScreen(name='history'))
        sm.add_widget(SettingsScreen(name='settings'))
        # ResultScreen would be dynamically added or separate
        return sm

    def init_services(self):
        # Load keys from DB
        keys = {
            'ali_ak': self.secrets.get_secret('ali_ak'),
            'ali_sk': self.secrets.get_secret('ali_sk'),
            'deepseek_key': self.secrets.get_secret('deepseek_key'),
            'tongyi_key': self.secrets.get_secret('tongyi_key')
        }
        self.ocr = MedicalOCR(keys)
        self.ai = MedicalAI(keys)

    def on_camera_click(self):
        # 1. Jump to Guide Screen
        self.root.current = 'guide'
        self.android.speak("请将报告单对齐白色边框，保持光线充足")
        # 2. Delayed launch of real camera
        Clock.schedule_once(self.launch_camera_delay, 2.5)

    def launch_camera_delay(self, dt):
        self.android.take_photo(self.on_photo_success, self.on_photo_cancel)
        # Note: on_photo_success callback will switch screen to loading

    def pick_image(self):
        self.android.pick_image(self.on_photo_success)

    @mainthread
    def on_photo_success(self, image_path):
        # Logic to process report...
        threading.Thread(target=self.process_report, args=(image_path,)).start()

    def on_photo_cancel(self):
        self.root.current = 'home'

    def process_report(self, image_path):
        # 1. OCR
        text = self.ocr.recognize(image_path)
        # 2. AI
        result = self.ai.analyze(text)
        # 3. Save
        self.db.add_record(result.get('title', '未命名报告'), result)
        pass

    def share_history_item(self, record_id):
        # Get record text
        record = self.db.get_record(record_id)
        if record:
            # Construct share text (desensitized)
            share_content = f"【检查报告解读】\n核心结论：{record.get('core_conclusion', '')}\n异常指标：{record.get('abnormal_analysis', '')}\n生活建议：{record.get('life_advice', '')}"
            self.android.share_text(share_content)


if __name__ == '__main__':
    MedicalApp().run()