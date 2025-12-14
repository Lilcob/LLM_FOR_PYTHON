import os
import tempfile
import time
import streamlit as st
import pdfplumber

# ①  PDF에서 페이지별로 텍스트 추출
def extract_text_by_pages(pdf_file):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(pdf_file.getvalue())
            temp_file_path = temp_file.name

        pages_text = {}
        with pdfplumber.open(temp_file_path) as pdf:
            total_pages = len(pdf.pages)
            progress_bar = st.progress(0, text="PDF 처리 중...")
            
            for page_num, page in enumerate(pdf.pages, 1):
                page_text = page.extract_text()
                if page_text:
                    pages_text[page_num] = page_text.strip()
                progress_bar.progress(page_num / total_pages, text=f"페이지 {page_num}/{total_pages} 처리 중...")
                time.sleep(0.01)

        progress_bar.empty()
        os.unlink(temp_file_path)
        return pages_text, total_pages
    except Exception as e:
        st.error(f"PDF 처리 오류: {str(e)}")
        return None, 0

# ② 페이지 번호 입력을 파싱하여 유효한 페이지 리스트 반환
def parse_page_numbers(page_input, total_pages):
    try:
        pages = set()
        parts = page_input.replace(" ", "").split(",")
        
        for part in parts:
            if "-" in part:
                start, end = map(int, part.split("-"))
                pages.update(range(start, end + 1))
            else:
                pages.add(int(part))
        
        # 유효한 페이지만 필터링
        valid_pages = [p for p in pages if 1 <= p <= total_pages]
        return sorted(valid_pages)
    except:
        return []

# ③ 선택된 페이지들의 텍스트를 결합
def combine_pages_text(pages_text, selected_pages): #, include_page_ref=True):
    combined_text = ""
    for page_num in selected_pages:
        # if include_page_ref:
        #     combined_text += f"\n[페이지 {page_num}]\n"
        combined_text += pages_text.get(page_num, "") + "\n"
    return combined_text

# ④ 업로드된 파일 정보 표시
def display_file_info(uploaded_file):
    st.subheader("📁 파일 정보")
    st.write(f"**이름:** {uploaded_file.name}")
    st.write(f"**크기:** {uploaded_file.size/1024:.1f} KB")

# def display_page_preview(pages_text, selected_pages, max_preview_pages=3):
#     """선택된 페이지들의 미리보기 표시"""
#     with st.expander("📋 선택된 페이지 미리보기", expanded=False):
#         preview_text = ""
#         preview_pages = selected_pages[:max_preview_pages]
        
#         for page_num in preview_pages:
#             preview_text += f"\n--- 페이지 {page_num} ---\n"
#             page_content = pages_text.get(page_num, "")
#             preview_text += page_content[:500]
#             if len(page_content) > 500:
#                 preview_text += "..."
#             preview_text += "\n"
        
#         if len(selected_pages) > max_preview_pages:
#             preview_text += f"\n... 그 외 {len(selected_pages) - max_preview_pages}개 페이지"
        
#         st.text_area("미리보기", preview_text, height=300, label_visibility='collapsed')