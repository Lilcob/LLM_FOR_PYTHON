import streamlit as st
import datetime as dt

# 1. 📅 캘린더
st.header("📅 캘린더")
today = dt.date.today()
selected_date = st.date_input("날짜를 선택하세요", today)
st.write(f"오늘은 {today.strftime('%Y년 %m월 %d일')} 입니다.")