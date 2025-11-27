# services/android_service.py
from jnius import autoclass, cast
from kivy.core.window import Window
from kivy.utils import platform

class AndroidService:
    def __init__(self):
        self.is_android = platform == 'android'
        if self.is_android:
            self.PythonActivity = autoclass('org.kivy.android.PythonActivity')
            self.activity = self.PythonActivity.mActivity
            self.Intent = autoclass('android.content.Intent')
            self.String = autoclass('java.lang.String')
            self.TTS = autoclass('android.speech.tts.TextToSpeech')
            self.tts = self.TTS(self.activity, None)
            self.Toast = autoclass('android.widget.Toast')

    def speak(self, text):
        if self.is_android:
            self.tts.speak(text, self.TTS.QUEUE_FLUSH, None)
        else:
            print(f"[PC TTS]: {text}")

    def set_speech_rate(self, rate):
        if self.is_android:
            self.tts.setSpeechRate(float(rate))

    def toast(self, text):
        if self.is_android:
            self.Toast.makeText(self.activity, text, self.Toast.LENGTH_SHORT).show()
        else:
            print(f"[Toast]: {text}")

    def take_photo(self, on_success, on_cancel):
        pass

    def pick_image(self, on_success):
        pass

    def share_text(self, text):
        if self.is_android:
            intent = self.Intent()
            intent.setAction(self.Intent.ACTION_SEND)
            intent.putExtra(self.Intent.EXTRA_TEXT, self.String(text))
            intent.setType("text/plain")
            chooser = self.Intent.createChooser(intent, self.String("分享解读结果"))
            self.activity.startActivity(chooser)
        else:
            print(f"[PC Share] Shared text: {text}")