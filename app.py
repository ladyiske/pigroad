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
    .mouth-menu-box {
        background-color: #FFFFFF !important; border: 6px solid #FF6B8B !important; 
        border-radius: 25px !important; padding: 20px !important; 
        box-shadow: 0px 10px 20px rgba(0,0,0,0.1); text-align: center; margin: 20px auto;
        max-width: 400px;
    }
    .map-btn {
        display: inline-block; background-color: #03C75A !important; color: white !important;
        border-radius: 12px !important; padding: 10px 20px !important; font-weight: bold !important; text-decoration: none;
    }
    /* 버튼을 돼지 옆으로 올리기 위한 스타일 */
    .pig-btn-container { margin-top: -150px; }
    </style>
""", unsafe_allow_html=True)

st.title("🐷 돼지름길")
st.subheader("오늘 뭐 먹지? 고민 끝, 지름길로 가세요!")

# 상태 초기화
if "clicked" not in st.session_state: st.session_state.clicked = False
if "selected_category" not in st.session_state: st.session_state.selected_category = "한식"

# --- 결과 출력 구간 ---
if st.session_state.clicked and st.session_state.recommended_menu:
    play_sound("magic.mp3")
    
    # 1. 말풍선 출력
    st.markdown(f"""
        <div class="mouth-menu-box">
            <h4>오늘의 추천! 냠냠</h4>
            <p style="font-size: 1.8rem; font-weight: bold;">✨ {st.session_state.recommended_menu} ✨</p>
            <a href="https://map.naver.com/v5/search/{urllib.parse.quote(st.session_state.recommended_menu)}" target="_blank" class="map-btn">📍 주변 맛집</a>
        </div>
    """, unsafe_allow_html=True)
    
    # 2. 돼지(왼쪽) + 버튼(오른쪽) 나란히 배치
    col_img, col_btn = st.columns([2, 1])
    
    with col_img:
        st.image("pig_open.png" if os.path.exists("pig_open.png") else "https://via.placeholder.com/400")
        
    with col_btn:
        # 버튼을 돼지 옆으로 끌어올리는 컨테이너
        st.markdown('<div class="pig-btn-container">', unsafe_allow_html=True)
        if st.button("📋 복사"):
            st.code(f"오늘의 메뉴: {st.session_state.recommended_menu}")
            st.toast("복사되었습니다!")
        st.markdown('</div>', unsafe_allow_html=True)
        
    if st.button("🔄 다시 고르기"):
        st.session_state.clicked = False
        st.rerun()

else:
    # --- 초기 선택 화면 ---
    category = st.selectbox("카테고리 선택", ["한식", "중식", "양식", "일식", "동남아", "디저트"])
    if st.button("주문하기! 🛎️"):
        st.session_state.recommended_menu = "설렁탕" # 예시 데이터
        st.session_state.clicked = True
        st.rerun()
    st.image("pig_closed.png" if os.path.exists("pig_closed.png") else "https://via.placeholder.com/400")
