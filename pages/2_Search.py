import streamlit as st
import random

st.set_page_config(page_title="버스 검색", page_icon="🔍")

# 가상 데이터 생성 (세션 상태에 저장하여 다른 페이지와 공유)
if "bus_data" not in st.session_state:
    bus_numbers = [f"{random.randint(100, 999)}번" for _ in range(50)]
    bus_numbers = list(set(bus_numbers))[:50]
    while len(bus_numbers) < 50:
        bus_numbers.append(f"{random.randint(100, 999)}번")
        bus_numbers = list(set(bus_numbers))
        
    data = {}
    stations_pool = ["서울역", "시청", "광화문", "종로3가", "동대문", "강남역", "홍대입구", "신촌", "잠실역", "사당역", "여의도역", "판교역"]
    for i, bus in enumerate(bus_numbers):
        data[bus] = {
            "remaining_time": (i % 15) + 3,
            "current_station": stations_pool[i % len(stations_pool)],
            "next_station": stations_pool[(i + 1) % len(stations_pool)],
            "alternatives": [bus_numbers[(i + 5) % 50], bus_numbers[(i + 12) % 50]]
        }
    st.session_state.bus_data = data

if "selected_bus" not in st.session_state:
    st.session_state.selected_bus = None

st.title("🔍 버스 검색")
st.write("조회하고자 하는 버스 번호를 선택하거나 검색해주세요.")

bus_list = sorted(list(st.session_state.bus_data.keys()))
selected = st.selectbox("버스 노선 선택", ["선택하세요..."] + bus_list)

if selected != "선택하세요...":
    st.session_state.selected_bus = selected
    st.success(f"🎯 {selected}이(가) 선택되었습니다! 사이드바에서 '3_Result(검색 결과)' 페이지로 이동해 주세요.")
