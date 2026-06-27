
import streamlit as st
import random
import csv
import os

# 세션 상태 초기화 (이전 추천 결과 기억용)
if "recommended_menu" not in st.session_state:
    st.session_state.recommended_menu = ""

# 1. 웹페이지 설정 및 제목
st.set_page_config(page_title="돼지름길", page_icon="🐷", layout="centered")
st.title("🐷 돼지름길")
st.subheader("오늘 뭐 먹지? 고민 끝, 지름길로 가세요!")

# 2. 카테고리 정의 (실제 저장하신 파일명과 일치해야 합니다)
categories = ["한식", "중식", "양식", "일식", "동남아", "디저트"]

# 3. 사용자 선택 UI
category = st.selectbox(
    "원하는 음식 종류를 선택하세요:",
    options=categories
)

# 4. 추천 버튼 클릭 시 로직
if st.button(f"{category} 메뉴 추천받기 ✨"):
    # 파일 이름 규칙 설정 (예: 한식.xlsx - Sheet1.csv 또는 한식.csv)
    # 현재 올려주신 파일명 형식인 '카테고리.xlsx - Sheet1.csv' 기준입니다.
    
    
    # 만약 파일 이름을 '한식.csv', '중식.csv'로 변경하셨다면 아래 주석을 해제하고 위 줄을 지우세요.
     file_name = f"{category}.csv"

    # 파일이 존재하는지 확인
    if os.path.exists(file_name):
        with open(file_name, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)  # 첫 번째 줄(menu 헤더)은 건너뜁니다.
            
            # 공백이 아닌 메뉴 이름만 리스트로 추출
            menus = [row[0].strip() for row in reader if row and row[0].strip()]
        
        if menus:
            # 리스트에서 무작위로 하나 추출하여 세션에 저장
            st.session_state.recommended_menu = random.choice(menus)
        else:
            st.error(f"{category} 파일에 저장된 메뉴가 없습니다.")
    else:
        st.error(f"'{file_name}' 파일을 찾을 수 없습니다. 파일명을 확인해 주세요!")

# 5. 결과 출력
if st.session_state.recommended_menu:
    st.success(f"오늘의 추천 메뉴는 바로 **[{st.session_state.recommended_menu}]** 입니다! 츄릅 😋")
