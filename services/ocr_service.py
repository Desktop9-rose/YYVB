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
    def __init__(self, config):
        self.access_key_id = config.get('ali_ak')
        self.access_key_secret = config.get('ali_sk')
        self.endpoint = 'ocr-api.cn-hangzhou.aliyuncs.com'

    def preprocess_image(self, image_path: str) -> bytes:
        try:
            img = Image.open(image_path)
            img = ImageOps.exif_transpose(img)
            img = img.convert('L')
            img = img.filter(ImageFilter.MedianFilter(size=3))
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(2.0)
            img = img.filter(ImageFilter.SHARPEN)
            img = ImageOps.autocontrast(img, cutoff=2)
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG', quality=95)
            return img_byte_arr.getvalue()
        except Exception as e:
            with open(image_path, 'rb') as f:
                return f.read()

    def recognize(self, image_path):
        if not self.access_key_id or not self.access_key_secret:
            return ""
        image_bytes = self.preprocess_image(image_path)
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
                return ""
        except Exception as e:
            return ""

    def _percent_encode(self, string):
        res = urllib.parse.quote(string.encode('utf8'), '')
        res = res.replace('+', '%20')
        res = res.replace('*', '%2A')
        res = res.replace('%7E', '~')
        return res