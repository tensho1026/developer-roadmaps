-- roadmap.sh/postgresql-dba lab schema
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE SCHEMA IF NOT EXISTS lab;

CREATE TABLE lab.users (
  id           BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  email        TEXT NOT NULL UNIQUE,
  display_name TEXT NOT NULL,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE lab.posts (
  id         BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  user_id    BIGINT NOT NULL REFERENCES lab.users(id),
  title      TEXT NOT NULL,
  body       TEXT NOT NULL,
  tags       TEXT[] NOT NULL DEFAULT '{}',
  metadata   JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX posts_user_id_idx ON lab.posts (user_id);
CREATE INDEX posts_created_at_idx ON lab.posts (created_at DESC);
CREATE INDEX posts_tags_gin ON lab.posts USING GIN (tags);
CREATE INDEX posts_metadata_gin ON lab.posts USING GIN (metadata);

CREATE TABLE lab.events (
  id         BIGINT GENERATED ALWAYS AS IDENTITY,
  occurred_at DATE NOT NULL,
  payload    JSONB NOT NULL,
  PRIMARY KEY (id, occurred_at)
) PARTITION BY RANGE (occurred_at);

CREATE TABLE lab.events_2026 PARTITION OF lab.events
  FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');

INSERT INTO lab.users (email, display_name) VALUES
  ('ada@example.com', 'Ada'),
  ('grace@example.com', 'Grace');

INSERT INTO lab.posts (user_id, title, body, tags, metadata)
SELECT id, 'Hello PostgreSQL', 'Roadmap lab post', ARRAY['postgres','sql'], '{"source":"init"}'::jsonb
FROM lab.users
WHERE email = 'ada@example.com';
