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

# 4. 버튼 클릭 감지
clicked = st.button(f"{category} 메뉴 추천받기 ✨")

if clicked:
    # 파일 이름 설정 (예: 일식.csv)
    file_name = f"{category}.csv"
    
    # 윈도우 환경에서 대문자 .CSV로 저장되는 경우도 대비
    file_name_upper = f"{category}.CSV"
    
    # 실제 존재하는 파일명 선택
    if os.path.exists(file_name):
        final_file = file_name
    elif os.path.exists(file_name_upper):
        final_file = file_name_upper
    else:
        final_file = None

    # 파일이 없는 경우 에러 처리
    if final_file is None:
        st.error(f"❌ '{file_name}' 파일을 찾을 수 없습니다.")
        st.info("💡 깃허브(GitHub) 저장소에 파일이 'app.py'와 같은 위치에 잘 올라갔는지, 파일 이름에 띄어쓰기가 포함되어 있지는 않은지 확인해 주세요!")
    else:
        # 파일 읽기
        with open(final_file, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            
            # 첫 번째 줄(헤더: menu) 건너뛰기
            try:
                next(reader)
            except StopIteration:
                pass # 파일이 비어있을 경우 대비
                
            # 공백을 제외한 메뉴명만 리스트로 담기
            menus = [row[0].strip() for row in reader if row and row[0].strip()]
        
        # 메뉴가 정상적으로 들어있다면 무작위 추천
        if menus:
            recommended_menu = random.choice(menus)
            st.success(f"오늘의 추천 메뉴는 바로 **[{recommended_menu}]** 입니다! 츄릅 😋")
        else:
            st.error(f"⚠️ {category}.csv 파일 안에 저장된 메뉴가 없습니다. 파일을 확인해 주세요.")
