alter table profiles         enable row level security;
alter table classes          enable row level security;
alter table students         enable row level security;
alter table enrollments      enable row level security;
alter table parent_students  enable row level security;
alter table assignments      enable row level security;
alter table notification_log enable row level security;

-- profiles: you see and edit only your own
create policy "own profile read" on profiles
  for select using (id = auth.uid());
create policy "own profile write" on profiles
  for all using (id = auth.uid()) with check (id = auth.uid());

-- classes
create policy "teacher manages own classes" on classes
  for all using (teacher_id = auth.uid())
  with check (teacher_id = auth.uid());
create policy "parent sees child's classes" on classes
  for select using (parent_has_class(id));

-- students
create policy "teacher sees own students" on students
  for select using (teaches_student(id));
create policy "parent sees own children" on students
  for select using (is_parent_of(id));

-- enrollments
create policy "teacher manages enrollments" on enrollments
  for all using (is_teacher_of(class_id))
  with check (is_teacher_of(class_id));
create policy "parent sees child's enrollments" on enrollments
  for select using (is_parent_of(student_id));

-- parent_students: parents see only their own links
create policy "parent sees own links" on parent_students
  for select using (parent_id = auth.uid());

-- assignments
create policy "teacher manages own assignments" on assignments
  for all using (is_teacher_of(class_id))
  with check (is_teacher_of(class_id));
create policy "parent sees shared assignments" on assignments
  for select using (shared_with_parents and parent_has_class(class_id));

-- notification_log: no policies on purpose (backend service key only)