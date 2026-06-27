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

# 2. 카테고리 정의
categories = ["한식", "중식", "양식", "일식", "동남아", "디저트"]

# 3. 사용자 선택 UI
category = st.selectbox(
    "원하는 음식 종류를 선택하세요:",
    options=categories
)

# 4. 추천 버튼 클릭 시 로직
if st.button(f"{category} 메뉴 추천받기 ✨"):
    # 파일 이름 규칙 설정 (현재 깃허브에 올리신 파일명 형태 기준)
    
    
    # ⚠️ 만약 파일 이름을 '한식.csv', '중식.csv'로 바꿨다면 아래 줄의 주석(#)을 지우고 사용하세요.
     file_name = f"{category}.csv"

    # 파일이 존재하는지 확인 (이 부분의 들여쓰기를 정확히 맞췄습니다)
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
        st.error(f"'{file_name}' 파일을 찾을 수 없습니다. 깃허브에 파일이 잘 올라갔는지 확인해 주세요!")

# 5. 결과 출력
if st.session_state.recommended_menu:
    st.success(f"오늘의 추천 메뉴는 바로 **[{st.session_state.recommended_menu}]** 입니다! 츄릅 😋")
