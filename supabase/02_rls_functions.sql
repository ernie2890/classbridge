create function is_teacher_of(cid uuid) returns boolean
language sql security definer stable set search_path = public as $$
  select exists (select 1 from classes
                 where id = cid and teacher_id = auth.uid());
$$;

create function parent_has_class(cid uuid) returns boolean
language sql security definer stable set search_path = public as $$
  select exists (select 1 from enrollments e
                 join parent_students ps on ps.student_id = e.student_id
                 where e.class_id = cid and ps.parent_id = auth.uid());
$$;

create function is_parent_of(sid uuid) returns boolean
language sql security definer stable set search_path = public as $$
  select exists (select 1 from parent_students
                 where student_id = sid and parent_id = auth.uid());
$$;

create function teaches_student(sid uuid) returns boolean
language sql security definer stable set search_path = public as $$
  select exists (select 1 from enrollments e
                 join classes c on c.id = e.class_id
                 where e.student_id = sid and c.teacher_id = auth.uid());
$$;