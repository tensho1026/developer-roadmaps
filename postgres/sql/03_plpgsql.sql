SET search_path TO lab, public;

CREATE OR REPLACE FUNCTION lab.slugify(input TEXT)
RETURNS TEXT
LANGUAGE plpgsql
IMMUTABLE
AS $$
BEGIN
  RETURN lower(regexp_replace(input, '[^a-zA-Z0-9]+', '-', 'g'));
END;
$$;

CREATE OR REPLACE FUNCTION lab.touch_post()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
  NEW.metadata = COALESCE(NEW.metadata, '{}'::jsonb) || jsonb_build_object('updated_at', now());
  RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS posts_touch ON lab.posts;
CREATE TRIGGER posts_touch
BEFORE UPDATE ON lab.posts
FOR EACH ROW
EXECUTE FUNCTION lab.touch_post();

CREATE OR REPLACE PROCEDURE lab.create_post(p_email TEXT, p_title TEXT, p_body TEXT)
LANGUAGE plpgsql
AS $$
DECLARE
  v_user_id BIGINT;
BEGIN
  SELECT id INTO v_user_id FROM lab.users WHERE email = p_email;
  IF v_user_id IS NULL THEN
    RAISE EXCEPTION 'unknown user %', p_email;
  END IF;
  INSERT INTO lab.posts (user_id, title, body) VALUES (v_user_id, p_title, p_body);
END;
$$;
