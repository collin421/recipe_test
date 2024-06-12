import streamlit as st
from utils import get_gspread_client, fetch_user_data


# Streamlit 앱의 세션 상태 변수 초기화
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# 사용자 로그인 상태 확인
if not st.session_state.logged_in:
    st.warning("로그인해주세요.")  # 로그인이 되어있지 않은 경우 경고 메시지 출력
else:
    # 세션 데이터 가져오기
    st.title("개인 페이지")
    st.write(f"환영합니다, {st.session_state.username}님!")
    st.write(st.session_state)

    # 로그인한 사용자의 데이터 가져오기
    client = get_gspread_client()
    user_data = fetch_user_data(st.session_state.username, client)
    
    if user_data:
        # 데이터를 Streamlit 표 형식으로 보여주기
        st.write(f"{st.session_state.username}님의 데이터:", user_data)
    else:
        st.write("데이터를 가져오는 데 실패했습니다.")  # 데이터를 가져오는데 실패한 경우 메시지 출력

    # 로그아웃 버튼 추가
    if st.button("로그아웃"):
        # 로그아웃 시 세션 상태 초기화
        st.session_state.logged_in = False
        st.session_state.login_success = False
        st.session_state.username = ""
        st.success("로그아웃 성공!")  # 로그아웃 성공 메시지 출력
        st.experimental_rerun()  # Streamlit 앱을 다시 실행하여 로그인 화면으로 돌아감


