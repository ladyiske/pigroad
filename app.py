import streamlit as st
import random
import csv
import os

# 1. 웹페이지 설정 및 제목
st.set_page_config(page_title="돼지름길", page_icon="🐷", layout="centered")

# 🎨 [추가된 코드] 웹사이트 배경을 연핑크로 변경하는 마법의 코드
st.markdown(
    """
    <style>
    .stApp {
        background-color: #FFF0F2;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🐷 돼지름길")
st.subheader("오늘 뭐 먹지? 고민 끝, 지름길로 가세요!")

# 2. 카테고리 정의
categories = ["한식", "중식", "양식", "일식", "동남아", "디저트"]

# 3. 사용자 선택 UI
category = st.selectbox("원하는 음식 종류를 선택하세요:", options=categories)

# 4. 버튼 클릭 감지
clicked = st.button(f"{category} 메뉴 추천받기 ✨")

if clicked:
    # 파일 이름 설정 (예: 일식.csv)
    file_name = f"{category}.xlsx - Sheet1.csv"
    backup_name = f"{category}.csv"
    
    if os.path.exists(file_name):
        final_file = file_name
    elif os.path.exists(backup_name):
        final_file = backup_name
    else:
        final_file = None

    if final_file is None:
        st.error(f"❌ '{category}' 파일을 찾을 수 없습니다.")
        st.info(f"💡 깃허브 저장소에 파일이 '{file_name}' 혹은 '{category}.csv' 이름으로 잘 올라갔는지 확인해 주세요!")
    else:
        with open(final_file, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)  # 헤더 건너뛰기
            menus = [row[0].strip() for row in reader if row and row[0].strip()]
        
        if menus:
            recommended_menu = random.choice(menus)
            st.success(f"오늘의 추천 메뉴는 바로 **[{recommended_menu}]** 입니다! 츄릅 😋")
        else:
            st.error(f"⚠️ {final_file} 파일 안에 저장된 메뉴가 없습니다.")
