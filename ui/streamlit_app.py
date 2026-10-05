import os
import uuid
import httpx
import streamlit as st

API = os.getenv("API_URL", "http://localhost:8000")
HEADERS = {"X-API-Key": os.getenv("APP_API_KEY", "")}

st.set_page_config(page_title="AI Personal OS", page_icon="🧠", layout="wide")
st.session_state.setdefault("sid", uuid.uuid4().hex[:12])
st.session_state.setdefault("msgs", [])

with st.sidebar:
    st.title("🧠 AI Personal OS")
    user = st.text_input("User ID", "default")
    if st.button("New session"):
        st.session_state.update(sid=uuid.uuid4().hex[:12], msgs=[])
        st.rerun()
    st.caption(f"Session: {st.session_state.sid}")
    st.subheader("Memories")
    if st.button("Refresh / run maintenance"):
        httpx.post(f"{API}/maintenance/run", params={"user_id": user}, headers=HEADERS, timeout=120)
    try:
        for m in httpx.get(f"{API}/memories", params={"user_id": user}, headers=HEADERS, timeout=10).json()[:25]:
            st.markdown(f"**{m['kind']}** · {m['strength']}  \n{m['content']}")
    except Exception:
        st.warning("API se connect nahi hua")

for m in st.session_state.msgs:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m.get("mem"):
            with st.expander(f"Memories used ({len(m['mem'])})"):
                for x in m["mem"]:
                    st.write(f"[{x['kind']}] {x['content']}  _(score {x['score']})_")

if prompt := st.chat_input("Kuch bhi poocho..."):
    st.session_state.msgs.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("soch raha hu..."):
            try:
                r = httpx.post(f"{API}/chat", headers=HEADERS, timeout=90,
                               json={"session_id": st.session_state.sid, "message": prompt, "user_id": user})
                r.raise_for_status()
                data = r.json()
                st.markdown(data["reply"])
                st.session_state.msgs.append({"role": "assistant", "content": data["reply"], "mem": data["memories_used"]})
            except Exception as e:
                st.error(f"Error: {e}")
