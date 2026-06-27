iimport streamlit as st
import random
import csv
import os
import base64
import urllib.parse
import time

# 1. 웹페이지 설정
st.set_page_config(page_title="돼지름길", page_icon="🐷", layout="centered")

# 🔊 [사운드 함수]
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
    html, body, [data-testid="stAppViewContainer"], .stApp { 
        background: 
            linear-gradient(90deg, rgba(255,255,255,0.4) 1px, transparent 1px),
            linear-gradient(rgba(255,255,255,0.4) 1px, transparent 1px),
            linear-gradient(135deg, #FFDEE9 0%, #B5FFFC 100%) !important;
        background-size: 40px 40px, 40px 40px, auto !important;
        position: relative;
        overflow-x: hidden;
    }
    
    h1, h3 { color: #2B2B2B !important; text-align: center; position: relative; z-index: 10; }
    h1 { text-shadow: 0px 4px 10px rgba(255, 255, 255, 0.6); }

    /* ⭐ 추천 박스 글자색 강제 */
    .result-box h2, .result-box h3 {
        color: #2B2B2B !important;
    }
    
    .food-sticker { position: fixed; font-size: 3.5rem; opacity: 0.8; user-select: none; pointer-events: none; z-index: 1; }
    .fs-1 { left: 4%; top: 15%; animation: floatSticker1 4s ease-in-out infinite alternate; }
    .fs-2 { left: 5%; top: 45%; animation: floatSticker2 5s ease-in-out infinite alternate; }
    .fs-3 { left: 3%; top: 75%; animation: floatSticker1 4.5s ease-in-out infinite alternate; }
    .fs-4 { right: 4%; top: 18%; animation: floatSticker2 4.2s ease-in-out infinite alternate; }
    .fs-5 { right: 6%; top: 48%; animation: floatSticker1 4.8s ease-in-out infinite alternate; }
    .fs-6 { right: 3%; top: 78%; animation: floatSticker2 5.2s ease-in-out infinite alternate; }

    @keyframes floatSticker1 { 0% { transform: translateY(0) rotate(-5deg); } 100% { transform: translateY(-15px) rotate(10deg); } }
    @keyframes floatSticker2 { 0% { transform: translateY(0) rotate(8deg); } 100% { transform: translateY(-20px) rotate(-8deg); } }

    .pig-wrapper { display:flex; justify-content:center; align-items:center; margin-top:10px; margin-bottom:-25px; }
    .pig-wrapper img { max-width:650px; width:100%; }

    .stButton button { background-color:#2B2B2B !important; color:white !important; border-radius:20px !important; }
    </style>

    <div class="food-sticker fs-1">🍗</div>
    <div class="food-sticker fs-2">🍔</div>
    <div class="food-sticker fs-3">🍲</div>
    <div class="food-sticker fs-4">🍣</div>
    <div class="food-sticker fs-5">🍕</div>
    <div class="food-sticker fs-6">🍰</div>
    """,
    unsafe_allow_html=True
)

# 2. 타이틀
st.title("🐷 돼지름길")
st.subheader("오늘 뭐 먹지? 고민 끝, 지름길로 가면 돼지!")

# 3. 상태
categories = ["한식", "중식", "양식", "일식", "동남아", "디저트"]

if "clicked" not in st.session_state:
    st.session_state.clicked = False
if "selected_category" not in st.session_state:
    st.session_state.selected_category = "한식"
if "recommended_menu" not in st.session_state:
    st.session_state.recommended_menu = None

# 4. UI
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    current_idx = categories.index(st.session_state.selected_category)
    category = st.selectbox("", categories, index=current_idx)

    if not st.session_state.clicked:
        st.session_state.selected_category = category

    if not st.session_state.clicked:
        if st.button("주문하기! 🛎️"):
            trigger = True
    else:
        if st.button("다시 고르기 🔄"):
            st.session_state.clicked = False
            st.session_state.recommended_menu = None
            st.rerun()
        trigger = False

# 5. 추천 결과
if 'trigger' in locals() and trigger:
    menus = ["김치찌개", "불고기", "짜장면", "파스타", "초밥"]
    st.session_state.recommended_menu = random.choice(menus)
    st.session_state.clicked = True
    st.rerun()

# 6. 결과 출력 (⭐ 여기 핵심 수정)
if st.session_state.clicked and st.session_state.recommended_menu:
    play_sound("magic.mp3")

    st.markdown(f"""
    <div class="result-box" style="
        background:white;
        border:5px solid #FF6B8B;
        border-radius:20px;
        padding:20px;
        text-align:center;
        margin:0 auto;
        max-width:400px;
        color:#2B2B2B;
    ">
        <h3>오늘의 추천!</h3>
        <h2>✨ {st.session_state.recommended_menu} ✨</h2>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        if os.path.exists("pig_open.png"):
            st.image("pig_open.png", use_container_width=True)

    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)

        if st.button("📋 결과 복사"):
            st.code(f"🐷 오늘의 메뉴: {st.session_state.recommended_menu}")
            st.toast("복사됨!")

        if st.button("🔄 다시 고르기"):
            st.session_state.clicked = False
            st.rerun()
