import { createServer } from "node:http";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import express from "express";
import { WebSocketServer } from "ws";

const app = express();
app.use(express.static(join(dirname(fileURLToPath(import.meta.url)), "../public")));

const clients = new Set<express.Response>();

app.get("/sse", (req, res) => {
  res.setHeader("Content-Type", "text/event-stream");
  res.setHeader("Cache-Control", "no-cache");
  res.setHeader("Connection", "keep-alive");
  res.flushHeaders();
  clients.add(res);
  res.write(`data: ${JSON.stringify({ type: "hello", at: Date.now() })}\n\n`);
  req.on("close", () => clients.delete(res));
});

app.get("/health", (_req, res) => {
  res.json({ ok: true, websocket: true, sse: true });
});

const server = createServer(app);
const wss = new WebSocketServer({ server, path: "/ws" });

wss.on("connection", (socket) => {
  socket.send(JSON.stringify({ type: "hello", via: "websocket" }));
  socket.on("message", (raw) => {
    const text = String(raw);
    const payload = JSON.stringify({ type: "echo", text, at: Date.now() });
    for (const peer of wss.clients) {
      if (peer.readyState === peer.OPEN) peer.send(payload);
    }
    for (const sse of clients) {
      sse.write(`data: ${payload}\n\n`);
    }
  });
});

server.listen(3021, () => {
  console.log("realtime (ws + sse) on http://localhost:3021");
});
