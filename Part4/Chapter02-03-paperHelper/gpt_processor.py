import time
import streamlit as st
from openai import OpenAI
from config import get_language_codes

# ① 요약 프롬프트 생성
def create_summary_prompt(text, settings):
    return f"""아래 논문 내용을 바탕으로 {settings['depth']} 수준의 요약을 {settings['length']}자 이상으로 작성해주세요.

요약 구조:
1. **논문 제목 및 저자**
2. **연구 목적 및 배경**
3. **연구 방법**
4. **주요 결과**
5. **결론 및 시사점**

논문 내용:
{text}

한국어로 작성하고, 학술적 용어는 원문과 함께 병기해주세요."""

# ② 번역 프롬프트 생성
def create_translation_prompt(text, target_lang):
    lang_codes = get_language_codes()
    
    return f"""다음 학술 논문 내용을 {lang_codes[target_lang]}로 정확하고 자연스럽게 번역해주세요.

번역 지침:
- 학술적 용어와 개념을 정확히 번역
- 원문의 의미와 뉘앙스 유지
- 자연스러운 {target_lang} 표현 사용
- 전문 용어는 괄호 안에 원문 병기

원문:
{text}"""

# ③ GPT를 사용하여 텍스트 처리
def process_with_gpt(text, task_type, api_key, model, settings):
    if not api_key:
        st.error("OpenAI API 키가 설정되지 않았습니다.")
        return None
    
    client = OpenAI(api_key=api_key)
    
    if task_type == "요약":
        prompt = create_summary_prompt(text, settings)
        system_msg = "당신은 학술 논문 요약 전문가입니다. 정확하고 체계적인 요약을 작성해주세요."
        temperature = 0.5
    else:  # 번역
        prompt = create_translation_prompt(text, settings['target_language'])
        system_msg = f"당신은 전문 번역가입니다. 학술 논문을 {settings['target_language']}로 정확히 번역해주세요."
        temperature = 0.3

    try:
        with st.spinner(f'{task_type} 진행 중...'):
            start_time = time.time()
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=4000,
                top_p=0.9
            )
            duration = time.time() - start_time

        result = response.choices[0].message.content
        st.success(f"{task_type} 완료 (소요 시간: {duration:.1f}초)")
        return result
    except Exception as e:
        st.error(f"{task_type} 실패: {str(e)}")
        return None

# ④ 결과 통계 정보 표시
def display_result_statistics(combined_text, result, selected_pages):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("처리된 페이지", len(selected_pages))
    with col2:
        st.metric("원문 글자수", len(combined_text))
    with col3:
        st.metric("결과 글자수", len(result))

# # ⑤ 다운로드 버튼 생성
# def create_download_button(result, task_type, filename, selected_pages):
#     import os
    
#     base_filename = os.path.splitext(filename)[0]
#     file_extension = "md" if task_type == "요약" else "txt"
#     page_suffix = '-'.join(map(str, selected_pages[:3]))

#     if len(selected_pages) > 3:
#         page_suffix += f"-등{len(selected_pages)}p"
    
#     download_filename = f"{base_filename}_{task_type}_p{page_suffix}.{file_extension}"
#     mime_type = "text/markdown" if task_type == "요약" else "text/plain"
    
#     st.download_button(
#         label=f"📥 {task_type} 결과 다운로드",
#         data=result,
#         file_name=download_filename,
#         mime=mime_type,
#         use_container_width=True
#     )