import streamlit as st
from config import load_config

# ① 페이지 기본 설정
def setup_page_config():
    """"""
    st.set_page_config(
        page_title="논문 분석 & 번역 서비스",
        page_icon="📚",
        layout="wide"
    )

# ② 헤더 표시
def display_header():
    st.title("📚 논문 분석 & 번역 서비스")
    st.markdown("""
    PDF 논문을 업로드하여 **요약** 또는 **번역** 작업을 수행할 수 있습니다. 
    전체 페이지 또는 원하는 페이지를 선택하여 작업할 수 있습니다.
    """)
    st.markdown("---")

# ③ 사이드바 생성 및 설정값 반환
def create_sidebar():
    config = load_config()
    
    with st.sidebar:
        st.header("🔧 기본 설정")
        
        model_choice = st.selectbox(
            "GPT 모델 선택",
            config['models'],
            index=0
        )
        
        st.markdown("---")
        st.markdown("### 📊 분석 설정")
        
        summary_length = st.slider(
            "요약 길이 (문자)", 
            500, 3000, 
            config['default_summary_length']
        )
        
        analysis_depth = st.select_slider(
            "분석 깊이", 
            config['analysis_depths'], 
            value=config['default_depth']
        )
        
        st.markdown("---")
        st.markdown("### 🌐 번역 설정")
        
        target_language = st.selectbox(
            "번역 대상 언어",
            config['languages'],
            index=0
        )
    
    return {
        'model_choice': model_choice,
        'summary_length': summary_length,
        'analysis_depth': analysis_depth,
        'target_language': target_language
    }

# ④ 요약 또는 번역 작업 유형 선택
def select_task_type():
    st.subheader("🎯 작업 선택")
    task_type = st.radio(
        "수행할 작업을 선택하세요:",
        ["요약", "번역"],
        horizontal=True
    )
    return task_type

# ⑤ pdf 페이지 선택 UI
def select_pages(total_pages):
    st.subheader("📖 페이지 선택")
    
    page_option = st.radio(
        "처리할 페이지를 선택하세요:",
        ["전체 페이지", "특정 페이지"],
        horizontal=True
    )
    
    selected_pages = []
    
    if page_option == "전체 페이지":
        selected_pages = list(range(1, total_pages + 1))
        st.info(f"전체 {total_pages}페이지가 선택되었습니다.")
    else:
        page_input = st.text_input(
            "페이지 번호 입력",
            placeholder="예: 1,3,5-8,10",
            help="쉼표로 구분하여 입력하세요. 범위는 하이픈(-)으로 표시"
        )
        
        if page_input:
            from pdf_preprocessor import parse_page_numbers
            selected_pages = parse_page_numbers(page_input, total_pages)
            if selected_pages:
                st.success(f"선택된 페이지: {', '.join(map(str, selected_pages))}")
            else:
                st.error("유효하지 않은 페이지 번호입니다.")
    
    return selected_pages

# ⑥ api key , page 입력 검증
def validate_inputs(api_key, selected_pages):
    if not api_key:
        st.error("❌ OpenAI API 키를 설정해주세요!")
        return False
    elif not selected_pages:
        st.error("❌ 처리할 페이지를 선택해주세요!")
        return False
    return True