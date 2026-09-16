# gRPC

Backend ロードマップの gRPC。Protocol Buffers で `ListNotes` / `AddNote` の unary RPC を動かします。Docker は不要です。

```bash
npm run dev
```

別ターミナル:

```bash
npm run client
```

- サーバー: `localhost:50051`
- proto: `proto/notes.proto`
