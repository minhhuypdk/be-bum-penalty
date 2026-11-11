-- Read-only inspection in the SQL Editor of project zzphvbedtxbhajkpavqp.
-- No GRANT, no policy changes, no data writes.
SELECT current_database() AS database_name,
       current_user AS sql_editor_role,
       session_user AS sql_editor_session_role;

SELECT r.rolname AS role_name,
       has_schema_privilege(r.oid, 'public', 'USAGE') AS public_usage,
       has_table_privilege(r.oid, 'public.bebum_penalty_rooms', 'SELECT') AS can_select,
       has_table_privilege(r.oid, 'public.bebum_penalty_rooms', 'INSERT') AS can_insert,
       has_table_privilege(r.oid, 'public.bebum_penalty_rooms', 'UPDATE') AS can_update
FROM pg_roles r
WHERE r.rolname IN ('anon', 'authenticated', 'authenticator')
ORDER BY r.rolname;

SELECT n.nspname AS schema_name, c.relname AS relation_name,
       c.relkind AS relation_kind, pg_get_userbyid(c.relowner) AS owner,
       c.relrowsecurity AS rls_enabled,
       c.relforcerowsecurity AS rls_forced
FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname = 'public' AND c.relname = 'bebum_penalty_rooms';

SELECT policyname, permissive, roles, cmd, qual, with_check
FROM pg_policies
WHERE schemaname = 'public' AND tablename = 'bebum_penalty_rooms'
ORDER BY policyname;

SELECT grantee, privilege_type
FROM information_schema.role_table_grants
WHERE table_schema = 'public' AND table_name = 'bebum_penalty_rooms'
ORDER BY grantee, privilege_type;

-- Test PostgreSQL's effective anon role without modifying any room.
-- If a policy depends on request claims, HTTP tests remain authoritative.
BEGIN READ ONLY;
SET LOCAL ROLE anon;
SELECT current_user AS effective_role,
       has_schema_privilege(current_user, 'public', 'USAGE') AS public_usage;
SELECT room_id FROM public.bebum_penalty_rooms WHERE room_id = 'ba-bum';
ROLLBACK;
