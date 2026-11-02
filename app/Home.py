import streamlit as st
from classbridge.db import get_anon_client, get_user_client

st.set_page_config(page_title="ClassBridge", page_icon="📖")
st.title("📖 ClassBridge")


def login(email: str, password: str) -> None:
    res = get_anon_client().auth.sign_in_with_password(
        {"email": email, "password": password}
    )
    token = res.session.access_token
    profile = (
        get_user_client(token)
        .table("profiles")
        .select("role, display_name")
        .eq("id", res.user.id)
        .single()
        .execute()
        .data
    )
    st.session_state["token"] = token
    st.session_state["user_id"] = res.user.id
    st.session_state["role"] = profile["role"]
    st.session_state["name"] = profile["display_name"]


if "token" in st.session_state:
    st.success(f"Hi, {st.session_state['name']}!")
    if st.session_state["role"] == "teacher":
        st.page_link("pages/1_Teacher.py", label="Go to Teacher Dashboard", icon="🧑‍🏫")
    else:
        st.page_link("pages/2_Parent.py", label="Go to Parent View", icon="👪")
    if st.button("Log out"):
        st.session_state.clear()
        st.rerun()
else:
    with st.form("login"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Log in")
    if submitted:
        try:
            login(email, password)
            st.rerun()
        except Exception:
            st.error("Login failed. Check your email and password.")