import streamlit as st
import random
import csv
import os
import base64
import time

# 1. 웹페이지 설정
st.set_page_config(page_title="돼지름길", page_icon="🐷", layout="centered")

# 🔊 사운드 함수
def play_sound(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            st.markdown(f"""
                <audio autoplay style="display:none;">
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
            """, unsafe_allow_html=True)

# 🎨 디자인
st.markdown("""
<style>
html, body, .stApp {
    background: linear-gradient(135deg, #FFDEE9 0%, #B5FFFC 100%) !important;
}

h1, h3 {
    color: #2B2B2B !important;
    text-align: center;
}

.result-box h2, .result-box h3 {
    color: #2B2B2B !important;
}

.result-box {
    background: white;
    border: 5px solid #FF6B8B;
    border-radius: 20px;
    padding: 20px;
    text-align: center;
    margin: 0 auto;
    max-width: 420px;
}
</style>
""", unsafe_allow_html=True)

# 2. 타이틀
st.title("🐷 돼지름길")
st.subheader("오늘 뭐 먹지? 고민 끝!")

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
        if st.button("주문하기 🛎️"):
            trigger = True
    else:
        trigger = False
        if st.button("다시 고르기 🔄"):
            st.session_state.clicked = False
            st.session_state.recommended_menu = None
            st.rerun()

# 5. ⭐ 핵심: 카테고리별 CSV 연결 (방법 1)
if 'trigger' in locals() and trigger:

    current_cat = st.session_state.selected_category
    final_file = f"{current_cat}.csv"

    if not os.path.exists(final_file):
        st.error(f"❌ {final_file} 파일이 없습니다.")
    else:
        menus = []

        encodings = ["utf-8", "cp949", "utf-8-sig", "euc-kr"]
        success = False

        for enc in encodings:
            try:
                with open(final_file, "r", encoding=enc) as f:
                    reader = csv.reader(f)
                    rows = [row[0].strip() for row in reader if row and row[0].strip()]

                    if rows:
                        if rows[0] in ["메뉴", "menu", "title"]:
                            menus = rows[1:]
                        else:
                            menus = rows
                        success = True
                        break
            except:
                continue

        if success and menus:
            # 슬롯 느낌 연출
            slot_box = st.empty()

            for i in range(10):
                temp = random.choice(menus)
                with slot_box.container():
                    st.markdown(f"""
                        <h2 style="text-align:center; color:#FF6B8B;">
                        🌀 {temp} 🌀
                        </h2>
                    """, unsafe_allow_html=True)
                    st.markdown("<div style='text-align:center; font-size:120px;'>🐷</div>", unsafe_allow_html=True)
                time.sleep(0.1)

            slot_box.empty()

            # 결과 확정
            st.session_state.recommended_menu = random.choice(menus)
            st.session_state.clicked = True
            st.rerun()

# 6. 결과 화면
if st.session_state.clicked and st.session_state.recommended_menu:

    play_sound("magic.mp3")

    st.markdown(f"""
        <div class="result-box">
            <h3>오늘의 추천</h3>
            <h2>✨ {st.session_state.recommended_menu} ✨</h2>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        if os.path.exists("pig_open.png"):
            st.image("pig_open.png", use_container_width=True)

    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)

        if st.button("📋 복사"):
            st.code(f"🐷 오늘 메뉴: {st.session_state.recommended_menu}")
            st.toast("복사됨!")

        if st.button("🔄 다시 고르기"):
            st.session_state.clicked = False
            st.rerun()
