# API: https://docs.streamlit.io/
# emoji: https://snskeyboard.com/emoji/

# run: streamlit run ./app.py

import streamlit as st
import re
from datetime import datetime

from src.collector import news_collector

news_category = {
    "society": "사회",
    "politics": "정치",
    "economic": "경제",
    "foreign": "국제",
    "culture": "문화",
    "entertain": "연예",
    "sports": "스포츠",
    "digital": "IT"
}

st.set_page_config(
    page_title="뉴스 수집기",
    page_icon="./images/favicon_03.png"
)

st.markdown("""
<style>
</style>
""", unsafe_allow_html=True)

st.title(":blue[NEWS] Collector")
st.text("DAUM 뉴스를 수집합니다.")


@st.cache_data
def convert_df(df):
   return df.to_csv(index=False, encoding="cp949")


flag = False
with st.form(key="form"):
    category = st.text_input(label="수집하고 싶은 뉴스 카테고리를 입력해주세요.").strip()
    submitted = st.form_submit_button("Submit")
    if submitted:
        if category in list(news_category.keys()):
            st.write(f'"{news_category[category]}" 뉴스를 수집 합니다.')
            df_news, count = news_collector(category)
            csv = convert_df(df_news)
            flag = True
            now = datetime.now().strftime("%Y.%m.%d %H:%M:%S")
        else:
            st.write("올바른 뉴스 카테고리를 입력해주세요.")

if flag:
    st.write(f'"{news_category[category]}" 뉴스 {count}건 수집 완료')
    now = datetime.now().strftime("%Y_%m_%d_%H%M%S")
    st.download_button(
        label="Press to Download",
        data=csv,
        file_name=f"{news_category[category]}_뉴스_{now}.csv",
        mime="text/csv",
        key='download-csv')

with st.expander(label="**DAUM 뉴스 카테고리**", expanded=False):
    for key, value in news_category.items():
        st.text(f"{key}({value})")
    st.link_button("LINK", "https://news.daum.net/breakingnews/")