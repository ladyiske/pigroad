import streamlit as st
import random
import os
import urllib.parse

# 1. 페이지 설정
st.set_page_config(page_title="돼지름길", layout="centered")

st.title("🐷 돼지름길")

# 상태 초기화
if "clicked" not in st.session_state: st.session_state.clicked = False

# --- 결과 출력 및 입력 로직 ---
if st.session_state.clicked:
    # 1. 말풍선 영역 (가운데 정렬)
    st.markdown(f"""
        <div style="background: white; border: 5px solid #FF6B8B; border-radius: 20px; padding: 20px; text-align: center; margin-bottom: 20px;">
            <h3>오늘의 추천!</h3>
            <h2>✨ {st.session_state.recommended_menu} ✨</h2>
            <a href="https://map.naver.com/v5/search/{urllib.parse.quote(st.session_state.recommended_menu)}" target="_blank" 
               style="background: #03C75A; color: white; padding: 10px 20px; border-radius: 10px; text-decoration: none; font-weight: bold;">
               📍 주변 맛집
            </a>
        </div>
    """, unsafe_allow_html=True)
    
    # 2. 돼지와 버튼 나란히 배치 (가장 확실한 방법)
    # 전체를 2:1 비율로 나누고, 중앙 정렬을 위해 div 컨테이너 사용
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.image("pig_open.png" if os.path.exists("pig_open.png") else "https://via.placeholder.com/400")
        
    with col_right:
        # 버튼을 위에서 아래로 내리기 위한 여백 (돼지 얼굴 높이 맞춤)
        st.write("<br><br><br>", unsafe_allow_html=True)
        if st.button("📋 결과 복사"):
            st.code(f"오늘의 메뉴: {st.session_state.recommended_menu}")
            st.toast("복사되었습니다!")
            
    if st.button("🔄 다시 고르기"):
        st.session_state.clicked = False
        st.rerun()

else:
    # 초기 화면
    category = st.selectbox("카테고리 선택", ["한식", "중식", "양식", "일식", "동남아", "디저트"])
    if st.button("주문하기! 🛎️"):
        st.session_state.recommended_menu = "오코노미야키" # 예시
        st.session_state.clicked = True
        st.rerun()
    st.image("pig_closed.png" if os.path.exists("pig_closed.png") else "https://via.placeholder.com/400")
