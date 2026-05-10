"""Policy Pass — Streamlit 프론트엔드."""

import os

import httpx
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8080")

st.set_page_config(page_title="Policy Pass", page_icon="🏛️", layout="wide")
st.title("Policy Pass — 청년정책 QA")


@st.cache_data(ttl=30)
def check_api_health():
    try:
        r = httpx.get(f"{API_BASE_URL}/health", timeout=5)
        return r.status_code == 200
    except Exception:
        return False


api_ok = check_api_health()
if api_ok:
    st.success("API 연결 정상")
else:
    st.warning(f"API 연결 실패: {API_BASE_URL}")

query = st.text_input("질문을 입력하세요", placeholder="청년 주거 정책에 대해 알려주세요")

if st.button("질문하기") and query:
    with st.spinner("답변 생성 중..."):
        try:
            r = httpx.post(f"{API_BASE_URL}/ask", json={"query": query}, timeout=60)
            if r.status_code == 200:
                data = r.json()
                st.markdown("### 답변")
                st.write(data.get("answer", "답변을 받지 못했습니다."))
            else:
                st.error(f"API 오류: {r.status_code}")
        except Exception as e:
            st.error(f"요청 실패: {e}")
