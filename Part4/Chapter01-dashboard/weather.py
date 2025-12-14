import streamlit as st
import requests
import datetime as dt
from datetime import timedelta

# 2. ☁️ 현재 날씨
st.header("☁️ 현재 날씨")

# 날씨 코드에 따른 설명 매핑
weather_code_descriptions = {
    0: "☀️ 맑음",
    1: "🌤 약간 흐림",
    2: "⛅ 대체로 흐림",
    3: "☁️ 흐림",
    45: "🌫 안개",
    48: "🌫 서리낀 안개",
    51: "🌦 가벼운 이슬비",
    53: "🌦 중간 이슬비",
    55: "🌧 강한 이슬비",
    61: "🌦 약한 비",
    63: "🌧 중간 비",
    65: "🌧 강한 비",
    66: "🌧 약간 얼어붙는 비",
    67: "🌧 강한 얼어붙는 비",
    71: "🌨 약한 눈",
    73: "🌨 중간 눈",
    75: "🌨 강한 눈",
    77: "🌨 진눈깨비",
    80: "🌧 소나기",
    81: "🌧 중간 소나기",
    82: "🌧 강한 소나기",
    95: "⛈ 천둥번개",
    96: "⛈ 천둥 + 약한 우박",
    99: "⛈ 천둥 + 강한 우박",
}

# 한국 주요 도시 목록
city_coords = {
    "서울": (37.5665, 126.9780),
    "부산": (35.1796, 129.0756),
    "대구": (35.8714, 128.6014),
    "인천": (37.4563, 126.7052),
    "광주": (35.1595, 126.8526),
    "대전": (36.3504, 127.3845),
    "울산": (35.5384, 129.3114),
    "수원": (37.2636, 127.0286),
    "성남": (37.4202, 127.1265),
    "고양": (37.6584, 126.8320),
    "용인": (37.2411, 127.1776),
    "청주": (36.6424, 127.4890),
    "전주": (35.8242, 127.1480),
    "제주": (33.4996, 126.5312)
}

# 드롭다운으로 선택
selected_city = st.selectbox("도시를 선택하세요", list(city_coords.keys()))

if st.button("3시간 간격 24시간 날씨 보기"):
    latitude, longitude = city_coords[selected_city]
    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={latitude}&longitude={longitude}"
        f"&hourly=temperature_2m,windspeed_10m,weathercode"
        f"&timezone=Asia%2FSeoul"
    )

    response = requests.get(weather_url)
    if response.status_code == 200:
        data = response.json()
        hourly = data.get("hourly", {})
        times = hourly.get("time", [])
        temps = hourly.get("temperature_2m", [])
        winds = hourly.get("windspeed_10m", [])
        codes = hourly.get("weathercode", [])

        now = dt.datetime.now()
        forecast = []
        for i in range(len(times)):
            forecast_time = dt.datetime.fromisoformat(times[i])
            if now <= forecast_time <= now + timedelta(hours=24):
                if forecast_time.hour % 3 == 0:
                    description = weather_code_descriptions.get(codes[i], "❓ 알 수 없음")
                    forecast.append((forecast_time.strftime("%Y-%m-%d %H:%M"), temps[i], winds[i], description))

        for time_str, temp, wind, desc in forecast:
            st.info(f"🕒 {time_str} → {desc} | 🌡 {temp}°C | 💨 {wind} km/h")
    else:
        st.error("예보 데이터를 가져오지 못했습니다.")