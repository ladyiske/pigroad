import streamlit as st
import random
import csv
import os

# 1. 웹페이지 설정
st.set_page_config(page_title="돼지름길", page_icon="🐷", layout="centered")

# 🎨 [디자인 커스텀] 배경 연핑크 + 카테고리 글씨 흰색 고정
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
    
    /* 돼지 이미지 스타일 (가운데 정렬) */
    .pig-box {
        display: flex;
        justify-content: center;
        margin: 20px 0;
    }
    
    /* 이름표 라벨 숨기기 */
    div[data-testid="stWidgetLabel"] p {
        display: none;
    }
    
    /* ★ 선택창 상자를 어두운 핑크로 만들어서 흰색 글씨가 잘 보이게 조절 ★ */
    div[data-baseweb="select"] {
        border: 3px solid #FF6B8B !important;
        border-radius: 15px !important;
        background-color: #FF6B8B !important; /* 배경을 진한 핑크로 */
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
    }
    
    /* ★ 선택창 내부의 '한식, 중식...' 글씨를 흰색으로 변경 ★ */
    div[data-baseweb="select"] div {
        color: #FFFFFF !important; 
        font-size: 1.3rem !important;
        font-weight: bold !important;
        text-align: center;
    }
    
    /* 드롭다운 메뉴가 아래로 열렸을 때의 스타일 */
    ul[role="listbox"] {
        background-color: #FFFFFF !important;
    }
    ul[role="listbox"] li {
        color: #2B2B2B !important; /* 펼쳐진 목록은 읽기 쉽게 어두운 색 */
        font-size: 1.2rem !important;
    }
    
    /* 주문하기 버튼 스타일 */
    .stButton {
        display: flex;
        justify-content: center;
        margin-top: 15px;
    }
    .stButton button {
        background-color: #2B2B2B !important; /* 버튼은 세련된 블랙 계열 */
        color: white !important;
        border-radius: 20px !important;
        padding: 0.6rem 2rem !important;
        border: none !important;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton button p {
        font-size: 1.2rem !important;
        font-weight: bold !important;
        color: white !important;
    }
    
    /* 결과창 디자인 및 팝업 애니메이션 */
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

# 3. 카테고리 정의 및 드롭다운 배치
categories = ["한식", "중식", "양식", "일식", "동남아", "디저트"]

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    category = st.selectbox("", options=categories)
    clicked = st.button("주문하기! 🛎️")

# 4. 버튼 클릭 여부에 따라 돼지 이미지 변환 및 결과 출력
if clicked:
    # 버튼 누르면 입 벌린 돼지 출력 시도
    st.markdown('<div class="pig-box">', unsafe_allow_html=True)
    if os.path.exists("pig_open.png"):
        st.image("pig_open.png", width=350)
    else:
        st.markdown("<div style='font-size: 120px; text-align: center;'>😮</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
        
    # 메뉴 추천 로직
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
            st.markdown("<h3 style='text-align:center; color:#FF6B8B;'>꿀꿀! 오늘의 추천 메뉴!</h3>", unsafe_allow_html=True)
            st.success(f"✨ {recommended_menu} ✨")
        else:
            st.error(f"⚠️ {final_file} 파일에 저장된 메뉴가 없습니다.")
            
else:
    # 평소에는 입 다문 돼지 출력 시도
    st.markdown('<div class="pig-box">', unsafe_allow_html=True)
    if os.path.exists("pig_closed.png"):
        st.image("pig_closed.png", width=350)
    else:
        st.markdown("<div style='font-size: 120px; text-align: center;'>😐</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
