import streamlit as st


def require_role(role: str) -> None:
    if st.session_state.get("role") != role:
        st.warning("Please log in first.")
        st.stop()