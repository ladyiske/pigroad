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
        position: relative;
        overflow-x: hidden;
    }
    
    h1, h3 { color: #2B2B2B !important; text-align: center; position: relative; z-index: 10; }
    h1 { text-shadow: 0px 4px 10px rgba(255, 255, 255, 0.6); }
    
    .food-sticker { position: fixed; font-size: 3.5rem; opacity: 0.8; user-select: none; pointer-events: none; z-index: 1; }
    .fs-1 { left: 4%; top: 15%; animation: floatSticker1 4s ease-in-out infinite alternate; }
    .fs-2 { left: 5%; top: 45%; animation: floatSticker2 5s ease-in-out infinite alternate; }
    .fs-3 { left: 3%; top: 75%; animation: floatSticker1 4.5s ease-in-out infinite alternate; }
    .fs-4 { right: 4%; top: 18%; animation: floatSticker2 4.2s ease-in-out infinite alternate; }
    .fs-5 { right: 6%; top: 48%; animation: floatSticker1 4.8s ease-in-out infinite alternate; }
    .fs-6 { right: 3%; top: 78%; animation: floatSticker2 5.2s ease-in-out infinite alternate; }
    
    @keyframes floatSticker1 { 0% { transform: translateY(0) rotate(-5deg); } 100% { transform: translateY(-15px) rotate(10deg); } }
    @keyframes floatSticker2 { 0% { transform: translateY(0) rotate(8deg); } 100% { transform: translateY(-20px) rotate(-8deg); } }
    
    .stHorizontalBlock, .pig-wrapper { position: relative; z-index: 5; }
    
    .pig-wrapper { position: relative; display: flex; justify-content: center; align-items: center; width: 100%; margin-top: 10px; margin-bottom: -25px; }
    .pig-wrapper img { display: block; max-width: 650px; width: 100%; height: auto; }
    
    .mouth-menu-box {
        position: absolute; left: 50%; margin-left: -320px; top: 0; margin-top: -360px; z-index: 999; 
        background-color: #FFFFFF !important; border: 6px solid #FF6B8B !important; border-radius: 25px !important;
        padding: 20px 25px !important; box-shadow: -10px 12px 25px rgba(0, 0, 0, 0.15); 
        min-width: 290px; max-width: 340px; text-align: center;
        animation: mouthPop 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    .mouth-menu-box h4 { margin: 0 0 6px 0 !important; color: #FF6B8B !important; font-size: 1.1rem !important; display: flex; align-items: center; justify-content: center; gap: 6px; }
    .nose-icon { display: inline-block; animation: noseWiggle 1s ease-in-out infinite alternate; }
    .nose-icon-right { display: inline-block; animation: noseWiggle 1s ease-in-out infinite alternate-reverse; }
    
    .mouth-menu-box .menu-title { margin: 5px 0 !important; font-size: 1.8rem !important; font-weight: bold !important; color: #2B2B2B !important; }
    .mouth-menu-box .pig-comment { margin: 8px 0 12px 0 !important; font-size: 0.95rem !important; color: #666666 !important; line-height: 1.4; background-color: #FFF0F2; padding: 8px; border-radius: 12px; }
    
    .btn-container { display: flex; justify-content: center; gap: 8px; margin-top: 5px; }
    
    .map-btn {
        display: inline-block; background-color: #03C75A !important; color: white !important;
        border-radius: 12px !important; padding: 8px 14px !important; font-size: 0.85rem !important;
        font-weight: bold !important; text-decoration: none !important; box-shadow: 0px 3px 6px rgba(0,0,0,0.1); transition: transform 0.2s;
        line-height: 1.2;
    }
    .map-btn:hover { transform: scale(1.05); }

    .right-share-box button {
        background-color: #FF6B8B !important; color: white !important;
        border-radius: 15px !important; padding: 12px 20px !important;
        border: none !important; box-shadow: 0px 4px 10px rgba(0,0,0,0.15) !important;
        transition: transform 0.2s; width: 100%; min-height: 50px;
        margin-top: -240px !important;
        position: relative; z-index: 9999;
    }
    .right-share-box button:hover { transform: scale(1.05); }
    .right-share-box button p { font-size: 1rem !important; font-weight: bold !important; color: white !important; }
    
    div[data-testid="stWidgetLabel"] p { display: none; }
    div[data-baseweb="select"] { border: 4px solid #FF6B8B !important; border-radius: 15px !important; background-color: #FF6B8B !important; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1); min-height: 55px !important; }
    div[data-baseweb="select"] div { color: #FFFFFF !important; font-size: 1.4rem !important; font-weight: bold !important; text-align: center; line-height: 1.5 !important; overflow: visible !important; }
    ul[role="listbox"] { background-color: #FFFFFF !important; }
    ul[role="listbox"] li { color: #2B2B2B !important; font-size: 1.2rem !important; }
    
    .stButton { display: flex; justify-content: center; margin-top: 15px; }
    .stButton button { background-color: #2B2B2B !important; color: white !important; border-radius: 20px !important; padding: 0.6rem 3rem !important; border: none !important; box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1); }
    .stButton button p { font-size: 1.3rem !important; font-weight: bold !important; color: white !important; }
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

# 2. 상단 타이틀
st.title("🐷 돼지름길")
st.subheader("오늘 뭐 먹지? 고민 끝, 지름길로 가세요!")

# 3. 세션 상태 정의
categories = ["한식", "중식", "양식", "일식", "동남아", "디저트"]
if "clicked" not in st.session_state: st.session_state.clicked = False
if "selected_category" not in st.session_state: st.session_state.selected_category = "한식"
if "recommended_menu" not in st.session_state: st.session_state.recommended_menu = None
if "pig_comment" not in st.session_state: st.session_state.pig_comment = None

comment_pool = {
    "한식": ["역시 한국인은 한식이 진리 꿀! 🍚", "입에 착 감기는 최고의 선택이다 꿀! 😋", "상상만 해도 벌써 든든하다 꿀! 👍"],
    "중식": ["오늘 입안 가득 불맛 충전 꿀! 🔥", "거부할 수 없는 짜릿한 중독성 꿀! 🥢", "오늘 한 끼는 제대로 기름칠 가자 꿀! 🐼"],
    "양식": ["입안 가득 풍미가 폭발한다 꿀! 🍴", "부드럽고 진한 맛의 정석 꿀! 🧀", "기분 내기 딱 좋은 훌륭한 선택 꿀! 🍷"],
    "일식": ["깔끔하고 담백하게 가보는 거다 꿀! 🍱", "정갈함 속의 깊은 내공 꿀! 🍣", "호불호 없이 싹 비울 비주얼 꿀! 🍜"],
    "동남아": ["매력적인 향에 푹 빠져보자 꿀! 🌿", "입맛을 제대로 돋워줄 치트키 꿀! 🍋", "한 번 맛보면 계속 생각나는 맛 꿀! 🍤"],
    "디저트": ["밥 배와 디저트 배는 따로 있다 꿀! 🍰", "달달함으로 당 충전 200% 완료 꿀! 🍩", "한 입 먹는 순간 스트레스 아웃 꿀! 🍦"]
}

error_message = None
trigger_slot_machine = False

# --- 이름표 및 카테고리 선택부 ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    current_idx = categories.index(st.session_state.selected_category)
    category = st.selectbox("", options=categories, index=current_idx)
    if not st.session_state.clicked: st.session_state.selected_category = category

    if st.session_state.clicked:
        if st.button("다시 고르기 🔄"):
            st.session_state.clicked = False
            st.session_state.recommended_menu = None
            st.session_state.pig_comment = None
            st.rerun()
    else:
        if st.button("주문하기! 🛎️"): trigger_slot_machine = True

# --- 흐름 제어 및 슬롯머신 공간 ---
if trigger_slot_machine:
    current_cat = st.session_state.selected_category
    file_candidates = [f"{current_cat}.xlsx - Sheet1.csv", f"{current_cat}.csv", f"{current_cat}.xlsx"]
    final_file = next((c for c in file_candidates if os.path.exists(c)), None)

    if final_file is None: error_message = f"❌ '{current_cat}' 파일이 없습니다."
    else:
        menus = []
        for enc in ["utf-8", "cp949", "utf-8-sig", "euc-kr"]:
            try:
                with open(final_file, mode="r", encoding=enc) as f:
                    reader = csv.reader(f)
                    rows = [row[0].strip() for row in reader if row and row[0].strip()]
                    menus = rows[1:] if rows and rows[0].lower() in ['menu', 'title', '이름', '메뉴'] else rows
                    if menus: break
            except: continue
        
        if menus:
            slot_placeholder = st.empty()
            for _ in range(12):
                temp = random.choice(menus)
                with slot_placeholder.container():
                    st.markdown(f"<h2 style='text-align:center; color:#FF6B8B; margin-bottom:10px;'>🌀 뚜루루루... {temp} 🌀</h2>", unsafe_allow_html=True)
                    st.markdown('<div class="pig-wrapper"><div style="font-size:220px; text-align:center;">😐</div></div>', unsafe_allow_html=True)
                time.sleep(0.08)
            slot_placeholder.empty()
            st.session_state.recommended_menu = random.choice(menus)
            st.session_state.pig_comment = random.choice(comment_pool.get(current_cat, ["맛있게 먹으면 0칼로리 꿀! 🐷"]))
            st.session_state.clicked = True
            st.rerun()
        else: error_message = f"❌ 메뉴를 읽지 못했습니다."

if error_message: st.error(error_message)

# --- 결과 출력 구간 ---
if st.session_state.clicked and st.session_state.recommended_menu:
    play_sound("magic.mp3")
    encoded_menu = urllib.parse.quote(st.session_state.recommended_menu)
    naver_map_url = f"https://map.naver.com/v5/search/{encoded_menu}"
    share_text = f"🐷 돼지름길 오늘 추천 메뉴: {st.session_state.recommended_menu}!\n\"{st.session_state.pig_comment}\""
    
    st.markdown(f"""
        <div style="position: relative; max-width: 750px; margin: 0 auto; padding-top: 10px;">
            <div class="mouth-menu-box" style="margin-top: 50px;">
                <h4><span class="nose-icon">🐷</span>오늘의 추천! 냠냠<span class="nose-icon-right">🐷</span></h4>
                <p class="menu-title">✨ {st.session_state.recommended_menu} ✨</p>
                <div class="pig-comment">🐷 {st.session_state.pig_comment}</div>
                <div class="btn-container"><a href="{naver_map_url}" target="_blank" class="map-btn">📍 주변 맛집</a></div>
            </div>
            <div class="pig-wrapper">
    """, unsafe_allow_html=True)
    
    if os.path.exists("pig_open.png"): st.image("pig_open.png")
    else: st.markdown("<div style='font-size: 220px; text-align:center;'>😮</div>", unsafe_allow_html=True)
    st.markdown("</div>")

    c1, c2, c3 = st.columns([4, 2, 3])
    with c3:
        st.markdown('<div class="right-share-box">', unsafe_allow_html=True)
        if st.button("📋 결과 복사해서 공유"):
            st.code(share_text, language="")
            st.toast("우측 복사 버튼을 눌러 공유하세요! 💬")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

elif not trigger_slot_machine:
    st.markdown('<div class="pig-wrapper">', unsafe_allow_html=True)
    if os.path.exists("pig_closed.png"): st.image("pig_closed.png")
    else: st.markdown("<div style='font-size: 220px;'>😐</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
