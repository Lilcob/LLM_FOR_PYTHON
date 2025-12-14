import streamlit as st
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np

st.title("이미지 필터링 데모")

# 예시 이미지 미리보기
st.header("Example Preview")
try:
    example = Image.open("images/example.png")
    st.subheader("Original Example")
    st.image(example, use_container_width=True)
    st.markdown("---")
    st.subheader("Filter Previews")
    filter_names = ["Grayscale", "Color Intensity", "Blur", "RGB Adjust"]
    cols = st.columns(len(filter_names))
    for col, name in zip(cols, filter_names):
        with col:
            if name == "Grayscale":
                img_preview = example.convert("L").convert("RGB")
            elif name == "Color Intensity":
                enhancer = ImageEnhance.Color(example)
                img_preview = enhancer.enhance(1.5)
            elif name == "Blur":
                img_preview = example.filter(ImageFilter.GaussianBlur(2.0))
            elif name == "RGB Adjust":
                arr = np.array(example).astype(float)
                arr[..., 0] *= 1.2
                arr[..., 1] *= 1.0
                arr[..., 2] *= 1.2
                arr = np.clip(arr, 0, 255).astype('uint8')
                img_preview = Image.fromarray(arr)
            col.image(img_preview, caption=name, use_container_width=True)
except FileNotFoundError:
    st.warning("example.png 파일을 images 디렉토리에 두고 실행하세요.")

st.markdown("---")

# 1) 이미지 업로드
uploaded = st.file_uploader("이미지를 업로드하세요", type=["png", "jpg", "jpeg"])
if uploaded is None:
    st.stop()

img = Image.open(uploaded)
st.subheader("원본 이미지")
st.image(img, use_container_width=True)

st.markdown("---")

# 2) 필터 선택
filter_type = st.radio("필터 선택", ["None", "Grayscale", "Color Intensity 조정", "Blur", "RGB 조정"])

# Grayscale
if filter_type == "Grayscale":
    gray = img.convert("L").convert("RGB")
    st.subheader("그레이스케일 변환")
    st.image(gray, use_container_width=True)

# Color Intensity
elif filter_type == "Color Intensity 조정":
    factor = st.slider("채도 조정 (0: 흑백 → 1: 원본 → 2: 과포화)", 0.0, 2.0, 1.0, 0.01)
    enhancer = ImageEnhance.Color(img)
    enhanced = enhancer.enhance(factor)
    st.subheader(f"채도 조정 결과 (factor={factor:.2f})")
    st.image(enhanced, use_container_width=True)

# Blur
elif filter_type == "Blur":
    radius = st.slider("블러 강도 (radius)", 0.0, 10.0, 0.0, 0.1)
    blurred = img.filter(ImageFilter.GaussianBlur(radius))
    st.subheader(f"블러 적용 결과 (radius={radius:.1f})")
    st.image(blurred, use_container_width=True)

# RGB 조정
elif filter_type == "RGB 조정":
    st.subheader("RGB 채널 조정")
    r_factor = st.slider("R 채널 조정", 0.0, 2.0, 1.0, 0.01)
    g_factor = st.slider("G 채널 조정", 0.0, 2.0, 1.0, 0.01)
    b_factor = st.slider("B 채널 조정", 0.0, 2.0, 1.0, 0.01)
    arr = np.array(img).astype(float)
    arr[..., 0] *= r_factor
    arr[..., 1] *= g_factor
    arr[..., 2] *= b_factor
    arr = np.clip(arr, 0, 255).astype('uint8')
    rgb_img = Image.fromarray(arr)
    st.image(rgb_img, use_container_width=True)

# None
else:
    st.info("필터를 선택하면 결과가 여기에 표시됩니다.")