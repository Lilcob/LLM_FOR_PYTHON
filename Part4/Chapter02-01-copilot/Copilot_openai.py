import streamlit as st
import openai
import os
from dotenv import load_dotenv

# ✅ 환경변수 로드
load_dotenv()
api_key = os.getenv("openai_api_key")

# ✅ Streamlit 기본 설정
st.set_page_config(page_title="언어 번역 & 코드 수정 코파일럿", layout="wide")
st.title("🤖 코딩 코파일럿 (언어 번역 & 코드 수정)")

# ✅ 작업 선택
st.header("1. 작업 선택")
selected_function = st.selectbox(
    "🛠 수행할 작업을 선택하세요",
    ("사람 언어 번역하기", "프로그래밍 코드 수정하기")
)

# ✅ 2-1. 사람 언어 번역하기
if selected_function == "사람 언어 번역하기":
    st.header("2. 번역할 문장 입력")
    user_text = st.text_area("💬 번역할 자연어 문장을 입력하세요", height=200)

    target_language = st.selectbox(
        "🌎 번역할 언어를 선택하세요",
        ("한국어", "영어", "일본어", "중국어", "스페인어", "프랑스어", "독일어", "이탈리아어", "포르투갈어", "러시아어")
    )

# ✅ 2-2. 프로그래밍 코드 수정하기
elif selected_function == "프로그래밍 코드 수정하기":
    st.header("2. 수정할 코드 및 오류 메시지 입력")
    user_code = st.text_area("💻 수정할 코드를 입력하세요", height=300)
    error_message = st.text_area("❗ 발생한 오류 메시지를 입력하세요", height=150, help="전체 오류 로그 중 핵심 오류 메시지를 입력하면 더 정확합니다.")

# ✅ OpenAI API 기반 함수 정의

def translate_text(api_key, text, target_lang):
    client = openai.OpenAI(api_key=api_key)
    system_prompt = "너는 세계 최고의 번역가야. 항상 자연스럽고 문맥에 맞게 번역해야 해."
    user_prompt = f"다음 문장을 {target_lang}로 번역해줘:\n\n{text}"

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3,
        max_tokens=1000,
    )
    return response.choices[0].message.content

def fix_programming_code(api_key, code, error_msg=None):
    client = openai.OpenAI(api_key=api_key)
    system_prompt = "너는 뛰어난 소프트웨어 엔지니어야. 코드를 분석하고 오류를 수정하며 최적화해야 해."
    if error_msg:
        user_prompt = f"""너는 뛰어난 소프트웨어 엔지니어야. 아래 코드를 오류 메시지를 참고하여 수정하고 최적화해줘.

<수정 대상 코드>
{code}

<오류 메시지>
{error_msg}
"""
    else:
        user_prompt = f"""너는 뛰어난 소프트웨어 엔지니어야. 다음 코드를 읽고 오류를 수정하고 최적화해줘.

{code}"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2,
        max_tokens=2000,
    )
    return response.choices[0].message.content

# ✅ 실행 버튼
if st.button("🚀 작업 실행"):
    if not api_key or not api_key.strip():
        st.warning("🔑 API 키를 입력해주세요! (.env 또는 환경변수)")
    elif selected_function == "사람 언어 번역하기" and not user_text.strip():
        st.warning("💬 번역할 문장을 입력해주세요!")
    elif selected_function == "프로그래밍 코드 수정하기" and not user_code.strip():
        st.warning("💻 수정할 코드를 입력해주세요!")
    else:
        with st.spinner("OpenAI가 작업 중입니다... ⏳"):
            try:
                if selected_function == "사람 언어 번역하기":
                    output = translate_text(api_key, user_text, target_language)
                elif selected_function == "프로그래밍 코드 수정하기":
                    output = fix_programming_code(api_key, user_code, error_message)
                else:
                    output = "지원하지 않는 기능입니다."
                st.success("✅ 완료되었습니다!")
                st.text_area("📄 결과", output, height=400)
            except Exception as e:
                st.error(f"❌ 오류 발생: {e}")
