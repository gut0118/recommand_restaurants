import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime

# https://zzsza.github.io/mlops/2021/02/07/python-streamlit-dashboard/

st.title(f'M&S팀 {datetime.today().strftime("%y년 %m월 %d일")} 점심메뉴')

button_style = """
    <style>
    .stButton > button {
        background-color: #073056;
        color: white;
        font-weight: bold;
        width: 100%;
        border: none;
        border-radius: 4px; 
        cursor: pointer; 
    }
    .stButton > button:hover {
        background-color: #CACBDF; /* 마우스 오버시 배경색 변경 */
        color: white;
        font-weight: bold;
    }
    </style>
    """

uploaded_file = "./restaurants.csv"

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("")
    st.subheader("탐험지수")
    # exploration = st.selectbox("새로운 곳에 대한 가중치", [1, 2, 3, 4, 5])
    option_exploration = st.selectbox("새로운 곳에 대한 가중치", ["평균값", "평균값*1.5", "평균값*0.7", "최대값", "최대값*1.3"])

    # type_distance = list(data["도보거리"].unique()) # 도보 3분, 5분, 10분, 20분
    type_recommender = list(data["추천인"].unique())
    type_fresh = list(data["미방문"].unique()) # 미방문 1, 방문 0

    st.write("")
    st.subheader("허용거리")
    option_distance = st.multiselect('너무 오래 걸리면 힘들어... 몇분까지 걸을수 있어?', [1, 3, 5, 10, 15, 20])
    st.write("")
    st.subheader("추천인")
    option_recommender = st.multiselect('니가 추천한 곳만 가자', type_recommender)
    st.write("")
    st.subheader("미방문")
    option_fresh = st.multiselect('오늘은 안가본 곳 가볼까?', type_fresh)
    st.write("")

    data['최종가중치'] = data['가중치'].replace('', np.nan).astype(float)

    if option_exploration == "평균값":
        exploration = data['가중치'].mean()
    elif option_exploration == "평균값*1.5":
        exploration = data['가중치'].mean()*1.5
    elif option_exploration == "평균값*0.7":
        exploration = data['가중치'].mean()*0.7
    elif option_exploration == "최대값":
        exploration = data['가중치'].max()
    elif option_exploration == "최대값*1.3":
        exploration = data['가중치'].max()*1.3
    else:
        pass

    # data['최종가중치'].fillna(data['가중치'].mean()*exploration, inplace=True)
    data['최종가중치'].fillna(exploration, inplace=True)

    # 음식종류 필터링
    if option_distance:
        data = data[data['도보거리'] <= max(option_distance)]
    if option_recommender:
        data = data[data['추천인'].isin(option_recommender)]
    if option_fresh:
        data = data[data['미방문'].isin(option_fresh)]

    st.write(data)

    st.markdown(button_style, unsafe_allow_html=True) # CSS 스타일 적용

    if st.button("result...."):
        with st.expander('어디에서 먹을까....'):
            probabilities = data['최종가중치'] / data['최종가중치'].sum()
            chosen_row = data.sample(1, weights=probabilities)
            st.write("")
            # st.write("추천 식당 :", chosen_row.iloc[0]['식당명'])
            st.subheader(f":green[{chosen_row.iloc[0]['식당명']}]")
            # st.write("Combining **bold and :green[colored text] is totally** fine! Just like with other markdown features.")
            url = chosen_row.iloc[0]['링크']
            st.markdown(f"[{chosen_row.iloc[0]['식당명']} 방문하기]({url})", unsafe_allow_html=True)

