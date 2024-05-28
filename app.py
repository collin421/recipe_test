import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

# 구글 스프레드시트와 연결 설정 함수
def get_gspread_client():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # 환경 변수에서 인증 정보 가져오기
    creds_dict = {
        "type": os.getenv("GSPREAD_TYPE"),
        "project_id": os.getenv("GSPREAD_PROJECT_ID"),
        "private_key_id": os.getenv("GSPREAD_PRIVATE_KEY_ID"),
        "private_key": os.getenv("GSPREAD_PRIVATE_KEY").replace('\\n', '\n'),
        "client_email": os.getenv("GSPREAD_CLIENT_EMAIL"),
        "client_id": os.getenv("GSPREAD_CLIENT_ID"),
        "auth_uri": os.getenv("GSPREAD_AUTH_URI"),
        "token_uri": os.getenv("GSPREAD_TOKEN_URI"),
        "auth_provider_x509_cert_url": os.getenv("GSPREAD_AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": os.getenv("GSPREAD_CLIENT_X509_CERT_URL")
    }
    
    # 자극 증명 개체 생성
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict)
    
    # 자격 증명을 사용하여 클라이언트 객체 생성
    client = gspread.authorize(creds)
    return client

client = get_gspread_client()
sheet = client.open("recipe_service_data").sheet1

def login(username, password, sheet):
    # 스프레드시트에서 모든 레코드 가져오기
    records = sheet.get_all_records()
    
    # 각 레코드를 순회하면서 사용자명과 비밀번호가 일치하는지 확인
    for record in records:
        if record['username'] == username and record['password'] == password:
            return True 
    return False  

def main():
    st.title("로그인 페이지")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    # 로그인 버튼이 눌렸을 때
    if st.button("Login"):
        if login(username, password, sheet):
            st.success("로그인 성공!")  
        else:
            st.error("잘 못된 정보입니다.")

if __name__ == "__main__":
    main()
