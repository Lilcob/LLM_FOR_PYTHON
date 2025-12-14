import streamlit as st
from config import load_config
from ui_components import (
    setup_page_config, display_header, create_sidebar, 
    select_task_type, select_pages,
    validate_inputs
)
from pdf_preprocessor import (
    extract_text_by_pages, combine_pages_text, 
    display_file_info
)
from gpt_processor import (
    process_with_gpt, display_result_statistics
)

# ① UI 요소 설정
setup_page_config()
display_header()

# 설정 로드
config = load_config()

# 사이드바 설정
sidebar_settings = create_sidebar()

# 파일 업로드
uploaded_file = st.file_uploader("📄 PDF 논문 파일 업로드", type="pdf")

# ② PDF 파일 처리
if uploaded_file:
    # 파일 정보 표시
    col1, col2 = st.columns([1, 3])
    with col1:
        display_file_info(uploaded_file)
    
    # PDF 텍스트 추출 (세션 상태 관리)
    if 'pages_text' not in st.session_state or st.session_state.get('current_file') != uploaded_file.name:
        with st.spinner("PDF 텍스트 추출 중..."):
            pages_text, total_pages = extract_text_by_pages(uploaded_file)
            if pages_text:
                st.session_state.pages_text = pages_text
                st.session_state.total_pages = total_pages
                st.session_state.current_file = uploaded_file.name
                st.success(f"✅ PDF 추출 완료 (총 {total_pages}페이지)")
            else:
                st.error("PDF 텍스트 추출에 실패했습니다.")
                st.stop() 
    
    # ③ 작업 수행
    if 'pages_text' in st.session_state:
        pages_text = st.session_state.pages_text
        total_pages = st.session_state.total_pages
        
        # 작업 선택
        task_type = select_task_type()
        
        # 페이지 선택
        selected_pages = select_pages(total_pages)
        
        # 작업 실행 버튼
        if st.button(f"🚀 {task_type} 시작", type="primary", use_container_width=True):
            if validate_inputs(config['api_key'], selected_pages):
                # 텍스트 결합
                combined_text = combine_pages_text(pages_text, selected_pages)
                
                # GPT 설정 준비
                gpt_settings = {
                    'length': sidebar_settings['summary_length'],
                    'depth': sidebar_settings['analysis_depth'],
                    'target_language': sidebar_settings['target_language']
                }
                
                # GPT 처리
                result = process_with_gpt(
                    combined_text, 
                    task_type, 
                    config['api_key'], 
                    sidebar_settings['model_choice'], 
                    gpt_settings
                )
                
                # ④ 작업 결과 처리
                if result:
                    # 결과 표시
                    st.markdown(f"## 📝 {task_type} 결과")
                    st.markdown(result)
                    
                    # 통계 정보
                    display_result_statistics(combined_text, result, selected_pages)