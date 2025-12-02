import pandas as pd
import streamlit as st
import sqlite3
from quizzes import quizzes2
from PIL import Image
from datetime import datetime
import pytz

import warnings
warnings.filterwarnings('ignore')

def connect_db():
    conn = None
    try:
        conn = sqlite3.connect('data.db')
    except Exception as e:
        st.write(e)
    
    return conn

def create_table():
    conn = connect_db()
    create_query = """
                   CREATE TABLE IF NOT EXISTS Members(
                       id integer primary key autoincrement,
                       name varchar(10) not null,
                       iscorrect1 boolean default False not null,
                       iscorrect2 boolean default False not null,
                       iscorrect3 boolean default False not null,
                       iscorrect4 boolean default False not null,
                       iscorrect5 boolean default False not null,
                       iscorrect6 boolean default False not null,
                       iscorrect7 boolean default False not null,
                       iscorrect8 boolean default False not null,
                       iscorrect9 boolean default False not null,
                       iscorrect10 boolean default False not null,
                       iscorrect11 boolean default False not null,
                       iscorrect12 boolean default False not null,
                       iscorrect13 boolean default False not null,
                       iscorrect14 boolean default False not null,
                       iscorrect15 boolean default False not null,
                       iscorrect16 boolean default False not null,
                       iscorrect17 boolean default False not null,
                       iscorrect18 boolean default False not null,
                       iscorrect19 boolean default False not null,
                       iscorrect20 boolean default False not null,
                       iscorrect21 boolean default False not null,
                       iscorrect22 boolean default False not null,
                       iscorrect23 boolean default False not null,
                       iscorrect24 boolean default False not null
                   );
                   """
    conn.execute(create_query)
    conn.commit()
    conn.close()

def read_table():
    conn = connect_db()
    select_query = "SELECT * FROM Members;"
    df = pd.read_sql_query(select_query, conn)
    conn.close()

    return df

def insert_table(new_user):
    conn = connect_db()
    insert_query = """
                   INSERT INTO Members (id, name, iscorrect1, iscorrect2, iscorrect3, iscorrect4,
                                        iscorrect5, iscorrect6, iscorrect7, iscorrect8, iscorrect9,
                                        iscorrect10, iscorrect11, iscorrect12, iscorrect13, iscorrect14,
                                        iscorrect15, iscorrect16, iscorrect17, iscorrect18, iscorrect19,
                                        iscorrect20, iscorrect21, iscorrect22, iscorrect23, iscorrect24)
                   VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);
                   """
    conn.execute(insert_query, (len(df), new_user, False, False, False, False, False, False, False, False, False, False,
                                False, False, False, False, False, False, False, False, False, False, False, False, False, False))
    conn.commit()
    conn.close()

def update_table(user, day):
    conn = connect_db()
    col_name = f'iscorrect{day}'
    update_query = f"UPDATE Members SET {col_name} = ? WHERE name = ?;"
    conn.execute(update_query, (True, user))
    conn.commit()
    conn.close()

def delete_table(user):
    conn = connect_db()
    delete_query = f"DELETE FROM Members WHERE name = ?;"
    conn.execute(delete_query, (user,))
    conn.commit()
    conn.close()

def drop_table():
    conn = connect_db()
    drop_query = "DROP TABLE IF EXISTS Members;"
    conn.execute(drop_query)
    conn.commit()
    conn.close()

def login():
    st.title("2025 Advent Calender Quiz 🎅")
    st.write('##### ㅡ 크리스마스를 기다리며 매일 오픈되는 퀴즈를 풀어보세요!')
    st.write('---')

    st.write('##### 🏷️ 이름을 입력하세요.')
    name = st.text_input(label='이름', label_visibility='collapsed').strip()
    if st.button('입력'):
        if df['name'].isin([name]).any():
            st.session_state.user_name = name
            st.success(f'{name}님, 안녕하세요👋')
            if st.button('퀴즈 풀러가기'):
                st.rerun()
        elif name == "":
            st.error('이름을 1글자 이상 입력하세요.')
        else:
            st.session_state.user_name = name
            insert_table(name)
            st.success(f'{name}님, 첫 방문을 환영합니다!')
            if st.button('퀴즈 풀러가기'):
                st.rerun()

def show_members():
    st.header("Members")
    st.write('---')

    conn = connect_db()
    edit_data = st.data_editor(df, hide_index=True)
    if st.button("Save Changes"):
        edit_data.sort_values(by='id', inplace=True)
        edit_data.to_sql('Members', conn, if_exists='replace', index=False)
        st.success("Changes saved to the database.")
    st.write('---')

    user_list = df['name'].tolist()
    delete_name = st.selectbox("Select a user to delete", user_list)
    if st.button('삭제하기'):
        delete_table(delete_name)
        st.success(f'{delete_name}님의 데이터가 삭제되었습니다.')
        st.rerun()
    
    if st.button('테이블 삭제'):
        drop_table()
        st.success('테이블이 삭제되었습니다.')
        st.rerun()

