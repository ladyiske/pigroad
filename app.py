import streamlit as st
import random
import csv
import os
import base64
import time

st.set_page_config(page_title="돼지름길", page_icon="🐷", layout="centered")

# 🔊 사운드
def play_sound(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            st.markdown(f"""
                <audio autoplay style="display:none;">
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
            """, unsafe_allow_html=True)

# 🎨 UI (격자 + 스타일 + hover 수정 포함)
st.markdown("""
<style>

/* 🔥 격자 배경 복구 */
.stApp {
    background:
        linear-gradient(90deg, rgba(255,255,255,0.4) 1px, transparent 1px),
        linear-gradient(rgba(255,255,255,0.4) 1px, transparent 1px),
        linear-gradient(135deg, #FFDEE9 0%, #B5FFFC 100%) !important;
    background-size: 40px 40px, 40px 40px, auto !important;
}

/* 타이틀 */
h1, h3 {
    color:#2B2B2B !important;
    text-align:center;
}

/* 🐷 스티커 복구 */
.food-sticker {
    position: fixed;
    font-size: 3rem;
    opacity: 0.8;
    z-index: 1;
    pointer-events: none;
}

.fs1 {left:5%; top:15%;}
.fs2 {left:6%; top:45%;}
.fs3 {left:4%; top:75%;}
.fs4 {right:5%; top:20%;}
.fs5 {right:6%; top:50%;}
.fs6 {right:4%; top:80%;}

/* 버튼 hover 문제 해결 */
.stButton button {
    background-color:#2B2B2B !important;
    color:white !important;
    border-radius:20px !important;
    transition: all 0.2s ease-in-out;
}

.stButton button:hover {
    background-color:#444 !important;
    color:white !important;
    transform: scale(1.03);
}

/* 결과 박스 */
.result-box {
    background:white;
    border:5px solid #FF6B8B;
    border-radius:20px;
    padding:20px;
    text-align:center;
    max-width:420px;
    margin:0 auto;
}

.result-box h2, .result-box h3 {
    color:#2B2B2B !important;
}

</style>

<!-- 🐷 스티커 -->
<div class="food-sticker fs1">🍗</div>
<div class="food-sticker fs2">🍔</div>
<div class="food-sticker fs3">🍲</div>
<div class="food-sticker fs4">🍣</div>
<div class="food-sticker fs5">🍕</div>
<div class="food-sticker fs6">🍰</div>
""", unsafe_allow_html=True)

# 🐷 제목
st.title("돼지름길 🐷")
st.subheader("오늘 뭐 먹지? 고민 끝!")

# 📦 상태
categories = ["한식","중식","양식","일식","동남아","디저트"]

comment_pool = {
    "한식": ["역시 한식이 진리 꿀!", "든든한 선택이다 꿀!"],
    "중식": ["불맛 충전 가자 꿀!", "중식은 실패 없다 꿀!"],
    "양식": ["풍미 폭발 꿀!", "기분 내기 좋은 선택 꿀!"],
    "일식": ["깔끔하게 가자 꿀!", "정갈한 맛 꿀!"],
    "동남아": ["향신료 치트키 꿀!", "중독성 있는 맛 꿀!"],
    "디저트": ["당 충전 완료 꿀!", "행복해지는 선택 꿀!"]
}

if "clicked" not in st.session_state:
    st.session_state.clicked = False
if "selected_category" not in st.session_state:
    st.session_state.selected_category = "한식"
if "menu" not in st.session_state:
    st.session_state.menu = None

# UI
col1, col2, col3 = st.columns([1,2,1])

with col2:
    idx = categories.index(st.session_state.selected_category)
    cat = st.selectbox("", categories, index=idx)

    if not st.session_state.clicked:
        st.session_state.selected_category = cat

    if not st.session_state.clicked:
        trigger = st.button("주문하기 🛎️")
    else:
        trigger = False
        if st.button("다시 고르기 🔄"):
            st.session_state.clicked = False
            st.rerun()

# 🍱 슬롯
if trigger:
    file = f"{st.session_state.selected_category}.csv"

    if not os.path.exists(file):
        st.error("파일 없음")
    else:
        with open(file, "r", encoding="utf-8") as f:
            menus = [row[0] for row in csv.reader(f) if row]

        for i in range(10):
            temp = random.choice(menus)
            st.markdown(f"<h2 style='text-align:center;color:#FF6B8B'>🌀 {temp}</h2>", unsafe_allow_html=True)
            time.sleep(0.08)

        st.session_state.menu = random.choice(menus)
        st.session_state.clicked = True
        st.rerun()

# 🎯 결과
if st.session_state.clicked:

    play_sound("magic.mp3")

    st.markdown(f"""
    <div class="result-box">
        <h3>오늘의 추천</h3>
        <h2>✨ {st.session_state.menu} ✨</h2>
        <p>{random.choice(comment_pool[st.session_state.selected_category])}</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2,1])

    with col1:
        if os.path.exists("pig_open.png"):
            st.image("pig_open.png", use_container_width=True)

    with col2:
        if st.button("📋 복사"):
            st.code(f"🐷 오늘 메뉴: {st.session_state.menu}")
            st.toast("복사됨!")

        if st.button("🔄 다시 고르기"):
            st.session_state.clicked = False
            st.rerun()
