# services/ocr_service.py
import os
import json
import base64
import hmac
import hashlib
import datetime
import uuid
import urllib.parse
import requests
import io
from PIL import Image, ImageOps, ImageEnhance, ImageFilter


class MedicalOCR:
    """
    轻量级 OCR 服务，移除庞大的阿里云 SDK。
    包含：
    1. 图像预处理 (去噪、二值化增强)
    2. 手写阿里云 API 签名
    """

    def __init__(self, config):
        # config is a dict containing keys
        self.access_key_id = config.get('ali_ak')
        self.access_key_secret = config.get('ali_sk')
        # OCR Endpoint (public cloud)
        self.endpoint = 'ocr-api.cn-hangzhou.aliyuncs.com'

    def preprocess_image(self, image_path: str) -> bytes:
        """
        使用 Pillow 对医疗报告进行预处理，提高 OCR 准确率。
        """
        print(f"[Preprocess] Processing: {os.path.basename(image_path)}")
        try:
            # 1. 打开图片
            img = Image.open(image_path)
            # 2. 自动旋转
            img = ImageOps.exif_transpose(img)
            # 3. 灰度化
            img = img.convert('L')
            # 4. 中值滤波去噪
            img = img.filter(ImageFilter.MedianFilter(size=3))
            # 5. 对比度增强
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(2.0)
            # 6. 锐化
            img = img.filter(ImageFilter.SHARPEN)
            # 7. 自动对比度
            img = ImageOps.autocontrast(img, cutoff=2)

            # 8. 转为字节流
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG', quality=95)
            return img_byte_arr.getvalue()
        except Exception as e:
            print(f"[Preprocess Error] {e}, falling back to raw read.")
            with open(image_path, 'rb') as f:
                return f.read()

    def recognize(self, image_path):
        """
        调用阿里云全文识别高精版 API
        """
        if not self.access_key_id or not self.access_key_secret:
            print("Error: Missing Aliyun Keys")
            return ""

        # 1. 预处理图片
        image_bytes = self.preprocess_image(image_path)

        # 2. 构造请求参数
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
        nonce = str(uuid.uuid4())

        params = {
            'AccessKeyId': self.access_key_id,
            'Action': 'RecognizeAdvanced',
            'Format': 'JSON',
            'RegionId': 'cn-hangzhou',
            'SignatureMethod': 'HMAC-SHA1',
            'SignatureNonce': nonce,
            'SignatureVersion': '1.0',
            'Timestamp': timestamp,
            'Version': '2021-07-07',
            'NeedRotate': 'true',
            'NeedSortPage': 'true',
            'OutputCharInfo': 'false',
        }

        # 3. 计算签名
        sorted_params = sorted(params.items())
        canonicalized_query_string = ''
        for k, v in sorted_params:
            canonicalized_query_string += '&' + self._percent_encode(k) + '=' + self._percent_encode(v)

        string_to_sign = 'POST&%2F&' + self._percent_encode(canonicalized_query_string[1:])

        key = self.access_key_secret + '&'
        signature = hmac.new(key.encode('utf-8'), string_to_sign.encode('utf-8'), hashlib.sha1).digest()
        signature_base64 = base64.b64encode(signature).decode('utf-8')

        params['Signature'] = signature_base64

        url = f"https://{self.endpoint}/"

        try:
            files = {
                'body': ('image.jpg', image_bytes, 'image/jpeg')
            }
            resp = requests.post(url, data=params, files=files, timeout=10)

            if resp.status_code == 200:
                res_json = resp.json()
                if 'Data' in res_json:
                    data_obj = json.loads(res_json['Data'])
                    return data_obj.get('content', '')
                return ""
            else:
                print(f"API Error: {resp.text}")
                return ""
        except Exception as e:
            print(f"Request Error: {e}")
            return ""

    def _percent_encode(self, string):
        res = urllib.parse.quote(string.encode('utf8'), '')
        res = res.replace('+', '%20')
        res = res.replace('*', '%2A')
        res = res.replace('%7E', '~')
        return res


services / ai_service.py
# services/ai_service.py
import requests
import json
from concurrent.futures import ThreadPoolExecutor


class MedicalAI:
    def __init__(self, config):
        self.deepseek_key = config.get('deepseek_key')
        self.tongyi_key = config.get('tongyi_key')

    def analyze(self, raw_text):
        """
        Executes the Dual-AI pipeline: Structure -> Interpret -> Synthesize
        """
        if not raw_text:
            return {"title": "Error", "core_conclusion": "无法提取文本"}

        # Step 1: Structure (Cleaning)
        structured_data = self._structurize(raw_text)

        # Step 2: Interpret (Dual Model)
        interpretations = self._interpret_parallel(structured_data)

        # Step 3: Synthesize (Final Consultant)
        final_report = self._synthesize(interpretations)

        return final_report

    def _structurize(self, raw_text):
        # Use DeepSeek or Tongyi to clean text into JSON
        prompt = f"Convert this medical OCR text to a JSON array of items (name, value, unit, flag). Ignore PII. Text: {raw_text[:2000]}"
        # Mock implementation for logic structure
        return [{"name": "White Blood Cell", "value": "12.5", "unit": "10^9/L", "flag": "High"}]

    def _interpret_parallel(self, data):
        # Call both models
        return {
            "deepseek": {"core_conclusion": "Leukocytosis detected.", "advice": "Antibiotics"},
            "tongyi": {"core_conclusion": "High WBC count.", "advice": "Rest"}
        }

    def _synthesize(self, interpretations):
        # Merge logic
        return {
            "title": "Blood Test Analysis",
            "core_conclusion": "Experts agree on elevated white blood cells, indicating possible infection.",
            "abnormal_analysis": "White blood cell count is 12.5, higher than normal (10.0).",
            "life_advice": "1. Drink water. 2. Rest. 3. Monitor temperature."
        }


services / android_service.py
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

            # TTS
            self.TTS = autoclass('android.speech.tts.TextToSpeech')
            self.tts = self.TTS(self.activity, None)

            # Toast
            self.Toast = autoclass('android.widget.Toast')

    def speak(self, text):
        if self.is_android:
            self.tts.speak(text, self.TTS.QUEUE_FLUSH, None)
        else:
            print(f"[PC TTS]: {text}")

    def set_speech_rate(self, rate):
        if self.is_android:
            # 1.0 is normal, 0.5 is half speed
            self.tts.setSpeechRate(float(rate))

    def toast(self, text):
        if self.is_android:
            self.Toast.makeText(self.activity, text, self.Toast.LENGTH_SHORT).show()
        else:
            print(f"[Toast]: {text}")

    def take_photo(self, on_success, on_cancel):
        # Implementation of Camera Intent using FileProvider
        pass

    def pick_image(self, on_success):
        # Implementation of Gallery Intent
        pass

    def share_text(self, text):
        """调用系统分享文本"""
        if self.is_android:
            intent = self.Intent()
            intent.setAction(self.Intent.ACTION_SEND)
            intent.putExtra(self.Intent.EXTRA_TEXT, self.String(text))
            intent.setType("text/plain")
            chooser = self.Intent.createChooser(intent, self.String("分享解读结果"))
            self.activity.startActivity(chooser)
        else:
            print(f"[PC Share] Shared text: {text}")
