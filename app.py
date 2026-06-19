import streamlit as st
import json, os

st.set_page_config(page_title="오늘의 유튜브 랭킹", page_icon="📺", layout="wide")
st.title("📺 오늘의 유튜브 랭킹 TOP 50")

if os.path.exists("data/latest.json"):
    with open("data/latest.json", "r", encoding="utf-8") as f:
        for item in json.load(f):
            col1, col2 = st.columns([1, 4])
            with col1:
                st.image(item["thumbnail"])
            with col2:
                st.subheader(f"{item['rank']}위. {item['title']}")
                st.write(f"👤 {item['channel']} | 👀 {int(item['viewCount']):,}회")
                st.link_button("👉 영상 보러가기", item["url"])
            st.write("---")
else:
    st.error("데이터 없음. collector.py를 먼저 실행하세요!")