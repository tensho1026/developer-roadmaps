# Mongoose + MongoDB

Backend ロードマップの NoSQL（MongoDB）と、Node からよく使う ODM。空なら起動時に 1 件シードします。

```bash
# リポジトリルートで
docker compose up -d mongodb
cp .env.example .env
npm run dev
```

- 一覧: GET http://localhost:3030/notes
- 作成: `POST http://localhost:3030/notes` `{ "title": "hello", "body": "mongoose" }`
- 削除: `DELETE http://localhost:3030/notes/:id`
- ヘルス: GET http://localhost:3030/health
