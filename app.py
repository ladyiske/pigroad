import streamlit as st
import random
import csv
import os

# 1. 웹페이지 설정 (중앙 정렬)
st.set_page_config(page_title="돼지름길", page_icon="🐷", layout="centered")

# 🎨 [디자인 커스텀] 돼지 초대형화 및 레이아웃 밀착 세팅
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
    
    /* ★ 돼지 이미지 크기를 극대화하고 가운데 정렬 ★ */
    .pig-box {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-top: 10px;
        margin-bottom: -35px; /* 이름표 상자와 완벽하게 겹치도록 여백 당기기 */
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
    
    /* ★ 돼지 입 바로 밑에 매칭될 메뉴 결과창 (말풍선/팝업 스타일) ★ */
    div[data-testid="stNotification"] {
        background-color: #FFFFFF !important;
        border: 6px solid #FF6B8B !important;
        border-radius: 25px !important;
        padding: 25px !important;
        box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.15);
        margin-top: -20px; /* 돼지 입 위치와 가깝게 위로 당김 */
        animation: mouthPop 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275); /* 통통 튀는 애니메이션 */
    }
    
    div[data-testid="stNotification"] p {
        font-size: 2rem !important; /* 메뉴 글자 크기 대폭 확대! */
        font-weight: bold !important;
        color: #FF6B8B !important;
        text-align: center;
    }

    @keyframes mouthPop {
        0% { transform: scale(0.3); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 2. 상단 타이틀
st.title("🐷 돼지름길")
st.subheader("오늘 뭐 먹지? 고민 끝, 지름길로 가면돼지!")

# 3. 세션 상태 정의
categories = ["한식", "중식", "양식", "일식", "동남아", "디저트"]
if "clicked" not in st.session_state:
    st.session_state.clicked = False
if "selected_category" not in st.session_state:
    st.session_state.selected_category = "한식"

# --- 화면 레이아웃 구성 ---

# [위치 1] 화면을 압도하는 왕 돼지 배치 (width를 650으로 한 번 더 확대!)
st.markdown('<div class="pig-box">', unsafe_allow_html=True)
if st.session_state.clicked:
    if os.path.exists("pig_open.png"):
        st.image("pig_open.png", width=650)
    else:
        st.markdown("<div style='font-size: 220px;'>😮</div>", unsafe_allow_html=True)
else:
    if os.path.exists("pig_closed.png"):
        st.image("pig_closed.png", width=650)
    else:
        st.markdown("<div style='font-size: 220px;'>😐</div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# [위치 2] 돼지 목 밑에 자석처럼 붙는 이름표 (카테고리 선택창)
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    current_idx = categories.index(st.session_state.selected_category)
    category = st.selectbox("", options=categories, index=current_idx)
    st.session_state.selected_category = category
    
    if st.button("주문하기! 🛎️"):
        st.session_state.clicked = True
        st.rerun()

# [위치 3] 메뉴 추천 결과 (버튼 클릭 시 돼지 입 하단에 팝업 연출)
if st.session_state.clicked:
    current_cat = st.session_state.selected_category
    
    # 여러 파일 확장자 및 형식 자동 매칭
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
        encodings = ["utf-8", "cp949", "utf-8-sig", "euc-kr"]
        success_read = False
        
        for enc in encodings:
            try:
                with open(final_file, mode="r", encoding=enc) as f:
                    reader = csv.reader(f)
                    raw_rows = [row[0].strip() for row in reader if row and row[0].strip()]
                    
                    if raw_rows:
                        # 🔍 [에러 방지 치트키] 
                        # 첫 줄이 'menu' 같은 영어 제목이든 실제 음식이든 상관없이 다 가져오되, 
                        # 메뉴 리스트 길이가 2개 이상이면 첫 줄(헤더)을 제외하고 안전하게 가져옵니다.
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
            # 돼지 입 밑에 나타날 큰 팝업창
            st.markdown("<h3 style='text-align:center; color:#FF6B8B; margin-top:20px;'>꿀꿀! 입에서 튀어나온 메뉴!</h3>", unsafe_allow_html=True)
            st.success(f"✨ {recommended_menu} ✨")
        else:
            st.error(f"⚠️ {final_file} 파일 내부에서 메뉴 글씨를 읽지 못했습니다. 파일 내용을 확인해 주세요!")
        
        if st.button("다시 고르기 🔄"):
            st.session_state.clicked = False
            st.rerun()
