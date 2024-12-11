import os, sys, time
import numpy as np
import pandas as pd
import streamlit as st
from quizzes import quizzes
from PIL import Image
from datetime import datetime
import pytz

import warnings
warnings.filterwarnings('ignore')

def show_home():
    st.title("Advent Calender Quiz 🎅")
    st.write('##### ㅡ 크리스마스를 기다리며 매일 오픈되는 퀴즈를 풀어보세요!')
    st.write('---')

    year = 2024
    month = 12

    cal = [[1,2,3,4,5,6,7],
           [8,9,10,11,12,13,14],
           [15,16,17,18,19,20,21],
           [22,23,24,25]]

    # 오늘 날짜 가져오기
    # 현재 UTC 시간 가져오기
    utc_now = datetime.now(pytz.utc)

    # 한국 시간으로 변환
    korea_tz = pytz.timezone('Asia/Seoul')
    today = utc_now.astimezone(korea_tz)
    today_day = today.day if today.month == month and today.year == year else 0  # 현재 월과 연도에 따라 일수 확인

    # 달력 그리기
    cols = st.columns(7)
    for i in range(7):
        weekday = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'][i]
        cols[i].markdown(f'<div style="font-size: 17px; font-weight: bold; border-radius: 5px; background-color: seagreen; text-align: center; padding: 5px; color: white;">{weekday}</div>', unsafe_allow_html=True)   
    st.write('')
    for week in cal:
        cols = st.columns(7)
        for i, day in enumerate(week):
            if day == 0:
                cols[i].write("")  # 빈 칸
            else:
                if day < 25:
                    if day <= today_day:
                        day_button = cols[i].button(f"**{day}**", key=day, type='primary', use_container_width = True)
                    else:
                        day_button = cols[i].button(f"**{day}**", key=day, disabled = True, use_container_width = True)
                    # 버튼 클릭 시 퀴즈 페이지로 이동
                    if day_button:
                        st.session_state.selected_day = day
                        st.rerun()
    st.write('---')

def show_quiz(day):
    if day < 24:
        st.header(f"🎈 12월 {day}일 퀴즈")
        st.write('---')
        question = quizzes[day]["question"]
        answer = quizzes[day]["answer"]
        description = quizzes[day]["description"]
        
        col1, col2 = st.columns([8,2])
        with col1:
            st.write(f"#### Q. {question}")
            st.write('※ 단답형 주관식이며, 모든 정답은 한글로 작성해주세요.(숫자는 가능)')
            user_answer = st.text_input(label='answer', label_visibility='hidden').strip()
            if st.button("제출"):
                if user_answer in answer:
                    st.success("정답입니다.")
                    st.info(description)
                else:
                    st.error("정답이 아닙니다.")
        with col2:
            img_path = f'images/q{day}.jpg'
            try:
                img = Image.open(img_path)
                st.image(img)
            except FileNotFoundError:
                st.write(f"{day}일 이미지 없음")
    elif day == 24:
        st.header('🎉 Finally, Today is Christmas Eve!')
        st.write('---')
        eve_image = 'merry-christmas.png'
        st.image(eve_image, use_container_width=True)

        go_link = '''
                    <a href="https://colormytree.me/2024/01GN25CR9M6GWYBY8KS91N7HXQ" target="_blank" style="width: 100%; text-decoration: none;">
                        <button style="width: 100%; font-size: 17px; font-weight: bold; padding: 5px; background-color: seagreen; color: white; border: none; border-radius: 5px; cursor: pointer;">
                            크리스마스 트리 구경하러 가기
                        </button>
                    </a>
                    '''
        st.markdown(go_link, unsafe_allow_html=True)
    else:
        st.write('---')

def main():
    st.set_page_config(page_icon='🎁', page_title="Advent Calender Quiz", layout="wide")
    
    if 'selected_day' not in st.session_state:
        st.session_state.selected_day = None
    
    st.sidebar.title('👋 Happy Merry Christmas!')
    if st.sidebar.button('**처음으로**', use_container_width = True):
        st.session_state.selected_day = None
        st.rerun()

    day = st.session_state.selected_day
    if day == None:
        show_home()
    else:
        show_quiz(day)

if __name__ == "__main__":
    main()
