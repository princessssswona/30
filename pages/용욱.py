import streamlit as st

# 1. 페이지 기본 설정 및 스타일 정의
st.set_page_config(
    page_title="버스 알리미",
    page_icon="🚌",
    layout="wide"
)

# 2. 고정 버스 데이터 및 대체 노선 그룹 정의
BUS_DATA = {
    "1": 5, "2": 10, "5": 30, "10": 14, "14": 9, "20": 21, 
    "24": 11, "38": 31, "70": 2, "90": 6, "100": 17, 
    "800": 15, "810": 5, "900": 3, "901": 28
}

# 유사 노선/대체 가능한 버스 그룹 정의 (가상 시나리오)
ALTERNATIVE_GROUPS = [
    {"1", "5", "810", "900"},  # A 노선 구역
    {"2", "14", "24", "70", "90"},  # B 노선 구역
    {"10", "20", "38", "100"},  # C 노선 구역
    {"800", "901"}  # 외곽 노선 구역
]

# 3. Session State 초기화 (알림 설정 보존용)
if "notifications" not in st.session_state:
    st.session_state.notifications = {}

# 4. 사이드바 구성 (알림 설정된 버스 표시 영역)
with st.sidebar:
    st.header("🔔 나의 알림 설정 버스")
    st.write("메인 화면에서 알림을 켠 버스의 남은 시간을 확인할 수 있습니다.")
    st.markdown("---")
    
    # 알림이 켜진 버스 필터링
    active_alerts = {bus: time for bus, time in st.session_state.notifications.items() if time}
    
    if active_alerts:
        for bus in sorted(active_alerts.keys(), key=int):
            remaining_time = BUS_DATA[bus]
            st.metric(
                label=f"🚌 {bus}번 버스", 
                value=f"{remaining_time}분 후 도착",
                delta="곧 도착" if remaining_time <= 5 else None
            )
            st.markdown("---")
    else:
        st.info("현재 알림이 설정된 버스가 없습니다. 메인 페이지에서 검색 후 알림을 켜주세요!")

# 5. 메인 페이지 구성
st.title("🚌 버스 알리미")
st.caption("실시간 버스 도착 정보 및 대체 노선 안내 서비스")
st.markdown("---")

# 검색 및 안내 구역
st.subheader("🔍 버스 검색")
search_query = st.selectbox(
    "조회할 버스 번호를 선택하거나 입력하세요.",
    options=["선택하세요"] + list(BUS_DATA.keys())
)

if search_query != "선택하세요":
    st.success(f"### 📍 {search_query}번 버스 정보")
    
    # 도착 시간 안내
    arrival_time = BUS_DATA[search_query]
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"⏱ 도착 예정 시간: **{arrival_time}분 후**")
    
    with col2:
        # 알림 On/Off 토글 버튼
        # 기존에 켜져 있었는지 상태 확인 후 기본값 지정
        is_active = st.session_state.notifications.get(search_query, False)
        alert_toggle = st.toggle("📢 도착 전 알림 받기", value=is_active, key=f"toggle_{search_query}")
        
        # 토글 상태 저장 및 페이지 새로고침(사이드바 즉시 반영용)
        if alert_toggle != is_active:
            st.session_state.notifications[search_query] = alert_toggle
            st.rerun()

    st.markdown("---")
    
    # 대체 노선 추천 기능
    st.subheader("🔄 대체 가능한 추천 노선")
    
    # 현재 버스가 속한 노선 그룹 찾기
    alternatives = []
    for group in ALTERNATIVE_GROUPS:
        if search_query in group:
            # 본인 제외, 도착 시간이 더 빠르거나 비슷한 버스 추천
            alternatives = [bus for bus in group if bus != search_query]
            break
            
    if alternatives:
        st.write(f"현재 {search_query}번 버스 대신 이용할 수 있는 노선 정보입니다.")
        
        # 추천 노선들을 보기 좋게 카드 형태로 배치
        cols = st.columns(len(alternatives))
        for idx, alt_bus in enumerate(alternatives):
            with cols[idx]:
                alt_time = BUS_DATA[alt_bus]
                # 검색한 버스보다 더 빠른 경우 초록색, 느린 경우 일반 표시
                if alt_time < arrival_time:
                    st.markdown(f"""
                    <div style="background-color:#e1f5fe; padding:15px; border-radius:10px; border-left: 5px solid #03a9f4;">
                        <h4 style="margin:0; color:#0288d1;">🚌 {alt_bus}번</h4>
                        <p style="margin:5px 0 0 0; font-size:18px; font-weight:bold; color:#01579b;">{alt_time}분 후 (더 빠름!)</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background-color:#f5f5f5; padding:15px; border-radius:10px; border-left: 5px solid #9e9e9e;">
                        <h4 style="margin:0; color:#616161;">🚌 {alt_bus}번</h4>
                        <p style="margin:5px 0 0 0; font-size:18px; font-weight:bold; color:#212121;">{alt_time}분 후</p>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.info("해당 버스는 단독 노선이므로 대체 가능한 다른 버스가 없습니다.")

else:
    # 아무것도 검색하지 않았을 때 나오는 기본 안내 화면
    st.info("위의 드롭다운 메뉴를 클릭하여 조회를 원하는 버스 번호를 선택해주세요.")
    
    # 전체 시간표 미리보기 (보너스 기능)
    with st.expander("📊 전체 버스 도착 시간표 보기"):
        # 데이터를 보기 좋게 3열로 나누어 출력
        all_buses = sorted(list(BUS_DATA.keys()), key=int)
        cols = st.columns(3)
        for idx, bus in enumerate(all_buses):
            with cols[idx % 3]:
                st.write(f"• **{bus}번 버스**: {BUS_DATA[bus]}분 후 도착")
