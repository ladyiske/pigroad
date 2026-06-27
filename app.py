import streamlit as st
import random
import csv
import os

# 1. 웹페이지 설정 및 제목
st.set_page_config(page_title="돼지름길", page_icon="🐷", layout="centered")
st.title("🐷 돼지름길")
st.subheader("오늘 뭐 먹지? 고민 끝, 지름길로 가세요!")

# 2. 카테고리 정의
categories = ["한식", "중식", "양식", "일식", "동남아", "디저트"]

# 3. 사용자 선택 UI
category = st.selectbox("원하는 음식 종류를 선택하세요:", options=categories)

# 4. 버튼 클릭 감지 및 파일명 설정
clicked = st.button(f"{category} 메뉴 추천받기 ✨")

if clicked:
    # 파일 이름 규칙 (현재 저장하신 파일명 형식 기준)
    file_name = f"{category}.xlsx - Sheet1.csv"
    
    # 만약 나중에 파일명을 '한식.csv' 형태로 바꾸시면 아래 줄의 주석(#)을 제거하세요.
    # file_name = f"{category}.csv"

    # 파일 존재 여부 확인 (버튼 아래에서 바로 검사하도록 수정)
    if not os.path.exists(file_name):
        st.error(f"'{file_name}' 파일을 찾을 수 없습니다. 깃허브에 파일이 잘 올라갔는지 확인해 주세요!")
    else:
        with open(file_name, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)  # 헤더(menu) 건너뛰기
            menus = [row[0].strip() for row in reader if row and row[0].strip()]
        
        if menus:
            recommended_menu = random.choice(menus)
            st.success(f"오늘의 추천 메뉴는 바로 **[{recommended_menu}]** 입니다! 츄릅 😋")
        else:
            st.error(f"{category} 파일에 저장된 메뉴가 없습니다.")
