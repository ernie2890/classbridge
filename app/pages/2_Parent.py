import streamlit as st
from classbridge.auth import require_role

require_role("parent")
st.title("Parent View")
st.write("Coming in Step 6.")