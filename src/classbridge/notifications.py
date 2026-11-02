import smtplib
from email.message import EmailMessage

from classbridge import config
from classbridge.db import get_admin_client


def _send(to: str, subject: str, body: str) -> None:
    msg = EmailMessage()
    msg["From"] = config.GMAIL_ADDRESS
    msg["To"] = config.TEST_RECIPIENT or to
    msg["Subject"] = subject
    msg.set_content(body)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(config.GMAIL_ADDRESS, config.GMAIL_APP_PASSWORD)
        server.send_message(msg)


def notify_new_assignment(assignment_id: str) -> int:
    """Email each parent whose child is in the class. Returns emails sent."""
    admin = get_admin_client()  # bypasses RLS: backend use only

    a = (
        admin.table("assignments")
        .select("id, title, due_date, class_id, shared_with_parents, classes(name)")
        .eq("id", assignment_id)
        .single()
        .execute()
        .data
    )
    if not a["shared_with_parents"]:
        return 0

    enrolled = (
        admin.table("enrollments").select("student_id")
        .eq("class_id", a["class_id"]).execute().data
    )
    student_ids = [e["student_id"] for e in enrolled]
    if not student_ids:
        return 0

    links = (
        admin.table("parent_students")
        .select("parent_id, students(first_name)")
        .in_("student_id", student_ids)
        .execute()
        .data
    )
    already = {
        r["parent_id"]
        for r in admin.table("notification_log").select("parent_id")
        .eq("assignment_id", assignment_id).execute().data
    }

    # One email per parent, even with several children in the class
    kids_by_parent = {}
    for link in links:
        kids_by_parent.setdefault(link["parent_id"], []).append(
            link["students"]["first_name"]
        )

    sent = 0
    for parent_id, kids in kids_by_parent.items():
        if parent_id in already:
            continue
        email = admin.auth.admin.get_user_by_id(parent_id).user.email
        _send(
            email,
            f"New homework: {a['title']}",
            f"A new assignment was posted for {', '.join(kids)} in "
            f"{a['classes']['name']}.\n\n{a['title']}, due {a['due_date']}.",
        )
        admin.table("notification_log").insert(
            {"assignment_id": assignment_id, "parent_id": parent_id}
        ).execute()
        sent += 1
    return sent