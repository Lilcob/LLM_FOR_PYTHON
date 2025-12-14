import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("BMI 계산기")

# 사이드바에 계산식과 기준표 출력 - ①

# BMI 계산식 표시
st.sidebar.header("BMI 계산식") # 좌측 사이드바에 헤더 추가
st.sidebar.write("BMI = 체중(kg) / (신장(m) ^ 2)")  # 텍스트 출력

# BMI 기준 표
st.sidebar.header("BMI 기준 표")    #
bmi_table = pd.DataFrame({  # pandas Dataframe을 활용하여 테이블 구조화
    "BMI 범위": ["18.5 미만", "18.5이상 24.9미만", "25이상 29.9미만", "30이상"],    
    "분류": ["저체중", "정상", "과체중", "비만"]    
})  
st.sidebar.table(bmi_table) 

# 1) 개별 BMI 계산 - ②  
st.header("개별 BMI 계산")
unit = st.radio("단위 선택", ["Metric (cm, kg)", "Imperial (inch, lb)"])    # 라디오 버튼을 통한 단위 선택

if unit == "Metric (cm, kg)":
    height_input = st.number_input("키 (cm)", min_value=0.0, step=0.1)
    weight_input = st.number_input("몸무게 (kg)", min_value=0.0, step=0.1)
    height_m = height_input / 100
    weight_kg = weight_input
else:
    height_input = st.number_input("키 (inch)", min_value=0.0, step=0.1)
    weight_input = st.number_input("몸무게 (lb)", min_value=0.0, step=0.1)
    height_m = height_input * 0.0254
    weight_kg = weight_input * 0.453592

# 단위 변환 값 계산 - ③
height_cm = height_input if unit.startswith("Metric") else height_m * 100
height_inch = height_input if unit.startswith("Imperial") else height_cm / 2.54
weight_lb = weight_input if unit.startswith("Imperial") else weight_kg / 0.453592

if st.button("계산하기"):   # 버튼 생성 및 클릭 시 동작 설계
    if height_m > 0:
        bmi = weight_kg / (height_m ** 2)
        if bmi < 18.5:
            category = "저체중"
        elif bmi < 25:
            category = "정상"
        elif bmi < 30:
            category = "과체중"
        else:
            category = "비만"

        st.write(f"키: {height_cm:.1f} cm / {height_inch:.2f} in")
        st.write(f"몸무게: {weight_kg:.1f} kg / {weight_lb:.2f} lb")
        st.success(f"당신의 BMI는 {bmi:.2f}이며, 분류는 **{category}** 입니다.")
    else:
        st.error("키를 올바르게 입력해주세요.")

st.markdown("---")

# 2) CSV 파일 단위 처리 - ④
st.header("CSV 파일 BMI 계산기")
uploaded_file = st.file_uploader("CSV 파일 업로드", type=["csv"])   # 업로드 창 생성
st.caption("CSV에 `height`, `weight` 컬럼이 있어야 합니다. 단위는 위에서 선택한 단위와 동일하게 준비하세요.")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file) # CSV를 pandas DataFrame 객체로 변환

    # 단위 변환
    if unit.startswith("Metric"):   # 단위 변환 컬럼 추가
        df["height_m"] = df["height"] / 100
        df["weight_kg"] = df["weight"]
    else:
        df["height_m"] = df["height"] * 0.0254
        df["weight_kg"] = df["weight"] * 0.453592

    # BMI 계산 및 분류 - ⑤
    df["BMI"] = df["weight_kg"] / df["height_m"] ** 2   # BMI 컬럼 추가

    def categorize(b):  # BMI 분류 기준 생성
        if b < 18.5:
            return "저체중"
        elif b < 25:
            return "정상"
        elif b < 30:
            return "과체중"
        else:
            return "비만"

    df["Category"] = df["BMI"].apply(categorize)    # BMI 분류 컬럼 생성

    st.subheader("계산 결과")   # 계산 결과 테이블 시각화
    st.dataframe(df[["height", "weight", "BMI", "Category"]])

    # BMI 히스토그램 - ⑥
    st.subheader("BMI 히스토그램")
    fig, ax = plt.subplots()    # Pyplot을 활용한 서브 플롯 생성
    ax.hist(df["BMI"], bins=20) # 히스토그램 그리기
    ax.set_xlabel("BMI")        # X축 타이틀 설정
    ax.set_ylabel("Frequency")  # Y축 타이틀 설정
    st.pyplot(fig)

    # BMI 분류 별 분포 시각화 - ⑦
    st.subheader("분류별 인원 수")  # 분류 별 빈도 시각과
    counts = df["Category"].value_counts()  # 분류 별 인원 수 집계
    st.bar_chart(counts)    # 분류 결과 막대그래프 시각화