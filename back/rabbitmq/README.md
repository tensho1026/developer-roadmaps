# RabbitMQ

Backend ロードマップのメッセージブローカー。HTTP から publish し、同じプロセスの consumer が受け取って記録します。RabbitMQ が落ちていてもプロセスは落ちません。

```bash
# リポジトリルートで
docker compose up -d rabbitmq
cp .env.example .env
npm run dev
```

- 送信: `POST http://localhost:3031/publish` `{ "message": "hello" }`
- 受信一覧: GET http://localhost:3031/received
- ヘルス: GET http://localhost:3031/health
- 管理 UI: http://localhost:15672 （user/pass は `roadmaps`）
