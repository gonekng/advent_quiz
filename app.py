import streamlit as st
from quizzes import quizzes
import calendar
from PIL import Image
from datetime import datetime

import warnings
warnings.filterwarnings('ignore')

def show_home():
    st.title("Advent Calender Quiz 🎅")
    st.write('##### ㅡ 크리스마스를 기다리며 매일 오픈되는 퀴즈를 풀어보세요!')
    st.write('---')

    # 2024년 12월 달력 생성
    year = 2024
    month = 12
    cal = calendar.monthcalendar(year, month)

    # 오늘 날짜 가져오기
    today = datetime.now()
    today_day = today.day if today.month == month and today.year == year else 0  # 현재 월과 연도에 따라 일수 확인

    # 달력 그리기
    cols = st.columns(7)
    for i in range(7):
        weekday = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'][i]
        cols[i].markdown(f'<div style="font-size: 18px; font-family: bold; text-align: center; padding: 5px; background-color: darkgreen; color: white;">{weekday}</div>', unsafe_allow_html=True)   
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
            user_answer = st.text_input(label='answer', label_visibility='hidden')
            if st.button("제출"):
                if user_answer.strip() == answer:
                    st.success("정답입니다.")
                    st.info(description)
                else:
                    st.error(f"정답이 아닙니다.")
        with col2:
            img_path = f'images/q{day}.jpg'
            try:
                img = Image.open(img_path)
                st.image(img, use_container_width = True)
            except FileNotFoundError:
                st.write(f"{day}일 이미지 없음")
    elif day == 24:
        st.header('🎉 Finally, Today is Christmas Eve!')
        st.write('---')
    else:
        st.write('---')

def main():
    st.set_page_config(page_title="Advent Calender Quiz", layout="wide")
    
    if 'selected_day' not in st.session_state:
        st.session_state.selected_day = None
    
    st.sidebar.title('Merry Christmas !')
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
