import streamlit as st
import random
import csv
import os

# 1. 웹페이지 설정
st.set_page_config(page_title="돼지름길", page_icon="🐷", layout="centered")

# 🎨 [디자인 커스텀]
st.markdown(
    """
    <style>
    .stApp {
        background-color: #FFF0F2 !important;
    }
    h1, h3 {
        color: #2B2B2B !important;
        text-align: center; 
    }
    .pig-box {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 30px;
        margin-bottom: -25px;
    }
    div[data-testid="stWidgetLabel"] p {
        display: none;
    }
    div[data-baseweb="select"] {
        border: 4px solid #FF6B8B !important;
        border-radius: 15px !important;
        background-color: #FF6B8B !important;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
    }
    div[data-baseweb="select"] div {
        color: #FFFFFF !important; 
        font-size: 1.4rem !important;
        font-weight: bold !important;
        text-align: center;
    }
    ul[role="listbox"] {
        background-color: #FFFFFF !important;
    }
    ul[role="listbox"] li {
        color: #2B2B2B !important;
        font-size: 1.2rem !important;
    }
    .stButton {
        display: flex;
        justify-content: center;
        margin-top: 15px;
    }
    .stButton button {
        background-color: #2B2B2B !important;
        color: white !important;
        border-radius: 20px !important;
        padding: 0.6rem 2.5rem !important;
        border: none !important;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton button p {
        font-size: 1.3rem !important;
        font-weight: bold !important;
        color: white !important;
    }
    div[data-testid="stNotification"] {
        background-color: #FFFFFF !important;
        border: 5px solid #FF6B8B !important;
        border-radius: 25px !important;
        padding: 20px !important;
        box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.15);
        animation: popUp 0.4s ease-out;
    }
    div[data-testid="stNotification"] p {
        font-size: 1.8rem !important;
        font-weight: bold !important;
        color: #FF6B8B !important;
    }
    @keyframes popUp {
        0% { transform: scale(0.5); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 2. 상단 타이틀
st.title("🐷 돼지름길")
st.subheader("오늘 뭐 먹지? 고민 끝, 지름길로 가세요!")

# 3. 세션 상태 정의
categories = ["한식", "중식", "양식", "일식", "동남아", "디저트"]
if "clicked" not in st.session_state:
    st.session_state.clicked = False
if "selected_category" not in st.session_state:
    st.session_state.selected_category = "한식"

# --- 화면 출력부 ---

# [위치 1] 대형 돼지 배치
st.markdown('<div class="pig-box">', unsafe_allow_html=True)
if st.session_state.clicked:
    if os.path.exists("pig_open.png"):
        st.image("pig_open.png", width=500)
    else:
        st.markdown("<div style='font-size: 180px;'>😮</div>", unsafe_allow_html=True)
else:
    if os.path.exists("pig_closed.png"):
        st.image("pig_closed.png", width=500)
    else:
        st.markdown("<div style='font-size: 180px;'>😐</div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# [위치 2] 이름표 (카테고리 선택창)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    current_idx = categories.index(st.session_state.selected_category)
    category = st.selectbox("", options=categories, index=current_idx)
    st.session_state.selected_category = category
    
    if st.button("주문하기! 🛎️"):
        st.session_state.clicked = True
        st.rerun()

# [위치 3] 메뉴 추천 결과 출력
if st.session_state.clicked:
    current_cat = st.session_state.selected_category
    
    file_candidates = [
        f"{current_cat}.xlsx - Sheet1.csv",
        f"{current_cat}.csv",
        f"{current_cat}.xlsx"
    ]
    
    final_file = None
    for candidate in file_candidates:
        if os.path.exists(candidate):
            final_file = candidate
            break

    if final_file is None:
        st.error(f"❌ 깃허브에 '{current_cat}' 관련 파일이 없습니다.")
        st.session_state.clicked = False
    else:
        menus = []
        # 🔍 [핵심 수정] 다양한 인코딩 형식을 순서대로 시도하여 깨짐 방지
        encodings = ["utf-8", "cp949", "utf-8-sig", "euc-kr"]
        success_read = False
        
        for enc in encodings:
            try:
                with open(final_file, mode="r", encoding=enc) as f:
                    reader = csv.reader(f)
                    next(reader, None)  # 헤더 건너뛰기
                    menus = [row[0].strip() for row in reader if row and row[0].strip()]
                success_read = True
                break  # 성공하면 시도 종료
            except UnicodeDecodeError:
                continue  # 에러 나면 다음 인코딩 시도
        
        if success_read and menus:
            recommended_menu = random.choice(menus)
            st.markdown("<h3 style='text-align:center; color:#FF6B8B; margin-top:25px;'>꿀꿀! 입에서 나온 추천 메뉴!</h3>", unsafe_allow_html=True)
            st.success(f"✨ {recommended_menu} ✨")
        else:
            st.error(f"⚠️ {final_file} 파일을 읽을 수 없거나 저장된 메뉴가 없습니다.")
        
        if st.button("다시 고르기 🔄"):
            st.session_state.clicked = False
            st.rerun()
