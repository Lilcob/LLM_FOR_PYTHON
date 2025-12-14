import os
from dotenv import load_dotenv

# ① 환경변수 로드 및 설정 반환
def load_config():
    load_dotenv()
    return {
        'api_key': os.getenv("OPENAI_API_KEY"),
        'models': ["gpt-4o-mini", "gpt-4", "gpt-3.5-turbo"],
        'languages': ["한국어", "영어", "일본어", "중국어", "프랑스어", "독일어", "스페인어"],
        'analysis_depths': ["기본", "중간", "심층"],
        'default_summary_length': 1500,
        'default_depth': "심층",
        'default_language': "한국어"
    }

# ② 언어 코드 매핑 반환
def get_language_codes():
    return {
        "한국어": "Korean",
        "영어": "English", 
        "일본어": "Japanese",
        "중국어": "Chinese",
        "프랑스어": "French",
        "독일어": "German",
        "스페인어": "Spanish"
    }