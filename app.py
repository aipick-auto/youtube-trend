import streamlit as st
import requests

st.set_page_config(page_title="오늘의 유튜브 랭킹", page_icon="📺", layout="wide")
st.title("📺 오늘의 유튜브 랭킹 TOP 50")
st.caption("매일 업데이트되는 광고 없는 유튜브 인기 차트")
st.write("---")

@st.cache_data(ttl=3600)
def get_trending():
    api_key = st.secrets["YOUTUBE_API_KEY"]
    url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet,statistics",
        "chart": "mostPopular",
        "regionCode": "KR",
        "maxResults": 50,
        "key": api_key
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return None

    items = response.json().get("items", [])
    result = []
    for i, item in enumerate(items):
        snippet = item["snippet"]
        stats = item["statistics"]
        result.append({
            "rank": i + 1,
            "title": snippet["title"],
            "videoId": item["id"],
            "thumbnail": snippet["thumbnails"]["high"]["url"],
            "channel": snippet["channelTitle"],
            "viewCount": stats.get("viewCount", "0"),
            "url": f"https://www.youtube.com/watch?v={item['id']}"
        })
    return result

data = get_trending()

if data:
    for item in data:
        col1, col2 = st.columns([1, 4])
        with col1:
            # 썸네일 클릭 시 유튜브로 이동
            st.markdown(
                f'<a href="{item["url"]}" target="_blank">'
                f'<img src="{item["thumbnail"]}" width="100%" '
                f'style="border-radius:8px; cursor:pointer;">'
                f'</a>',
                unsafe_allow_html=True
            )
        with col2:
            # 순위 + 제목 클릭 시 유튜브로 이동
            st.markdown(
                f'### [{item["rank"]}위. {item["title"]}]({item["url"]})',
                unsafe_allow_html=True
            )
            st.write(f"👤 {item['channel']} | 👀 {int(item['viewCount']):,}회")
        st.write("---")
else:
    st.error("데이터를 가져올 수 없습니다. 잠시 후 다시 시도해 주세요.")
