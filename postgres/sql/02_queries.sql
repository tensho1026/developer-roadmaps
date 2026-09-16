-- DML / advanced SQL from the PostgreSQL DBA roadmap
SET search_path TO lab, public;

-- Filtering / joining
SELECT u.display_name, p.title, p.created_at
FROM users u
JOIN posts p ON p.user_id = u.id
WHERE p.created_at >= now() - INTERVAL '30 days'
ORDER BY p.created_at DESC;

-- CTE + window functions
WITH ranked AS (
  SELECT
    p.*,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at DESC) AS rn,
    COUNT(*) OVER (PARTITION BY user_id) AS post_count
  FROM posts p
)
SELECT * FROM ranked WHERE rn = 1;

-- JSONB + arrays
SELECT title, tags, metadata->>'source' AS source
FROM posts
WHERE tags @> ARRAY['postgres']
  AND metadata @> '{"source":"init"}'::jsonb;

-- Set operations
SELECT email FROM users
EXCEPT
SELECT 'nobody@example.com';

-- Lateral
SELECT u.display_name, recent.title
FROM users u
LEFT JOIN LATERAL (
  SELECT title FROM posts p
  WHERE p.user_id = u.id
  ORDER BY created_at DESC
  LIMIT 1
) recent ON true;

-- Transactions (run as a block)
BEGIN;
  UPDATE users SET display_name = display_name || ' *' WHERE id = 1;
ROLLBACK;

EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM posts WHERE user_id = 1;
