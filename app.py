import streamlit as st
import random
import csv
import os
import base64

# 1. 웹페이지 설정
st.set_page_config(page_title="돼지름길", page_icon="🐷", layout="centered")

# 🔊 [사운드 함수] MP3 파일을 브라우저에서 자동 재생할 수 있도록 base64로 인코딩하는 함수
def play_sound(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""
                <audio autoplay style="display:none;">
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                """
            st.markdown(md, unsafe_allow_html=True)

# 🎨 [디자인 커스텀] 
st.markdown(
    """
    <style>
    .stApp { background-color: #FFF0F2 !important; }
    h1, h3 { color: #2B2B2B !important; text-align: center; }
    
    .pig-wrapper {
        position: relative;
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin-top: 10px;
        margin-bottom: -25px;
    }
    .pig-wrapper img {
        display: block;
        max-width: 650px;
        width: 100%;
        height: auto;
    }
    
    .mouth-menu-box {
        position: absolute;
        left: 50%;
        margin-left: -320px; 
        top: 0;
        margin-top: -340px; 
        z-index: 999; 
        background-color: #FFFFFF !important;
        border: 6px solid #FF6B8B !important;
        border-radius: 25px !important;
        padding: 20px 25px !important;
        box-shadow: -10px 12px 25px rgba(0, 0, 0, 0.15); 
        min-width: 250px;
        text-align: center;
        animation: mouthPop 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .mouth-menu-box h4 { margin: 0 0 8px 0 !important; color: #FF6B8B !important; font-size: 1.1rem !important; }
    .mouth-menu-box .menu-title { margin: 0 !important; font-size: 1.8rem !important; font-weight: bold !important; color: #2B2B2B !important; }
    
    div[data-testid="stWidgetLabel"] p { display: none; }
    
    div[data-baseweb="select"] {
        border: 4px solid #FF6B8B !important;
        border-radius: 15px !important;
        background-color: #FF6B8B !important;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        min-height: 55px !important;
    }
    div[data-baseweb="select"] div {
        color: #FFFFFF !important; 
        font-size: 1.4rem !important;
        font-weight: bold !important;
        text-align: center;
        line-height: 1.5 !important;
        overflow: visible !important;
    }
    ul[role="listbox"] { background-color: #FFFFFF !important; }
    ul[role="listbox"] li { color: #2B2B2B !important; font-size: 1.2rem !important; }
    
    .stButton { display: flex; justify-content: center; margin-top: 15px; }
    .stButton button {
        background-color: #2B2B2B !important;
        color: white !important;
        border-radius: 20px !important;
        padding: 0.6rem 3rem !important;
        border: none !important;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton button p { font-size: 1.3rem !important; font-weight: bold !important; color: white !important; }
    @keyframes mouthPop { 0% { transform: scale(0.3); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }
    </style>
    """,
    unsafe_allow_html=True
)

# 2. 상단 타이틀
st.title("🐷 돼지름길")
st.subheader("오늘 뭐 먹지? 고민 끝, 지름길로 가면 돼지!")

# 3. 세션 상태 정의
categories = ["한식", "중식", "양식", "일식", "동남아", "디저트"]
if "clicked" not in st.session_state:
    st.session_state.clicked = False
if "selected_category" not in st.session_state:
    st.session_state.selected_category = "한식"
if "recommended_menu" not in st.session_state:
    st.session_state.recommended_menu = None

error_message = None

# --- 이름표 및 카테고리 선택부 ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    current_idx = categories.index(st.session_state.selected_category)
    category = st.selectbox("", options=categories, index=current_idx)
    if not st.session_state.clicked:
        st.session_state.selected_category = category

    if st.session_state.clicked:
        if st.button("다시 고르기 🔄"):
            st.session_state.clicked = False
            st.session_state.recommended_menu = None
            st.rerun()
    else:
        if st.button("주문하기! 🛎️"):
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
                    st.session_state.recommended_menu = random.choice(menus)
                    st.session_state.clicked = True
                    st.rerun()
                else:
                    error_message = f"⚠️ {final_file}의 메뉴를 읽지 못했습니다."

    if error_message:
        st.error(error_message)

# --- 돼지 이미지 및 말풍선 오버레이 공간 ---
st.markdown('<div class="pig-wrapper">', unsafe_allow_html=True)

if st.session_state.clicked and st.session_state.recommended_menu:
    # ★ 저장하신 파일명 'magic.mp3' 혹은 'magic.wav' 등 확장자에 맞춰 지정해 줍니다.
    # 만약 확장자가 wav라면 "magic.wav"로 변경해 주세요!
    play_sound("magic.mp3")
    
    if os.path.exists("pig_open.png"):
        st.image("pig_open.png")
    else:
        st.markdown("<div style='font-size: 220px;'>😮</div>", unsafe_allow_html=True)
    
    st.markdown(
        f"""
        <div class="mouth-menu-box">
            <h4>돼지름신의 추천! 냠냠</h4>
            <p class="menu-title">✨ {st.session_state.recommended_menu} ✨</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
else:
    if os.path.exists("pig_closed.png"):
        st.image("pig_closed.png")
    else:
        st.markdown("<div style='font-size: 220px;'>😐</div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
