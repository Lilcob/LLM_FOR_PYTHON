import streamlit as st
import requests
from xml.etree import ElementTree as ET

# 4. 📰 뉴스 헤드라인
st.header("📰 주요 뉴스 헤드라인")

news_url = "https://rss.etnews.com/Section902.xml"  # 전자신문 IT뉴스 RSS
rss_response = requests.get(news_url)

if rss_response.status_code == 200:
    root = ET.fromstring(rss_response.content)
    items = root.findall('.//item')
    news_list = []
    for item in items[:5]:  # 상위 5개 뉴스
        title = item.find('title').text
        link = item.find('link').text
        news_list.append((title, link))

    for title, link in news_list:
        st.markdown(f"- [{title}]({link})")
else:
    st.error("뉴스 정보를 가져오지 못했습니다.")