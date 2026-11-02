# ClassBridge: Project Overview

*For developers joining the project. Explains what exists, and why it is built this way.*

## 1. What it is

ClassBridge is a web app that helps teachers stay organized and lets parents/tutors follow their child's homework and upcoming exams. One platform, two experiences:

- **Teacher side:** create assignments, choose whether to share them with parents.
- **Parent/tutor side:** see upcoming homework and exam dates for their own child.

The original mockups also show a schedule, task list, student progress, skill-gap flags, and a "Start Study Session" feature. These are **deliberately out of scope for v1** (see section 7).

## 2. Goals and constraints

- **Learning project first.** Built to practice building a real app end to end. Competing with existing tools (Google Classroom, ClassDojo, Remind) is not the v1 goal.
- **Get something working quickly.** The owner is comfortable in Python, so the stack avoids JavaScript.
- **$0 to build and test.** Everything runs on free tiers.
- **Children's data.** Students are Grade 6-7 (many under 13), so privacy is designed in from the start, not added later.

## 3. Stack and why

| Layer | Choice | Why |
|---|---|---|
| UI | Streamlit (Python) | Pure Python, working screens in hours, usable in a phone browser. A native phone app was deferred on purpose: it needs JavaScript and app store setup. |
| Database + auth | Supabase (Postgres) | Free tier, built-in logins, and Row Level Security (RLS) enforces privacy inside the database. |
| Backend logic | Python (`src/classbridge`) | Same language as the UI; shared helpers for config and DB clients. |
| Email (planned) | Gmail via `smtplib` | Free and needs no domain. Sending services like Resend need a verified domain before emailing real people. Kept in one module so it can be swapped later. |
| Hosting | None yet | Runs locally. |

Databricks was considered and rejected for the app itself: it suits data pipelines and analytics, not user accounts or transactional apps.

## 4. Data model

Seven tables (`supabase/01_tables.sql`):

- `profiles`: one row per login (teacher or parent), linked to Supabase Auth.
- `classes`: owned by a teacher.
- `students`: **first name only**, no login. Minimal data on purpose.
- `enrollments`: many-to-many between classes and students.
- `parent_students`: many-to-many between parents and students.
- `assignments`: belong to a class; have a due date and a `shared_with_parents` flag.
- `notification_log`: prevents duplicate emails (backend-only).

Why this shape: the mockups had inconsistencies (a Grade 7 student inside a Grade 6 class, the parent and teacher sharing a surname). Separate link tables model who belongs to whom without those assumptions.

## 5. Privacy and security model

Privacy rules live **in the database**, not just in app code, so an app bug cannot leak another family's data.

- **RLS is on for every table** (`03_rls_policies.sql`).
- Teachers manage only their own classes, enrollments, and assignments.
- Parents can only *read*: their own children, those children's classes, and assignments where `shared_with_parents = true`.
- Policy checks use small `security definer` helper functions (`02_rls_functions.sql`) to avoid Postgres "infinite recursion" errors between tables that reference each other.
- `notification_log` has no policies on purpose. Only backend code using the **service role key** can write to it.

Key handling:
- Pages use `get_user_client(token)` so RLS always applies.
- `get_admin_client()` (service key, bypasses RLS) is for backend jobs like notifications only, never page code.
- `.env` is git-ignored. Never commit it.
- Development uses **fake data only**.

Verification: `tests/test_rls.py` logs in as each fake user and checks what the database returns (each parent sees only their own child, unshared assignments are hidden, a logged-out visitor sees nothing). All checks currently pass.

Legal note: US student-data laws (FERPA, COPPA) likely apply once real students are involved. Review them, ideally with legal advice, before real use.

## 6. Repo layout and workflow

```
app/Home.py               login + routing by role
app/pages/1_Teacher.py    create/list assignments
app/pages/2_Parent.py     child's upcoming homework
src/classbridge/          config.py, db.py, auth.py
supabase/                 01_tables, 02_rls_functions, 03_rls_policies, 04_seed_fake_data
tests/test_rls.py         privacy checks
docs/                     checklist, this overview, mockups
```

- **SQL lives in the repo** so the database can be rebuilt from scratch.
- **Branches:** `dev` (daily work) -> `staging` (ready to test) -> `main` (stable). Branches separate code, not data. Staging could point at a second free Supabase project later.
- Run order for the SQL scripts: tables, functions, policies, then seed data.

## 7. Scope decisions

**In v1:** login by role, teacher creates assignments with a share toggle, parent sees upcoming homework, email notification when something new is posted.

**Deferred, and why:**
- *Skills needing support:* needs real performance data and a way to infer weak skills; a large feature on its own.
- *Submitted / Not Started status:* needs a third user type (students) or extra teacher data entry.
- *Parent/tutor activity shown to teachers:* useful, but may feel like surveillance to parents.
- *Schedule and task list:* the "teacher organizer" side; add after the assignment loop works.
- *Practice sets / study sessions:* the most distinctive idea (tying reminders to practice material), so worth building once the core loop is proven.
- *Native phone app and push notifications:* later, reusing the same Supabase backend.

Product risk to remember: assignment alerts alone are table stakes. The value is likely teachers not doing extra data entry, and parents getting practice material, not just reminders.

## 8. Status

| Step | State |
|---|---|
| 1. Project setup | Done |
| 2. Database (tables, RLS functions, policies) | Done |
| 3. Fake seed data | Done |
| 4. Privacy tests | Done, all passing |
| 5. Teacher page | Done |
| 6. Parent page | In progress |
| 7. Email notifications | Not started |
| 8. Trial with a real teacher and parent (fake student data) | Not started |

## 9. Running it locally

1. Clone the repo and check out `dev`.
2. `python -m venv .venv`, activate it, then `pip install -r requirements.txt` and `pip install -e .`
3. Copy `.env.example` to `.env` and fill in the Supabase URL, anon key, and service key from your own Supabase project.
4. Run the SQL scripts in `supabase/` in order in the Supabase SQL editor. Create fake auth users, then fill their IDs into the seed script.
5. `python tests/test_rls.py` to verify the privacy rules.
6. `streamlit run app/Home.py`

## 10. Known limitations

- Streamlit forgets the login on browser refresh.
- Supabase sessions expire (about an hour by default); log in again if queries fail.
- The free Supabase plan pauses inactive projects.
- No hosting, no real email domain, no tests beyond the RLS checks.
