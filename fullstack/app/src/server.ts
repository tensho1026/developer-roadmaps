import "dotenv/config";
import express from "express";
import cors from "cors";
import jwt from "jsonwebtoken";
import { z } from "zod";

const app = express();
app.use(cors());
app.use(express.json());
app.use(express.static(new URL("../public", import.meta.url).pathname));

const secret = process.env.JWT_SECRET ?? "dev-only-change-me";
const Login = z.object({ email: z.string().email(), password: z.string().min(4) });

app.get("/api/health", (_req, res) => {
  res.json({
    ok: true,
    stack: ["html", "css", "javascript", "react-ready", "node", "jwt", "postgresql", "redis"],
  });
});

app.post("/api/login", (req, res) => {
  const parsed = Login.safeParse(req.body);
  if (!parsed.success) {
    res.status(400).json(parsed.error.flatten());
    return;
  }
  res.json({ token: jwt.sign({ sub: parsed.data.email }, secret, { expiresIn: "2h" }) });
});

app.listen(Number(process.env.PORT ?? 3010), () => {
  console.log("fullstack app on http://localhost:3010");
});
