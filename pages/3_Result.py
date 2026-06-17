import streamlit as st

st.set_page_config(page_title="검색 결과", page_icon="📊")

st.title("📊 검색 결과")

if "selected_bus" not in st.session_state or st.session_state.selected_bus is None:
    st.warning("먼저 '2_Search' 페이지에서 버스를 선택하고 와주세요!")
else:
    bus = st.session_state.selected_bus
    info = st.session_state.bus_data[bus]
    
    st.metric(label=f"🟢 {bus} 실시간 정보", value=f"{info['remaining_time']}분 후 도착 예정")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"📍 현재 위치: **{info['current_station']}**")
    with col2:
        st.success(f"🛑 다음 정류장: **{info['next_station']}**")
        
    st.markdown("---")
    st.write("⚠️ 버스가 너무 멀리 있거나 만차인가요? 사이드바에서 '4_Alternative(대체버스 추천)' 페이지를 확인해보세요.")
