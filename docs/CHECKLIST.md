# ClassBridge v1

## Step 1: Setup
- [x] Create GitHub repo, clone, create dev and staging branches
- [x] Create venv
- [x] Create .gitignore before first commit
- [x] Create folder structure, .env.example, requirements.txt, pyproject.toml
- [x] Add config.py and db.py
- [x] First commit and push on dev

## Step 2: Database
- [x] Create Supabase project
- [x] Run tables script
- [x] Run RLS functions script
- [x] Run RLS policies script
- [x] Add URL, anon key, service key to .env

## Step 3: Fake data
- [x] Create 1 teacher + 2 parent users in Supabase Auth
- [x] Add profiles rows with roles
- [x] Add 1 class, 2 students, enrollments
- [x] Link each parent to one child
- [x] Save as supabase/04_seed_fake_data.sql

## Step 4: Test privacy
- [x] Parent A sees only their child's assignments
- [x] Parent B sees only their child's assignments
- [x] Teacher sees only their own classes
- [x] Unshared assignment hidden from parents
- [x] Fix any leaks before moving on

## Step 5: Teacher page
- [x] Login with Supabase Auth
- [x] Create assignment form (title, type, due date, share toggle)
- [x] List this week's assignments

## Step 6: Parent page
- [ ] Parent login
- [ ] Upcoming homework list by due date

## Step 7: Email notifications
- [ ] Gmail app password in .env
- [ ] Email parents when an assignment is created (smtplib)
- [ ] Write to notification_log (no duplicates)

## Step 8: Try it
- [ ] One teacher and one parent test it (fake data only)
- [ ] Write down what confused them