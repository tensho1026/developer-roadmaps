import Fastify from "fastify";
import cors from "@fastify/cors";

const app = Fastify({ logger: true });
await app.register(cors, { origin: true });

app.get("/health", async () => ({ ok: true, framework: "fastify" }));

app.post<{ Body: { message: string } }>("/echo", async (req) => ({ echo: req.body.message }));

await app.listen({ port: 3004, host: "0.0.0.0" });
