# services/ai_service.py
import requests
import json
from concurrent.futures import ThreadPoolExecutor

class MedicalAI:
    def __init__(self, config):
        self.deepseek_key = config.get('deepseek_key')
        self.tongyi_key = config.get('tongyi_key')

    def analyze(self, raw_text):
        if not raw_text:
            return {"title": "Error", "core_conclusion": "无法提取文本"}
        structured_data = self._structurize(raw_text)
        interpretations = self._interpret_parallel(structured_data)
        final_report = self._synthesize(interpretations)
        return final_report

    def _structurize(self, raw_text):
        return [{"name": "White Blood Cell", "value": "12.5", "unit": "10^9/L", "flag": "High"}]

    def _interpret_parallel(self, data):
        return {
            "deepseek": {"core_conclusion": "Leukocytosis detected.", "advice": "Antibiotics"},
            "tongyi": {"core_conclusion": "High WBC count.", "advice": "Rest"}
        }

    def _synthesize(self, interpretations):
        return {
            "title": "Blood Test Analysis",
            "core_conclusion": "Experts agree on elevated white blood cells, indicating possible infection.",
            "abnormal_analysis": "White blood cell count is 12.5, higher than normal (10.0).",
            "life_advice": "1. Drink water. 2. Rest. 3. Monitor temperature."
        }