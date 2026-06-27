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
    }
    
    .pig-wrapper { position: relative; display: flex; justify-content: center; align-items: center; width: 100%; margin-top: 10px; }
    .pig-wrapper img { display: block; max-width: 500px; width: 100%; height: auto; }
    
    .mouth-menu-box {
        background-color: #FFFFFF !important; border: 6px solid #FF6B8B !important; border-radius: 25px !important;
        padding: 20px 25px !important; box-shadow: -10px 12px 25px rgba(0, 0, 0, 0.15); 
        text-align: center; margin: 20px auto; max-width: 350px;
    }
    
    /* ★ 복사 버튼 위치 조정: margin-top 값을 더 음수로 주어 위로 올림 ★ */
    .right-share-box { 
        position: relative; 
        margin-top: -380px !important; 
        z-index: 1000;
    }
    .right-share-box button {
        background-color: #FF6B8B !important; color: white !important;
        border-radius: 15px !important; padding: 15px 25px !important;
        font-weight: bold !important; border: none !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2) !important;
    }
    
    /* ★ 코드 블록 크기 강화 ★ */
    pre { font-size: 1.2rem !important; padding: 20px !important; background: #FFF0F2 !important; border: 2px solid #FF6B8B !important; }
    </style>
    """,
    unsafe_allow_html=True
)

# 세션 및 로직 초기화
if "clicked" not in st.session_state: st.session_state.clicked = False

st.title("🐷 돼지름길")

if st.session_state.clicked and st.session_state.recommended_menu:
    share_text = f"🐷 오늘의 추천 메뉴: {st.session_state.recommended_menu}!"
    
    # 말풍선
    st.markdown(f"""
        <div class="mouth-menu-box">
            <h3>오늘의 추천!</h3>
            <p style="font-size: 1.8rem; font-weight: bold;">✨ {st.session_state.recommended_menu} ✨</p>
        </div>
    """, unsafe_allow_html=True)
    
    # 돼지 + 버튼을 한 줄로 배치
    c1, c2 = st.columns([2, 1])
    with c1:
        st.image("pig_open.png" if os.path.exists("pig_open.png") else "https://via.placeholder.com/400")
    with c2:
        st.markdown('<div class="right-share-box">', unsafe_allow_html=True)
        if st.button("📋 결과 복사"):
            st.code(share_text, language="")
            st.toast("복사되었습니다!")
        st.markdown('</div>', unsafe_allow_html=True)
        
    if st.button("🔄 다시 고르기"):
        st.session_state.clicked = False
        st.rerun()

else:
    # 초기 화면
    if st.button("주문하기! 🛎️"):
        st.session_state.recommended_menu = "설렁탕"
        st.session_state.clicked = True
        st.rerun()
    st.image("pig_closed.png" if os.path.exists("pig_closed.png") else "https://via.placeholder.com/400")
