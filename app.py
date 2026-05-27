import streamlit as st
from google import genai
from google.genai import types

# 페이지 설정
st.set_page_config(
    page_title="연애상담 챗봇",
    page_icon="💌",
)

st.title("💌 연애상담 챗봇")
st.caption("Gemini 2.5 Flash Lite 기반 상담 챗봇")

# API 키 불러오기
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except Exception:
    st.error("Secrets에 GOOGLE_API_KEY를 설정해주세요.")
    st.stop()

# Gemini 클라이언트 생성
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Gemini 클라이언트 생성 실패: {e}")
    st.stop()

# 채팅 기록 저장
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "안녕하세요 😊\n"
                "연애 고민을 편하게 이야기해주세요.\n"
                "최대한 공감하고 현실적으로 조언해드릴게요."
            ),
        }
    ]

# 기존 메시지 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
user_input = st.chat_input("연애 고민을 입력하세요...")

if user_input:
    # 사용자 메시지 저장
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    # 사용자 메시지 출력
    with st.chat_message("user"):
        st.markdown(user_input)

    # AI 응답 생성
    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        try:
            # 대화 기록 변환
            conversation_text = ""

            for msg in st.session_state.messages:
                role = "사용자" if msg["role"] == "user" else "상담사"
                conversation_text += f"{role}: {msg['content']}\n"

            prompt = f"""
당신은 따뜻하고 공감 능력이 뛰어난 연애상담 전문가입니다.

다음 원칙을 지켜 답변하세요:
- 공감하기
- 현실적인 조언 제공
- 지나친 단정 금지
- 부드럽고 따뜻한 말투 사용
- 한국어로 답변

대화 내용:
{conversation_text}

상담사 답변:
"""

            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.8,
                    max_output_tokens=700,
                ),
            )

            ai_response = response.text

            message_placeholder.markdown(ai_response)

            # 응답 저장
            st.session_state.messages.append(
                {"role": "assistant", "content": ai_response}
            )

        except Exception as e:
            error_message = f"""
⚠️ 오류가 발생했습니다.

잠시 후 다시 시도해주세요.

오류 내용:
`{e}`
"""
            message_placeholder.error(error_message)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": "오류가 발생했어요 😢 잠시 후 다시 시도해주세요.",
                }
            )

# 사이드바
with st.sidebar:
    st.header("설정")

    if st.button("대화 초기화"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "안녕하세요 😊\n"
                    "새로운 고민을 이야기해주세요."
                ),
            }
        ]
        st.rerun()

    st.markdown("---")
    st.markdown(
        """
### 안내
- Gemini 2.5 Flash Lite 사용
- Streamlit Community Cloud 배포 가능
- 채팅 기록 유지 지원
- 오류 처리 포함
"""
    )
