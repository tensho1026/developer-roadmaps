# PostgreSQL

[roadmap.sh/postgresql-dba](https://roadmap.sh/postgresql-dba) の実習環境です。

## 起動

リポジトリルートで:

```bash
docker compose up -d postgres
psql "postgresql://roadmaps:roadmaps@localhost:5432/roadmaps"
```

初期スキーマは `init/001_schema.sql` がコンテナ初回起動時に入ります。

## 含まれる実習

| ファイル | ロードマップ上のテーマ |
| --- | --- |
| `init/001_schema.sql` | スキーマ、テーブル、JSONB、配列、GIN、パーティション、拡張 |
| `sql/02_queries.sql` | JOIN、CTE、Window、LATERAL、EXPLAIN |
| `sql/03_plpgsql.sql` | 関数、トリガー、プロシージャ |
| `sql/04_security.sql` | ロール、GRANT、Row Level Security |

`pg_dump` / `pg_restore` は Docker 内の `postgres` イメージでそのまま使えます。
