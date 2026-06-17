import streamlit as st

st.set_page_config(page_title="도착 알림 설정", page_icon="⏰")

st.title("⏰ 도착 전 알림 설정")

if "alarms" not in st.session_state:
    st.session_state.alarms = {}

if "selected_bus" in st.session_state and st.session_state.selected_bus:
    bus = st.session_state.selected_bus
    st.info(f"현재 검색했던 버스: **{bus}**")
    
    if bus not in st.session_state.alarms:
        st.session_state.alarms[bus] = {"active": False, "time": 5}
        
    col1, col2 = st.columns(2)
    with col1:
        toggle = st.toggle("알림 활성화", value=st.session_state.alarms[bus]["active"], key=f"toggle_{bus}")
        st.session_state.alarms[bus]["active"] = toggle
    with col2:
        noti_time = st.selectbox("몇 분 전에 알릴까요?", [3, 5, 10], index=[3, 5, 10].index(st.session_state.alarms[bus]["time"]), key=f"time_{bus}")
        st.session_state.alarms[bus]["time"] = noti_time
        
    if toggle:
        st.toast(f"🎉 {bus} {noti_time}분 전 알림 설정 완료!", icon="🔔")

st.markdown("---")
st.subheader("📋 전체 알림 설정 현황")

if not st.session_state.alarms:
    st.caption("활성화된 알림이 없습니다.")
else:
    for b_num, settings in st.session_state.alarms.items():
        status_emoji = "🔔 ON" if settings["active"] else "🔕 OFF"
        status_color = "green" if settings["active"] else "gray"
        st.markdown(f"- **{b_num}**: :{status_color}[{status_emoji}] ({settings['time']}분 전 알림)")
