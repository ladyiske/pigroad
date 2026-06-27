import streamlit as st
import random
import os
import openpyxl  # 엑셀 파일을 읽기 위한 라이브러리

# 1. 웹페이지 설정 및 제목
st.set_page_config(page_title="돼지름길", page_icon="🐷", layout="centered")
st.title("🐷 돼지름길")
st.subheader("오늘 뭐 먹지? 고민 끝, 지름길로 가세요!")

# 2. 카테고리 정의
categories = ["한식", "중식", "양식", "일식", "동남아", "디저트"]

# 3. 사용자 선택 UI
category = st.selectbox("원하는 음식 종류를 선택하세요:", options=categories)

# 4. 버튼 클릭 감지
clicked = st.button(f"{category} 메뉴 추천받기 ✨")

if clicked:
    # 찾을 엑셀 파일 이름 후보들 (확장자 문제 완벽 방지)
    file_candidates = [
        f"{category}.xlsx",
        f"{category}.csv",  # 이름만 csv인 엑셀 파일 대비
        f"{category}.xlsx - Sheet1.csv"
    ]
    
    final_file = None
    for candidate in file_candidates:
        if os.path.exists(candidate):
            final_file = candidate
            break

    # 파일이 없는 경우 에러 처리
    if final_file is None:
        st.error(f"❌ '{category}' 관련 엑셀 파일을 찾을 수 없습니다.")
        st.info(f"💡 깃허브 저장소에 **'{category}.xlsx'** 파일이 올바르게 올라가 있는지 확인해 주세요!")
    else:
        try:
            # 엑셀 파일 열기
            wb = openpyxl.load_workbook(final_file, data_only=True)
            sheet = wb.active
            
            menus = []
            # 첫 번째 줄(헤더: menu)을 제외하고 두 번째 줄부터 데이터 읽기
            for row in sheet.iter_rows(min_row=2, min_col=1, max_col=1, values_only=True):
                if row[0]:  # 빈 칸이 아니라면
                    menus.append(str(row[0]).strip())
            
            # 메뉴 추천
            if menus:
                recommended_menu = random.choice(menus)
                st.success(f"오늘의 추천 메뉴는 바로 **[{recommended_menu}]** 입니다! 츄릅 😋")
            else:
                st.error(f"⚠️ {final_file} 파일 안에 저장된 메뉴가 없습니다.")
                
        except Exception as e:
            st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")
