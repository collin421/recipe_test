import streamlit as st
from utils import login, sheet, register

st.set_page_config(page_title="My Multipage App",)

# st.title("main page")
st.sidebar.success("select a page above.")

tab1, tab2 = st.tabs(["로그인", "회원가입"])

with tab1:
    if 'login_success' not in st.session_state:
        st.session_state.login_success = False

    st.title("로그인 페이지")
    username = st.text_input("이름", key="login_username")
    password = st.text_input("비밀번호", type="password", key="login_password")

    if st.button("로그인"):
        if login(username, password, sheet):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.login_success = True
            st.experimental_rerun()
        else:
            st.error("잘못된 정보입니다.")

    # 로그인 성공 메시지 유지
    if st.session_state.login_success:
        st.success("로그인 성공!")

with tab2:
    st.header("회원가입")
    # 신규 유저 이름 입력받기
    new_username = st.text_input("신규 유저 이름", key="register_username")

    # 비밀번호 입력받기 (비밀번호는 숨김 처리)
    new_password = st.text_input("비밀번호", type="password", key="register_password")

    # 회원가입 버튼을 클릭했을 때의 동작 정의
    if st.button("회원가입"):
        # 회원가입 함수 호출
        if register(new_username, new_password, sheet):
            st.success("회원가입 성공!")  # 회원가입 성공 시 메시지 출력
        else:
            st.error("사용자명이 이미 존재합니다.")  # 사용자명이 중복될 경우 오류 메시지 출력

