import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import uuid  # 유저 고유 ID 생성을 위해 UUID 라이브러리 사용

# Google 스프레드시트 클라이언트 객체를 얻는 함수
def get_gspread_client():
    # Google API와 통신하기 위한 인증 범위 설정
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
    
    # 인증 정보를 사용하여 gspread 클라이언트 객체 생성
    client = gspread.authorize(creds)
    return client

# gspread 클라이언트 객체 생성
client = get_gspread_client()

# 메인 데이터가 저장된 스프레드시트와 시트 객체
spreadsheet = client.open("recipe_service_data")
sheet = spreadsheet.sheet1

user_sheet = client.open("recipe_service_users")

# 로그인 함수
def login(username, password, sheet):
    # 시트의 모든 기록 가져오기
    records = sheet.get_all_records()
    
    # 각 기록을 순회하며 사용자명과 비밀번호 확인
    for record in records:
        if record['username'] == username and record['password'] == password:
            return True  # 일치하는 경우 True 반환
    return False  # 일치하지 않는 경우 False 반환

# 회원가입 함수
def register(username, password, sheet):
    # 시트의 모든 기록 가져오기
    records = sheet.get_all_records()
    
    # 각 기록을 순회하며 사용자명 중복 확인
    for record in records:
        if record['username'] == username:
            return False  # 사용자명이 이미 존재하면 False 반환

    # 유저 고유 ID 생성
    user_id = str(uuid.uuid4())
    
    # 메인 시트에 유저 ID, 사용자명, 비밀번호 추가
    sheet.append_row([user_id, username, password])
    
    try:
        # 새로운 유저를 위한 시트 생성 (메인 스프레드시트 내에 새로운 워크시트 추가)
        new_sheet_title = f"{username}"
        new_sheet = user_sheet.add_worksheet(title=new_sheet_title, rows="100", cols="20")
        
        # 유저의 개인 시트에 기본 헤더 추가 (예: 레시피 이름, 재료, 조리법)
        new_sheet.append_row(["날짜", "음식명", "칼로리"])
        
        print(f"New sheet created: {new_sheet_title}")  # 디버깅을 위한 메시지 출력
        
        # 디버깅을 위해 생성된 시트의 정보를 출력합니다.
        sheet_list = user_sheet.worksheets()
        print("Available sheets:")
        for sh in sheet_list:
            print(sh.title)
        
        # 생성된 시트의 URL을 반환
        #sheet_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet.id}/edit#gid={new_sheet.id}"
        return True #, sheet_url  # 회원가입 성공 시 True와 시트 URL 반환
        
    except Exception as e:
        print(f"An error occurred while creating a new sheet: {e}")  # 예외 발생 시 오류 메시지 출력
        return False, None  # 오류 발생 시 False와 None 반환


# 지정된 사용자 이름의 워크시트에서 모든 데이터를 가져오는 함수
def fetch_user_data(username, client):
    # 사용자 데이터를 저장하고 있는 스프레드시트 열기
    user_sheet = client.open("recipe_service_users")
    try:
        # 사용자 이름으로 명명된 워크시트 열기
        worksheet = user_sheet.worksheet(title=username)
        
        # 워크시트의 모든 데이터를 레코드 형태로 가져오기
        user_data = worksheet.get_all_records()
        return user_data
    except Exception as e:
        # 데이터를 가져오는 중 에러 발생 시 에러 메시지 출력
        print(f"An error occurred while fetching data for {username}: {e}")
        return None