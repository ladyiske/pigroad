import streamlit as st
import random
import csv
import os

# 1. 웹페이지 설정
st.set_page_config(page_title="돼지름길", page_icon="🐷", layout="centered")

# 🎨 [디자인 커스텀] HTML 구조 개편으로 이미지 위에 메뉴 겹치기
st.markdown(
    """
    <style>
    /* 전체 웹사이트 배경을 연핑크로 변경 */
    .stApp {
        background-color: #FFF0F2 !important;
    }
    
    /* 제목 및 부제목 스타일 */
    h1, h3 {
        color: #2B2B2B !important;
        text-align: center; 
    }
    
    /* ★ 돼지와 메뉴를 하나로 묶는 상대 위치 바구니 ★ */
    .pig-wrapper {
        position: relative;
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin-top: 20px;
        margin-bottom: -25px; /* 이름표와 밀착 */
    }
    
    /* 돼지 이미지 스타일 */
    .pig-wrapper img {
        display: block;
        max-width: 650px;
        width: 100%;
        height: auto;
    }
    
    /* ★ 돼지 입 앞(정중앙 부근)에 메뉴판을 절대 위치로 강제 고정 ★ */
    .mouth-menu-box {
        position: absolute;
        top: 50%;   /* 돼지 얼굴 중앙 높이 */
        left: 50%;  /* 화면 가로 중앙 */
        transform: translate(-50%, -40%); /* 입 위치에 오도록 세밀하게 조정 */
        z-index: 999; /* 이미지보다 무조건 앞에 보이게 세팅 */
        
        /* 대화상자/메뉴판 디자인 */
        background-color: #FFFFFF !important;
        border: 6px solid #FF6B8B !important;
        border-radius: 25px !important;
        padding: 20px 30px !important;
        box-shadow: 0px 12px 25px rgba(0, 0, 0, 0.2);
        min-width: 280px;
        text-align: center;
        
        /* 튀어나오는 애니메이션 */
        animation: mouthPop 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .mouth-menu-box h4 {
        margin: 0 0 8px 0 !important;
        color: #FF6B8B !important;
        font-size: 1.1rem !important;
    }
    
    .mouth-menu-box .menu-title {
        margin: 0 !important;
        font-size: 2rem !important; /* 메뉴 글자 왕 크게 */
        font-weight: bold !important;
        color: #2B2B2B !important;
    }
    
    /* 이름표 라벨 숨기기 */
    div[data-testid="stWidgetLabel"] p {
        display: none;
    }
    
    /* 선택창 상자를 어두운 핑크로 디자인 (이름표 느낌) */
    div[data-baseweb="select"] {
        border: 4px solid #FF6B8B !important;
        border-radius: 15px !important;
        background-color: #FF6B8B !important;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
    }
    
    /* 선택창 내부의 카테고리 글씨를 흰색 크고 굵게 */
    div[data-baseweb="select"] div {
        color: #FFFFFF !important; 
        font-size: 1.5rem !important;
        font-weight: bold !important;
        text-align: center;
    }
    
    /* 드롭다운 메뉴 스타일 */
    ul[role="listbox"] {
        background-color: #FFFFFF !important;
    }
    ul[role="listbox"] li {
        color: #2B2B2B !important;
        font-size: 1.2rem !important;
    }
    
    /* 주문하기 버튼 스타일 */
    .stButton {
        display: flex;
        justify-content: center;
        margin-top: 15px;
    }
    .stButton button {
        background-color: #2B2B2B !important;
        color: white !important;
        border-radius: 20px !important;
        padding: 0.6rem 3rem !important;
        border: none !important;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton button p {
        font-size: 1.3rem !important;
        font-weight: bold !important;
        color: white !important;
    }

    @keyframes mouthPop {
        0% { transform: translate(-50%, -40%) scale(0.3); opacity: 0; }
        100% { transform: translate(-50%, -40%) scale(1); opacity: 1; }
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

# --- 화면 레이아웃 구성 ---

# [메뉴 추천 먼저 연산] 돼지 입 위치에 텍스트를 바로 얹기 위해 데이터를 먼저 뽑습니다.
recommended_menu = None
error_message = None

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
        error_message = f"❌ '{current_cat}' 파일이 없습니다."
        st.session_state.clicked = False
    else:
        menus = []
        encodings = ["utf-8", "cp949", "utf-8-sig", "euc-kr"]
        success_read = False
        
        for enc in encodings:
            try:
                with open(final_file, mode="r", encoding=enc) as f:
                    reader = csv.reader(f)
                    raw_rows = [row[0].strip() for row in reader if row and row[0].strip()]
                    
                    if raw_rows:
                        if len(raw_rows) > 1 and raw_rows[0].lower() in ['menu', 'title', '이름', '메뉴']:
                            menus = raw_rows[1:]
                        else:
                            menus = raw_rows
                        success_read = True
                        break
            except UnicodeDecodeError:
                continue
        
        if success_read and menus:
            recommended_menu = random.choice(menus)
        else:
            error_message = f"⚠️ {final_file}의 메뉴를 읽지 못했습니다."
            st.session_state.clicked = False

# [위치 1] 돼지 이미지 공간 (버튼 클릭 시 입 앞에 메뉴판이 겹쳐서 생성됨!)
st.markdown('<div class="pig-wrapper">', unsafe_allow_html=True)

if st.session_state.clicked and recommended_menu:
    # 😮 입 벌린 돼지 출력
    if os.path.exists("pig_open.png"):
        st.image("pig_open.png")
    else:
        st.markdown("<div style='font-size: 220px;'>😮</div>", unsafe_allow_html=True)
    
    # ★ 핵심: 이미지 위에 절대 좌표로 메뉴 상자 얹어버리기 (입 앞 타겟팅) ★
    st.markdown(
        f"""
        <div class="mouth-menu-box">
            <h4>꿀꿀! 오늘의 메뉴</h4>
            <p class="menu-title">✨ {recommended_menu} ✨</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
else:
    # 😐 평소엔 입 다문 돼지 출력
    if os.path.exists("pig_closed.png"):
        st.image("pig_closed.png")
    else:
        st.markdown("<div style='font-size: 220px;'>😐</div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


# [위치 2] 돼지 목 밑에 자석처럼 붙는 이름표 (카테고리 선택창)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if error_message:
        st.error(error_message)
        
    current_idx = categories.index(st.session_state.selected_category)
    category = st.selectbox("", options=categories, index=current_idx)
    st.session_state.selected_category = category
    
    # 클릭 상태에 따라 버튼 글자 유동적 변경
    btn_label = "다시 고르기 🔄" if st.session_state.clicked else "주문하기! 🛎️"
    
    if st.button(btn_label):
        if st.session_state.clicked:
            st.session_state.clicked = False
        else:
            st.session_state.clicked = True
        st.rerun()
