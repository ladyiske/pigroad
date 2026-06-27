import streamlit as st
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
            st.markdown(f'<audio autoplay style="display:none;"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>', unsafe_allow_html=True)

# 🎨 [디자인 커스텀]
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] { 
        background: linear-gradient(135deg, #FFDEE9 0%, #B5FFFC 100%) !important; 
    }
    .pig-wrapper { display: flex; justify-content: center; align-items: center; margin-top: 20px; }
    .mouth-menu-box {
        background-color: #FFFFFF !important; border: 6px solid #FF6B8B !important; 
        border-radius: 25px !important; padding: 20px !important; 
        box-shadow: 0px 10px 20px rgba(0,0,0,0.1); text-align: center; margin-bottom: 20px;
    }
    .map-btn {
        display: inline-block; background-color: #03C75A !important; color: white !important;
        border-radius: 12px !important; padding: 10px 20px !important; font-weight: bold !important; text-decoration: none;
    }
    .copy-btn-area { display: flex; flex-direction: column; justify-content: center; align-items: center; height: 300px; }
    </style>
""", unsafe_allow_html=True)

st.title("🐷 돼지름길")

# 상태 초기화
if "clicked" not in st.session_state: st.session_state.clicked = False
if "recommended_menu" not in st.session_state: st.session_state.recommended_menu = None

# --- 로직 ---
if st.session_state.clicked and st.session_state.recommended_menu:
    # 1. 말풍선
    st.markdown(f"""
        <div class="mouth-menu-box">
            <h3 style="color:#FF6B8B;">오늘의 추천!</h3>
            <p style="font-size: 1.5rem; font-weight:bold;">✨ {st.session_state.recommended_menu} ✨</p>
            <a href="https://map.naver.com/v5/search/{urllib.parse.quote(st.session_state.recommended_menu)}" target="_blank" class="map-btn">📍 주변 맛집</a>
        </div>
    """, unsafe_allow_html=True)
    
    # 2. 돼지(왼쪽) + 복사버튼(오른쪽) 나란히 배치
    col_img, col_btn = st.columns([2, 1])
    with col_img:
        st.image("pig_open.png" if os.path.exists("pig_open.png") else "https://via.placeholder.com/400")
    with col_btn:
        st.markdown('<div class="copy-btn-area">', unsafe_allow_html=True)
        if st.button("📋 결과 복사"):
            st.code(f"오늘의 메뉴: {st.session_state.recommended_menu}")
            st.toast("복사되었습니다!")
        st.markdown('</div>', unsafe_allow_html=True)
        
    if st.button("🔄 다시 고르기"):
        st.session_state.clicked = False
        st.rerun()

else:
    # 3. 메인 화면
    category = st.selectbox("카테고리 선택", ["한식", "중식", "양식", "일식", "동남아", "디저트"])
    if st.button("주문하기! 🛎️"):
        st.session_state.recommended_menu = "설렁탕" # 테스트용
        st.session_state.clicked = True
        st.rerun()
    st.image("pig_closed.png" if os.path.exists("pig_closed.png") else "https://via.placeholder.com/400")
