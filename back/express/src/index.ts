import "dotenv/config";
import express from "express";
import cors from "cors";
import helmet from "helmet";
import morgan from "morgan";
import jwt from "jsonwebtoken";
import { z } from "zod";

const app = express();
const port = Number(process.env.PORT ?? 3001);
const secret = process.env.JWT_SECRET ?? "dev-only-change-me";

app.use(cors());
app.use(helmet());
app.use(morgan("dev"));
app.use(express.json());

const Login = z.object({ email: z.string().email(), password: z.string().min(4) });

app.get("/health", (_req, res) => {
  res.json({ ok: true, framework: "express" });
});

app.post("/auth/login", (req, res) => {
  const parsed = Login.safeParse(req.body);
  if (!parsed.success) {
    res.status(400).json(parsed.error.flatten());
    return;
  }
  const token = jwt.sign({ sub: parsed.data.email }, secret, { expiresIn: "1h" });
  res.json({ token });
});

app.get("/auth/me", (req, res) => {
  const header = req.header("authorization");
  if (!header?.startsWith("Bearer ")) {
    res.status(401).json({ error: "missing token" });
    return;
  }
  try {
    const payload = jwt.verify(header.slice(7), secret);
    res.json({ user: payload });
  } catch {
    res.status(401).json({ error: "invalid token" });
  }
});

app.listen(port, () => {
  console.log(`express listening on http://localhost:${port}`);
});
