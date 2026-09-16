-- Roles, privileges, RLS (PostgreSQL DBA roadmap: Security)
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'lab_app') THEN
    CREATE ROLE lab_app LOGIN PASSWORD 'lab_app';
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'lab_reader') THEN
    CREATE ROLE lab_reader LOGIN PASSWORD 'lab_reader';
  END IF;
END;
$$;

GRANT USAGE ON SCHEMA lab TO lab_app, lab_reader;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA lab TO lab_app;
GRANT SELECT ON ALL TABLES IN SCHEMA lab TO lab_reader;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA lab TO lab_app;

ALTER TABLE lab.posts ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS posts_owner_write ON lab.posts;
CREATE POLICY posts_owner_write ON lab.posts
  FOR ALL
  TO lab_app
  USING (true)
  WITH CHECK (true);

DROP POLICY IF EXISTS posts_reader_select ON lab.posts;
CREATE POLICY posts_reader_select ON lab.posts
  FOR SELECT
  TO lab_reader
  USING (true);
