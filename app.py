import streamlit as st
import random
import csv
import os
import base64
import urllib.parse

# 1. 웹페이지 설정
st.set_page_config(page_title="돼지름길", page_icon="🐷", layout="centered")

# 🔊 [사운드 함수] MP3 파일을 브라우저에서 자동 재생할 수 있도록 base64로 인코딩하는 함수
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

# 🎨 [디자인 커스텀] 말풍선 내부 디자인 및 지도 버튼 스타일 추가
st.markdown(
    """
    <style>
    .stApp { background-color: #FFF0F2 !important; }
    h1, h3 { color: #2B2B2B !important; text-align: center; }
    
    .pig-wrapper {
        position: relative;
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin-top: 10px;
        margin-bottom: -25px;
    }
    .pig-wrapper img {
        display: block;
        max-width: 650px;
        width: 100%;
        height: auto;
    }
    
    /* 말풍선 상자 크기를 멘트와 버튼 수용을 위해 조금 더 넓히고 조절 */
    .mouth-menu-box {
        position: absolute;
        left: 50%;
        margin-left: -320px; 
        top: 0;
        margin-top: -360px; /* 멘트가 길어져서 위로 20px 더 올렸습니다! */
        z-index: 999; 
        background-color: #FFFFFF !important;
        border: 6px solid #FF6B8B !important;
        border-radius: 25px !important;
        padding: 20px 25px !important;
        box-shadow: -10px 12px 25px rgba(0, 0, 0, 0.15); 
        min-width: 280px;
        max-width: 320px;
        text-align: center;
        animation: mouthPop 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .mouth-menu-box h4 { margin: 0 0 4px 0 !important; color: #FF6B8B !important; font-size: 1.0rem !important; }
    .mouth-menu-box .menu-title { margin: 5px 0 !important; font-size: 1.8rem !important; font-weight: bold !important; color: #2B2B2B !important; }
    
    /* 돼지 운세 멘트 스타일 */
    .mouth-menu-box .pig-comment { 
        margin: 8px 0 12px 0 !important; 
        font-size: 0.95rem !important; 
        color: #666666 !important; 
        line-height: 1.4;
        background-color: #FFF0F2;
        padding: 8px;
        border-radius: 12px;
    }
    
    /* 네이버 지도 버튼 스타일 */
    .map-btn {
        display: inline-block;
        background-color: #03C75A !important; /* 네이버 고유 초록색 */
        color: white !important;
        border-radius: 12px !important;
        padding: 6px 14px !important;
        font-size: 0.9rem !important;
        font-weight: bold !important;
        text-decoration: none !important;
        box-shadow: 0px 3px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    .map-btn:hover {
        transform: scale(1.05);
    }
    
    div[data-testid="stWidgetLabel"] p { display: none; }
    
    div[data-baseweb="select"] {
        border: 4px solid #FF6B8B !important;
        border-radius: 15px !important;
        background-color: #FF6B8B !important;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        min-height: 55px !important;
    }
    div[data-baseweb="select"] div {
        color: #FFFFFF !important; 
        font-size: 1.4rem !important;
        font-weight: bold !important;
        text-align: center;
        line-height: 1.5 !important;
        overflow: visible !important;
    }
    ul[role="listbox"] { background-color: #FFFFFF !important; }
    ul[role="listbox"] li { color: #2B2B2B !important; font-size: 1.2rem !important; }
    
    .stButton { display: flex; justify-content: center; margin-top: 15px; }
    .stButton button {
        background-color: #2B2B2B !important;
        color: white !important;
        border-radius: 20px !important;
        padding: 0.6rem 3rem !important;
        border: none !important;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
    }
    .stButton button p { font-size: 1.3rem !important; font-weight: bold !important; color: white !important; }
    @keyframes mouthPop { 0% { transform: scale(0.3); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }
    </style>
    """,
    unsafe_allow_html=True
)

# 2. 상단 타이틀
st.title("🐷 돼지름길")
st.subheader("오늘 뭐 먹지? 고민 끝, 지름길로 가면 돼지!")

# 3. 세션 상태 정의
categories = ["한식", "중식", "양식", "일식", "동남아", "디저트"]
if "clicked" not in st.session_state:
    st.session_state.clicked = False
if "selected_category" not in st.session_state:
    st.session_state.selected_category = "한식"
if "recommended_menu" not in st.session_state:
    st.session_state.recommended_menu = None
# ★ [새로 추가] 뽑힌 멘트를 기억해두는 보관함
if "pig_comment" not in st.session_state:
    st.session_state.pig_comment = None

