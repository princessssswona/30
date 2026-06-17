import streamlit as st

st.set_page_config(page_title="대체버스 추천", page_icon="🔄")

st.title("🔄 대체버스 추천")

if "selected_bus" not in st.session_state or st.session_state.selected_bus is None:
    st.warning("조회된 버스가 없습니다. '2_Search' 페이지에서 버스를 먼저 검색해주세요.")
else:
    bus = st.session_state.selected_bus
    info = st.session_state.bus_data[bus]
    alts = info["alternatives"]
    
    st.subheader(f"💡 {bus} 대신 탈 수 있는 추천 노선")
    
    for alt in alts:
        alt_info = st.session_state.bus_data[alt]
        with st.container(border=True):
            st.markdown(f"### 🚍 {alt}")
            st.write(f"⏱️ 도착까지 **{alt_info['remaining_time']}분** 남음")
            st.caption(f"현재 위치: {alt_info['current_station']} ➡️ 다음 정류장: {alt_info['next_station']}")
            
            if st.button(f"🎯 {alt} 정보로 변경하기", key=alt):
                st.session_state.selected_bus = alt
                st.success(f"선택 버스가 {alt}로 변경되었습니다! '3_Result' 페이지에서 결과를 확인하세요.")