def show_home():
    st.title("2025 Advent Calender Quiz🎅")
    st.write('##### ㅡ 크리스마스를 기다리며 매일 오픈되는 퀴즈를 풀어보세요!')
    st.write('---')

    year = 2025
    month = 12

    cal = [[30,1,2,3,4,5,6],
           [7,8,9,10,11,12,13],
           [14,15,16,17,18,19,20],
           [21,22,23,24,25]]

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
        cols[i].markdown(f'<div style="font-size: 18px; font-weight: bold; border-radius: 5px; background-color: seagreen; text-align: center; padding: 5px; color: white;">{weekday}</div>', unsafe_allow_html=True)   
    st.write('')
    for week in cal:
        cols = st.columns(7)
        for i, day in enumerate(week):
            if day == 0:
                cols[i].write("")  # 빈 칸
            else:
                if day <= 25:
                    if day == 1 or (day <= today_day and st.session_state.answer_list[day-2] == True):
                        day_button = cols[i].button(f"**{day}**", key=day, type='primary', use_container_width = True)
                    else:
                        day_button = cols[i].button(f"**{day}**", key=day, disabled = True, use_container_width = True)
                    # 버튼 클릭 시 퀴즈 페이지로 이동
                    if day_button:
                        st.session_state.selected_day = day
                        st.rerun()
    st.write('---')

def show_quiz(day):
    st.header(f"🎈 12월 {day}일 퀴즈")
    st.write('---')
    question = quizzes2[day]["question"]
    answer = quizzes2[day]["answer"]
    description = quizzes2[day]["description"]
    
    col1, col2 = st.columns([8,2])
    with col1:
        st.write(f"#### Q. {question}")
        if day == 9:
            st.write('※ 단답형 주관식이며, 이 문제의 정답은 영어로 작성해주세요.')
        else:
            st.write('※ 단답형 주관식이며, 정답은 한글로 작성해주세요.(숫자는 가능)')
        user_answer = st.text_input(label='answer', label_visibility='hidden').strip().lower()
        if st.button("제출"):
            if user_answer in answer:
                st.success("딩동댕! 정답입니다.")
                st.info(description)
                update_table(st.session_state.user_name, day)
            else:
                st.error("땡! 오답입니다. 다시 풀어주세요.")
    with col2:
        img_path = f'images/q{day}.jpg'
        try:
            img = Image.open(img_path)
            st.image(img)
        except FileNotFoundError:
            st.write(f"{day}일 이미지 없음")
    if day == 24 and user_answer in answer:
        st.write('---')
        st.warning(f'{st.session_state.user_name}님, 모든 퀴즈를 통과하셨습니다. 아래 버튼을 클릭해주세요.')
        go_link = '''
                <a href="https://colormytree.me/2025/01GN25CR9M6GWYBY8KS91N7HXQ" target="_blank" style="width: 100%; text-decoration: none;">
                    <button style="width: 100%; font-size: 17px; font-weight: bold; padding: 5px; background-color: seagreen; color: white; border: none; border-radius: 5px; cursor: pointer;">
                        크리스마스 트리 구경하러 가기
                    </button>
                </a>
                '''
        st.markdown(go_link, unsafe_allow_html=True)

def main():
    st.set_page_config(page_icon='🎁', page_title="2025 Advent Calender Quiz", layout="wide")

    if 'selected_day' not in st.session_state:
        st.session_state.selected_day = None
    if 'user_name' not in st.session_state:
        st.session_state.user_name = None
    if 'answer_list' not in st.session_state:
        st.session_state.answer_list = None
    
    create_table()
    global df
    df = read_table()

    user_name = st.session_state.user_name        
    st.sidebar.title('🎉 Happy Merry Christmas!')
    if user_name != None:
        st.sidebar.write(f'### {user_name}님, 안녕하세요👋')
        if st.sidebar.button('**로그아웃**', use_container_width=True):
            st.session_state.user_name = None
            st.rerun()
    if st.sidebar.button('**메인화면**', type = 'primary', use_container_width = True):
        st.session_state.selected_day = None
        st.rerun()
    # if st.sidebar.button('테이블 삭제', use_container_width=True):
    #     drop_table()
    #     st.rerun()
    
    answer_list = df.loc[df['name'] == user_name].values.flatten().tolist()[2:]
    st.session_state.answer_list = answer_list
    st.sidebar.write(zip(answer_list.index, answer_list.value))
    if user_name == None:
        login()
    elif user_name == '관리자':
        show_members()
    else:
        day = st.session_state.selected_day
        if day == None:
            show_home()
        else:
            show_quiz(day)

if __name__ == "__main__":
    main()
