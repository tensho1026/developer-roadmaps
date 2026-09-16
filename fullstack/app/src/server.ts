import "dotenv/config";
import bcrypt from "bcryptjs";
import cors from "cors";
import express from "express";
import jwt from "jsonwebtoken";
import pg from "pg";
import { createClient } from "redis";
import { z } from "zod";

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static(new URL("../public", import.meta.url).pathname));

const secret = process.env.JWT_SECRET ?? "dev-only-change-me";
const databaseUrl =
  process.env.DATABASE_URL ?? "postgresql://roadmaps:roadmaps@localhost:5432/roadmaps";
const redisUrl = process.env.REDIS_URL ?? "redis://localhost:6379";

const pool = new pg.Pool({ connectionString: databaseUrl });
const redis = createClient({ url: redisUrl });
redis.on("error", (err) => {
  console.warn("redis:", err.message);
});

const Login = z.object({ email: z.string().email(), password: z.string().min(4) });
const NoteBody = z.object({ body: z.string().min(1) });

async function ensureSchema() {
  await pool.query(`
    CREATE SCHEMA IF NOT EXISTS app;
    CREATE TABLE IF NOT EXISTS app.users (
      id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
      email TEXT UNIQUE NOT NULL,
      password_hash TEXT NOT NULL,
      created_at TIMESTAMPTZ NOT NULL DEFAULT now()
    );
    CREATE TABLE IF NOT EXISTS app.notes (
      id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
      user_id BIGINT NOT NULL REFERENCES app.users(id) ON DELETE CASCADE,
      body TEXT NOT NULL,
      created_at TIMESTAMPTZ NOT NULL DEFAULT now()
    );
  `);
  const existing = await pool.query("SELECT id FROM app.users WHERE email = $1", [
    "ada@example.com",
  ]);
  if (existing.rowCount === 0) {
    const passwordHash = await bcrypt.hash("password", 10);
    await pool.query("INSERT INTO app.users (email, password_hash) VALUES ($1, $2)", [
      "ada@example.com",
      passwordHash,
    ]);
  }
}

function auth(req: express.Request, res: express.Response, next: express.NextFunction) {
  const header = req.header("authorization");
  if (!header?.startsWith("Bearer ")) {
    res.status(401).json({ error: "missing token" });
    return;
  }
  try {
    const payload = jwt.verify(header.slice(7), secret) as { sub: string; uid: number };
    res.locals.user = payload;
    next();
  } catch {
    res.status(401).json({ error: "invalid token" });
  }
}

app.get("/api/health", async (_req, res) => {
  let postgres = false;
  let redisOk = false;
  try {
    await pool.query("SELECT 1");
    postgres = true;
  } catch {
    postgres = false;
  }
  try {
    if (redis.isOpen) {
      await redis.ping();
      redisOk = true;
    }
  } catch {
    redisOk = false;
  }
  res.json({
    ok: postgres,
    postgres,
    redis: redisOk,
    stack: ["html", "css", "javascript", "node", "jwt", "postgresql", "redis"],
  });
});

app.post("/api/login", async (req, res) => {
  const parsed = Login.safeParse(req.body);
  if (!parsed.success) {
    res.status(400).json(parsed.error.flatten());
    return;
  }
  const found = await pool.query("SELECT id, email, password_hash FROM app.users WHERE email = $1", [
    parsed.data.email,
  ]);
  const user = found.rows[0] as { id: string; email: string; password_hash: string } | undefined;
  if (!user || !(await bcrypt.compare(parsed.data.password, user.password_hash))) {
    res.status(401).json({ error: "invalid credentials" });
    return;
  }
  const token = jwt.sign({ sub: user.email, uid: Number(user.id) }, secret, { expiresIn: "2h" });
  await redis.set(`session:${user.id}`, token, { EX: 60 * 60 * 2 }).catch(() => undefined);
  res.json({ token, email: user.email });
});

app.get("/api/notes", auth, async (_req, res) => {
  const uid = res.locals.user.uid as number;
  const cacheKey = `notes:${uid}`;
  const cached = await redis.get(cacheKey).catch(() => null);
  if (cached) {
    res.json({ source: "redis", notes: JSON.parse(cached) });
    return;
  }
  const result = await pool.query(
    "SELECT id, body, created_at FROM app.notes WHERE user_id = $1 ORDER BY id DESC",
    [uid],
  );
  await redis.set(cacheKey, JSON.stringify(result.rows), { EX: 30 }).catch(() => undefined);
  res.json({ source: "postgres", notes: result.rows });
});

app.post("/api/notes", auth, async (req, res) => {
  const parsed = NoteBody.safeParse(req.body);
  if (!parsed.success) {
    res.status(400).json(parsed.error.flatten());
    return;
  }
  const uid = res.locals.user.uid as number;
  const inserted = await pool.query(
    "INSERT INTO app.notes (user_id, body) VALUES ($1, $2) RETURNING id, body, created_at",
    [uid, parsed.data.body],
  );
  await redis.del(`notes:${uid}`).catch(() => undefined);
  res.status(201).json(inserted.rows[0]);
});

const port = Number(process.env.PORT ?? 3010);

async function main() {
  try {
    await redis.connect();
  } catch (error) {
    console.warn("redis not connected:", error);
  }
  try {
    await ensureSchema();
  } catch (error) {
    console.warn("postgres schema skipped:", error);
  }
  app.listen(port, () => {
    console.log(`fullstack app on http://localhost:${port}`);
  });
}

main();
