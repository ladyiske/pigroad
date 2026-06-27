import streamlit as st
import random
import csv
import os

# 1. 웹페이지 설정
st.set_page_config(page_title="돼지름길", page_icon="🐷", layout="centered")

# 🎨 [강력한 디자인 커스텀] 글자색 완전 검은색 계열로 고정 및 크기 확대
st.markdown(
    """
    <style>
    /* 1. 전체 웹사이트 배경을 연핑크로 변경 */
    .stApp {
        background-color: #FFF0F2 !important;
    }
    
    /* 2. 제목(H1), 부제목(H3)을 포함한 전체 텍스트 색상을 어두운 색으로 강제 고정 */
    h1, h2, h3, p, label, span, li {
        color: #2B2B2B !important;
    }
    
    /* 3. "원하는 음식 종류를 선택하세요" 라벨 글자 크기 키우기 */
    div[data-testid="stWidgetLabel"] p {
        font-size: 1.4rem !important;
        font-weight: bold !important;
        color: #2B2B2B !important;
    }
    
    /* 4. 선택창(Selectbox) 내부 글자색을 어두운 색으로 강제 지정 (★가장 중요★) */
    div[data-baseweb="select"] div {
        color: #2B2B2B !important;
        font-size: 1.2rem !important;
        font-weight: 500 !important;
    }
    
    /* 드롭다운 아래로 열렸을 때 나오는 항목들의 글자색도 고정 */
    ul[role="listbox"] li {
        color: #2B2B2B !important;
        font-size: 1.1rem !important;
    }
    
    /* 5. 추천받기 버튼 스타일 변경 (크기 키우고 글자 진하게) */
    .stButton button {
        background-color: #FF6B8B !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
    }
    .stButton button p {
        font-size: 1.3rem !important;
        font-weight: bold !important;
        color: white !important; /* 버튼 글자는 흰색이 잘 보여서 흰색 고정 */
    }
    
    /* 6. 결과 메시지(초록색 박스) 안의 글자 크기 대폭 확대 */
    div[data-testid="stNotification"] p {
        font-size: 1.6rem !important;
        font-weight: bold !important;
        color: #1E4620 !important; /* 결과창 안의 글씨는 진한 초록색 */
        line-height: 1.6 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 2. 타이틀 및 서브타이틀
st.title("🐷 돼지름길")
st.subheader("오늘 뭐 먹지? 고민 끝, 지름길로 가세요!")

# 3. 카테고리 정의
categories = ["한식", "중식", "양식", "일식", "동남아", "디저트"]

# 4. 사용자 선택 UI
category = st.selectbox("원하는 음식 종류를 선택하세요:", options=categories)

# 5. 버튼 클릭 감지
clicked = st.button(f"{category} 메뉴 추천받기 ✨")

if clicked:
    # 파일 이름 설정
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
    else:
        with open(final_file, mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader)  # 헤더 건너뛰기
            menus = [row[0].strip() for row in reader if row and row[0].strip()]
        
        if menus:
            recommended_menu = random.choice(menus)
            # 성공 결과창
            st.success(f"오늘의 추천 메뉴는 바로 **[{recommended_menu}]** 입니다! 😋")
        else:
            st.error(f"⚠️ {final_file} 파일 안에 저장된 메뉴가 없습니다.")