# 카테고리별 돼지의 한마디 리스트 세팅
comment_pool = {
    "한식": ["역시 한국인은 밥심 꿀! 🍚", "뜨끈한 국물로 배를 채울 타이밍이다 꿀! 🍲", "상상만 해도 침 고인다 꿀...🤤"],
    "중식": ["강렬한 불맛이 당기는 날 꿀! 🔥", "단짠단짠의 정석으로 가자 꿀! 🥢", "오늘 기름칠 좀 해볼까 꿀? 🐼"],
    "양식": ["칼질 좀 하러 가볼까 꿀? 🍴", "치즈가 쭉 늘어나는 행복 꿀! 🍕", "분위기 한 번 내보는 거다 꿀! 🍷"],
    "일식": ["깔끔하고 정갈하게 가자 꿀! 🍣", "바삭함과 담백함의 끝판왕 꿀! 🍱", "호로록 한 그릇 뚝딱 꿀! 🍜"],
    "동남아": ["이국적인 향에 취해보자 꿀! 🌿", "입안 가득 퍼지는 상큼새콤함 꿀! 🍋", "한 번 빠지면 헤어나올 수 없다 꿀! 🍤"],
    "디저트": ["밥 배와 디저트 배는 따로 있다 꿀! 🍰", "달달함으로 당 충전 완료 꿀! 🍩", "행복은 멀리 있지 않다 꿀! 🍦"]
}

error_message = None

# --- 이름표 및 카테고리 선택부 ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    current_idx = categories.index(st.session_state.selected_category)
    category = st.selectbox("", options=categories, index=current_idx)
    if not st.session_state.clicked:
        st.session_state.selected_category = category

    if st.session_state.clicked:
        if st.button("다시 고르기 🔄"):
            st.session_state.clicked = False
            st.session_state.recommended_menu = None
            st.session_state.pig_comment = None
            st.rerun()
    else:
        if st.button("주문하기! 🛎️"):
            current_cat = st.session_state.selected_category
            file_candidates = [
                f"{current_cat}.xlsx - Sheet1.csv",
                f"{current_cat}.csv",
                f"{current_cat}.xlsx"
            ]
            
            final_file = None
            for candidate in file_candidates:
                if os.path.exists(candidate):
                    final_file = candidate
                    break

            if final_file is None:
                error_message = f"❌ '{current_cat}' 파일이 없습니다."
            else:
                menus = []
                encodings = ["utf-8", "cp949", "utf-8-sig", "euc-kr"]
                success_read = False
                
                for enc in encodings:
                    try:
                        with open(final_file, mode="r", encoding=enc) as f:
                            reader = csv.reader(f)
                            raw_rows = [row[0].strip() for row in reader if row and row[0].strip()]
                            if raw_rows:
                                if len(raw_rows) > 1 and raw_rows[0].lower() in ['menu', 'title', '이름', '메뉴']:
                                    menus = raw_rows[1:]
                                else:
                                    menus = raw_rows
                                success_read = True
                                break
                    except UnicodeDecodeError:
                        continue
                
                if success_read and menus:
                    st.session_state.recommended_menu = random.choice(menus)
                    # 버튼을 누른 순간 해당 카테고리의 멘트 풀에서 하나를 랜덤으로 뽑아 박제합니다.
                    st.session_state.pig_comment = random.choice(comment_pool.get(current_cat, ["맛있게 먹으면 0칼로리 꿀! 🐷"]))
                    st.session_state.clicked = True
                    st.rerun()
                else:
                    error_message = f"⚠️ {final_file}의 메뉴를 읽지 못했습니다."

    if error_message:
        st.error(error_message)

# --- 돼지 이미지 및 말풍선 오버레이 공간 ---
st.markdown('<div class="pig-wrapper">', unsafe_allow_html=True)

if st.session_state.clicked and st.session_state.recommended_menu:
    play_sound("magic.mp3")
    
    if os.path.exists("pig_open.png"):
        st.image("pig_open.png")
    else:
        st.markdown("<div style='font-size: 220px;'>😮</div>", unsafe_allow_html=True)
    
    # 네이버 지도 검색에 넣을 메뉴 이름을 인코딩 (한글 깨짐 방지)
    encoded_menu = urllib.parse.quote(st.session_state.recommended_menu)
    naver_map_url = f"https://map.naver.com/v5/search/{encoded_menu}"
    
    st.markdown(
        f"""
        <div class="mouth-menu-box">
            <h4>돼지름신의 추천! 냠냠</h4>
            <p class="menu-title">✨ {st.session_state.recommended_menu} ✨</p>
            <div class="pig-comment">🐷 {st.session_state.pig_comment}</div>
            <a href="{naver_map_url}" target="_blank" class="map-btn">📍 주변 맛집 찾기</a>
        </div>
        """, 
        unsafe_allow_html=True
    )
else:
    if os.path.exists("pig_closed.png"):
        st.image("pig_closed.png")
    else:
        st.markdown("<div style='font-size: 220px;'>😐</div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
