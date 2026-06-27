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

# 🎨 CSS
st.markdown("""
<style>

.stApp {
    background:
        linear-gradient(90deg, rgba(255,255,255,0.4) 1px, transparent 1px),
        linear-gradient(rgba(255,255,255,0.4) 1px, transparent 1px),
        linear-gradient(135deg, #FFDEE9 0%, #B5FFFC 100%) !important;
    background-size: 40px 40px, 40px 40px, auto !important;
}

/* 제목 */
h1 {
    color: #1f1f1f !important;
    font-weight: 900;
    text-align: center;
    text-shadow: 0px 2px 6px rgba(255,255,255,0.7);
}

h3 {
    color: #333 !important;
    text-align: center;
}

/* 스티커 */
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

/* 버튼 */
.stButton button {
    background-color:#2B2B2B !important;
    color:white !important;
    border-radius:20px !important;
}

.stButton button:hover {
    background-color:#444 !important;
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

.result-box h2, .result-box h3, .result-box p {
    color:#2B2B2B !important;
}

/* 모바일 스티커 완화 */
@media (max-width: 768px) {
    .food-sticker {
        opacity: 0.15;
        z-index: 0;
    }
}

</style>

<!-- 스티커 -->
<div class="food-sticker fs1">🍗</div>
<div class="food-sticker fs2">🍔</div>
<div class="food-sticker fs3">🍲</div>
<div class="food-sticker fs4">🍣</div>
<div class="food-sticker fs5">🍕</div>
<div class="food-sticker fs6">🍰</div>
""", unsafe_allow_html=True)

# 제목
st.title("돼지름길 🐷")
st.subheader("오늘 뭐 먹지? 추천 받으면 돼지!")

# 데이터
categories = ["한식","중식","양식","일식","동남아","디저트"]

comment_pool = {
   "한식": ["역시 한국인은 한식이 진리 꿀! 🍚", "입에 착 감기는 최고의 선택이다 꿀! 😋", "상상만 해도 벌써 든든하다 꿀! 👍"],
    "중식": ["오늘 입안 가득 불맛 충전 꿀! 🔥", "거부할 수 없는 짜릿한 중독성 꿀! 🥢", "오늘 한 끼는 제대로 기름칠 가자 꿀! 🐼"],
    "양식": ["입안 가득 풍미가 폭발한다 꿀! 🍴", "부드럽고 진한 맛의 정석 꿀! 🧀", "기분 내기 딱 좋은 훌륭한 선택 꿀! 🍷"],
    "일식": ["깔끔하고 담백하게 가보는 거다 꿀! 🍱", "정갈함 속의 깊은 내공 꿀! 🍣", "호불호 없이 싹 비울 비주얼 꿀! 🍜"],
    "동남아": ["매력적인 향에 푹 빠져보자 꿀! 🌿", "입맛을 제대로 돋워줄 치트키 꿀! 🍋", "한 번 맛보면 계속 생각나는 맛 꿀! 🍤"],
    "디저트": ["밥 배와 디저트 배는 따로 있다 꿀! 🍰", "달달함으로 당 충전 200% 완료 꿀! 🍩", "한 입 먹는 순간 스트레스 아웃 꿀! 🍦"]
}

# 상태
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
        trigger = st.button("주문하기 🛎️")
        reset = False
    else:
        trigger = False
        reset = st.button("🔄 다시 고르기")

if reset:
    st.session_state.clicked = False
    st.session_state.menu = None
    st.rerun()

# 슬롯
if trigger:

    file = f"{st.session_state.selected_category}.csv"

    if not os.path.exists(file):
        st.error("파일 없음")
    else:
        with open(file, "r", encoding="utf-8") as f:
            menus = [row[0] for row in csv.reader(f) if row]

        slot_box = st.empty()

        for i in range(10):
            temp = random.choice(menus)

            slot_box.markdown(f"""
                <h2 style="text-align:center;color:#FF6B8B;">
                    🌀 {temp} 🌀
                </h2>
            """, unsafe_allow_html=True)

            time.sleep(0.08)

        slot_box.empty()

        st.session_state.menu = random.choice(menus)
        st.session_state.clicked = True
        st.rerun()

# 결과
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

        # 📋 복사
        if st.button("📋 복사"):
            st.code(f"🐷 돼지름신의 추천: {st.session_state.menu}")
            st.toast("복사됨!")

        # 🗺 지도 버튼 (✔ 복사 바로 아래로 이동 완료)
        map_url = f"https://map.naver.com/v5/search/{st.session_state.menu}"

        st.markdown(f"""
        <div style="text-align:center; margin-top:10px;">
            <a href="{map_url}" target="_blank"
               style="
                    display:inline-block;
                    background:#03C75A;
                    color:white;
                    padding:12px 18px;
                    border-radius:12px;
                    text-decoration:none;
                    font-weight:900;
                    font-size:14px;
                    box-shadow:0px 4px 10px rgba(0,0,0,0.15);
               ">
               🗺️ 네이버 지도에서 검색
            </a>
        </div>
        """, unsafe_allow_html=True)





st.markdown("""
<style>

/* 🟢 기본 배경 */
.stApp {
    background:
        linear-gradient(90deg, rgba(255,255,255,0.4) 1px, transparent 1px),
        linear-gradient(rgba(255,255,255,0.4) 1px, transparent 1px),
        linear-gradient(135deg, #FFDEE9 0%, #B5FFFC 100%) !important;
    background-size: 40px 40px, 40px 40px, auto !important;
}

/* 🐷 스티커 기본 */
.food-sticker {
    position: fixed;
    font-size: 3rem;
    opacity: 0.8;
    z-index: 1;
    pointer-events: none;
}

/* 📱 모바일 대응 (핵심 수정) */
@media (max-width: 768px) {

    /* 👉 스티커만 뒤로 + 투명하게 */
    .food-sticker {
        opacity: 0.15;
        z-index: 0;
    }

    /* 👉 UI는 건드리지 말 것 (이게 핵심) */
}

</style>
""", unsafe_allow_html=True)
