import streamlit as st
import random
import csv
import os
import base64
import urllib.parse
import time
import streamlit.components.v1 as components

# =========================
# 1. 페이지 설정
# =========================
st.set_page_config(page_title="돼지름길", page_icon="🐷", layout="centered")

# =========================
# 2. 사운드
# =========================
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

# =========================
# 3. CSS 디자인
# =========================
st.markdown("""
<style>
html, body, .stApp {
    background: linear-gradient(135deg, #FFDEE9 0%, #B5FFFC 100%) !important;
}

h1, h3 { text-align:center; }

.pig-wrapper {
    display:flex;
    justify-content:center;
}

.mouth-menu-box {
    background:#fff;
    border:5px solid #FF6B8B;
    border-radius:20px;
    padding:15px;
    text-align:center;
    margin-top:-20px;
}

.btn {
    background:#2B2B2B;
    color:white;
    padding:10px 15px;
    border-radius:10px;
    text-decoration:none;
}
</style>
""", unsafe_allow_html=True)

# =========================
# 4. 타이틀
# =========================
st.title("🐷 돼지름길")
st.subheader("오늘 뭐 먹지? 고민 끝!")

# =========================
# 5. 상태 초기화
# =========================
categories = ["한식", "중식", "양식", "일식", "동남아", "디저트"]

if "clicked" not in st.session_state:
    st.session_state.clicked = False
if "selected_category" not in st.session_state:
    st.session_state.selected_category = "한식"
if "recommended_menu" not in st.session_state:
    st.session_state.recommended_menu = None
if "pig_comment" not in st.session_state:
    st.session_state.pig_comment = None

comment_pool = {
    "한식": ["꿀맛 한식!", "든든하다 꿀!", "집밥 최고!"],
    "중식": ["불맛 폭발!", "짜장 or 짬뽕 가자!", "기름지게 행복!"],
    "양식": ["고급진 선택!", "파스타 각이다!", "치즈폭발!"],
    "일식": ["깔끔한 선택!", "초밥 가자!", "정갈하다 꿀!"],
    "동남아": ["향신료 충전!", "이국적인 맛!", "쌀국수 ㄱㄱ"],
    "디저트": ["당 충전 완료!", "달달하다!", "행복 끝판왕!"]
}

# =========================
# 6. UI - 선택
# =========================
col1, col2, col3 = st.columns([1,2,1])

with col2:
    category = st.selectbox("", categories, index=categories.index(st.session_state.selected_category))

    if not st.session_state.clicked:
        st.session_state.selected_category = category

    if st.button("주문하기 🛎️"):
        trigger = True
    else:
        trigger = False

# =========================
# 7. 슬롯머신
# =========================
if trigger:
    menus = ["김치찌개", "된장찌개", "불고기", "짜장면", "파스타", "초밥", "쌀국수", "케이크"]

    slot = st.empty()

    for _ in range(10):
        temp = random.choice(menus)
        with slot.container():
            st.markdown(f"## 🌀 {temp}")
            st.image("pig_closed.png" if os.path.exists("pig_closed.png") else None)
        time.sleep(0.1)

    slot.empty()

    st.session_state.recommended_menu = random.choice(menus)
    st.session_state.pig_comment = random.choice(comment_pool[category])
    st.session_state.clicked = True
    st.rerun()

# =========================
# 8. 결과 출력
# =========================
if st.session_state.clicked and st.session_state.recommended_menu:

    play_sound("magic.mp3")

    st.image("pig_open.png" if os.path.exists("pig_open.png") else None)

    menu = st.session_state.recommended_menu
    comment = st.session_state.pig_comment

    share_text = f"🐷 돼지름길 추천!\n{menu}\n{comment}"

    naver_map_url = f"https://map.naver.com/v5/search/{urllib.parse.quote(menu)}"

    kakao_text = urllib.parse.quote(share_text + f"\n{naver_map_url}")
    kakao_link = f"https://sharer.kakao.com/talk/friends/picker/link?link={kakao_text}"

    # =========================
    # UI 박스
    # =========================
    st.markdown(f"""
    <div class="mouth-menu-box">
        <h3>🐷 오늘의 추천</h3>
        <h2>{menu}</h2>
        <p>{comment}</p>
        <a class="btn" href="{naver_map_url}" target="_blank">📍 맛집 보기</a>
    </div>
    """, unsafe_allow_html=True)

    # =========================
    # 🔥 클립보드 복사 (JS)
    # =========================
    components.html(f"""
        <textarea id="t" style="position:absolute;left:-9999px;">{share_text}</textarea>

        <button onclick="
            navigator.clipboard.writeText(document.getElementById('t').value);
            alert('복사 완료!');
        "
        style="
            margin-top:15px;
            background:#2B2B2B;
            color:white;
            padding:12px 18px;
            border:none;
            border-radius:12px;
            cursor:pointer;
        ">
            📋 복사하기
        </button>
    """, height=120)

    # =========================
    # 💛 카카오 공유 버튼
    # =========================
    components.html(f"""
        <div style="margin-top:10px;">
            <a href="{kakao_link}" target="_blank"
               style="
                    display:inline-block;
                    background:#FEE500;
                    color:#3A1D1D;
                    padding:12px 18px;
                    border-radius:12px;
                    text-decoration:none;
                    font-weight:bold;
               ">
                💬 카카오톡 공유
            </a>
        </div>
    """, height=80)

# =========================
# 9. 기본 돼지
# =========================
else:
    st.image("pig_closed.png" if os.path.exists("pig_closed.png") else None)
