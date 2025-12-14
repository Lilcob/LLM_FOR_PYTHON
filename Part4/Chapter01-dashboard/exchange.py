import streamlit as st
import requests

# 3. 💱 환율 (USD -> KRW)
st.header("💱 환율 (USD -> KRW)")

exchange_url = "https://open.er-api.com/v6/latest/USD"
exchange_response = requests.get(exchange_url)

if exchange_response.status_code == 200:
    exchange_data = exchange_response.json()
    
    if 'rates' in exchange_data and 'KRW' in exchange_data['rates']:
        usd_krw = exchange_data['rates']['KRW']
        update_time_utc = exchange_data.get('time_last_update_utc', '업데이트 시간 정보 없음')

        # 환율 값 표시
        st.metric(label="1달러당 원화", value=f"{usd_krw:.2f} 원")

        # 환율 기준 시간 표시
        st.caption(f"⏰ 기준 시각 (UTC 기준): {update_time_utc}")

    else:
        st.error("환율 데이터를 불러오는데 실패했습니다.")
else:
    st.error("환율 API 서버에 연결할 수 없습니다.")