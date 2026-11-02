insert into profiles (id, role, display_name) values
  ('dfab2277-266a-4127-8b49-6bdfa823a441', 'teacher', 'Ms. Carter'),
  ('cb1f4ac9-a69f-406d-862b-b2d936cfc857', 'parent',  'Parent One'),
  ('f2fbc9ae-d1db-4363-bb27-c5fa33bfbdc8', 'parent',  'Parent Two');

insert into classes (id, teacher_id, name, grade, room) values
  ('11111111-1111-1111-1111-111111111111', 'dfab2277-266a-4127-8b49-6bdfa823a441', 'Math', 6, '104');

insert into students (id, first_name) values
  ('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'Mateo'),
  ('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 'Taylor');

insert into enrollments (class_id, student_id) values
  ('11111111-1111-1111-1111-111111111111', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'),
  ('11111111-1111-1111-1111-111111111111', 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb');

insert into parent_students (parent_id, student_id) values
  ('cb1f4ac9-a69f-406d-862b-b2d936cfc857', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'),
  ('f2fbc9ae-d1db-4363-bb27-c5fa33bfbdc8', 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb');

insert into assignments (class_id, title, type, due_date, shared_with_parents) values
  ('11111111-1111-1111-1111-111111111111', 'Fractions Practice', 'worksheet', current_date + 2, true),
  ('11111111-1111-1111-1111-111111111111', 'Teacher-only draft', 'quiz', current_date + 5, false);