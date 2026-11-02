from datetime import date

import streamlit as st

from classbridge.auth import require_role
from classbridge.db import get_user_client

require_role("parent")
client = get_user_client(st.session_state["token"])

st.title("Parent View")

# RLS means this only returns this parent's children
children = client.table("students").select("id, first_name").execute().data
if not children:
    st.info("No children are linked to your account yet.")
    st.stop()

for child in children:
    st.header(child["first_name"])

    enrolled = (
        client.table("enrollments")
        .select("class_id")
        .eq("student_id", child["id"])
        .execute()
        .data
    )
    class_ids = [e["class_id"] for e in enrolled]
    if not class_ids:
        st.write("Not enrolled in any classes yet.")
        continue

    rows = (
        client.table("assignments")
        .select("title, type, due_date, classes(name)")
        .in_("class_id", class_ids)
        .gte("due_date", date.today().isoformat())
        .order("due_date")
        .execute()
        .data
    )
    if rows:
        for r in rows:
            st.markdown(
                f"**{r['title']}**  \n"
                f"{r['classes']['name']} · {r['type']} · due {r['due_date']}"
            )
    else:
        st.write("No upcoming homework.")