import "dotenv/config";
import amqp from "amqplib";
import cors from "cors";
import express from "express";
import { z } from "zod";

const app = express();
const port = Number(process.env.PORT ?? 3031);
const rabbitUrl = process.env.RABBITMQ_URL ?? "amqp://roadmaps:roadmaps@localhost:5672";
const QUEUE = "roadmaps.notes";

type AmqpConnection = Awaited<ReturnType<typeof amqp.connect>>;
type AmqpChannel = Awaited<ReturnType<AmqpConnection["createChannel"]>>;

app.use(cors());
app.use(express.json());

const Publish = z.object({ message: z.string().min(1) });
const received: { message: string; at: number }[] = [];

let channel: AmqpChannel | null = null;
let connecting: Promise<AmqpChannel | null> | null = null;

async function connectRabbit(): Promise<AmqpChannel | null> {
  if (channel) return channel;
  if (connecting) return connecting;

  connecting = (async () => {
    try {
      const connection = await amqp.connect(rabbitUrl, { timeout: 3000 });
      connection.on("error", (err) => {
        console.warn("rabbitmq:", err.message);
      });
      connection.on("close", () => {
        channel = null;
        console.warn("rabbitmq connection closed");
      });
      const ch = await connection.createChannel();
      await ch.assertQueue(QUEUE, { durable: false });
      await ch.consume(QUEUE, (msg) => {
        if (!msg) return;
        const text = msg.content.toString();
        received.push({ message: text, at: Date.now() });
        console.log("consumed:", text);
        ch.ack(msg);
      });
      channel = ch;
      console.log("rabbitmq connected");
      return ch;
    } catch (error) {
      console.warn("rabbitmq not connected:", error);
      return null;
    } finally {
      connecting = null;
    }
  })();

  return connecting;
}

app.get("/health", (_req, res) => {
  const rabbit = channel !== null;
  res.status(rabbit ? 200 : 503).json({
    ok: rabbit,
    rabbitmq: rabbit,
    received: received.length,
  });
});

app.get("/received", (_req, res) => {
  res.json({ count: received.length, messages: received });
});

app.post("/publish", async (req, res) => {
  const parsed = Publish.safeParse(req.body);
  if (!parsed.success) {
    res.status(400).json(parsed.error.flatten());
    return;
  }
  const ch = (await connectRabbit()) ?? channel;
  if (!ch) {
    res.status(503).json({ error: "rabbitmq not connected" });
    return;
  }
  ch.sendToQueue(QUEUE, Buffer.from(parsed.data.message));
  res.status(202).json({ queued: true, queue: QUEUE, message: parsed.data.message });
});

async function main() {
  await connectRabbit();
  app.listen(port, () => {
    console.log(`rabbitmq lab on http://localhost:${port}`);
  });
}

void main();
