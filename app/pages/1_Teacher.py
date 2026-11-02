from datetime import date, timedelta

import streamlit as st

from classbridge.auth import require_role
from classbridge.db import get_user_client

require_role("teacher")
client = get_user_client(st.session_state["token"])

st.title("Teacher Dashboard")

# RLS means this only returns this teacher's classes
classes = client.table("classes").select("id, name, grade").execute().data
if not classes:
    st.info("You have no classes yet.")
    st.stop()

labels = {f"{c['name']} (Grade {c['grade']})": c["id"] for c in classes}
choice = st.selectbox("Class", list(labels))
class_id = labels[choice]

st.subheader("Create Assignment")
with st.form("create_assignment", clear_on_submit=True):
    title = st.text_input("Assignment title", placeholder="e.g. Fractions Practice")
    kind = st.selectbox("Type", ["worksheet", "quiz", "study guide"])
    due = st.date_input("Due date", value=date.today() + timedelta(days=2))
    share = st.toggle("Share with parents/tutors", value=True)
    submitted = st.form_submit_button("Create Assignment")

if submitted:
    if not title.strip():
        st.error("Please enter a title.")
    else:
        client.table("assignments").insert({
            "class_id": class_id,
            "title": title.strip(),
            "type": kind,
            "due_date": due.isoformat(),
            "shared_with_parents": share,
        }).execute()
        st.success("Assignment created.")

st.subheader("Upcoming assignments")
rows = (
    client.table("assignments")
    .select("title, type, due_date, shared_with_parents")
    .eq("class_id", class_id)
    .gte("due_date", date.today().isoformat())
    .order("due_date")
    .execute()
    .data
)
if rows:
    st.dataframe(rows, hide_index=True, use_container_width=True)
else:
    st.write("Nothing due yet.")