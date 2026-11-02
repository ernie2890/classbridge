create table profiles (
  id uuid primary key references auth.users,
  role text check (role in ('teacher','parent')),
  display_name text
);

create table classes (
  id uuid primary key default gen_random_uuid(),
  teacher_id uuid references profiles(id),
  name text,
  grade int,
  room text
);

create table students (
  id uuid primary key default gen_random_uuid(),
  first_name text
);

create table enrollments (
  class_id uuid references classes(id),
  student_id uuid references students(id),
  primary key (class_id, student_id)
);

create table parent_students (
  parent_id uuid references profiles(id),
  student_id uuid references students(id),
  primary key (parent_id, student_id)
);

create table assignments (
  id uuid primary key default gen_random_uuid(),
  class_id uuid references classes(id),
  title text not null,
  type text,
  due_date date not null,
  file_url text,
  shared_with_parents boolean default true,
  created_at timestamptz default now()
);

create table notification_log (
  assignment_id uuid references assignments(id),
  parent_id uuid references profiles(id),
  sent_at timestamptz default now(),
  primary key (assignment_id, parent_id)
);