import "dotenv/config";
import { PrismaClient } from "@prisma/client";
import cors from "cors";
import express from "express";
import { z } from "zod";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const prisma = new PrismaClient();
const app = express();
const port = Number(process.env.PORT ?? 3020);
const spec = JSON.parse(
  readFileSync(join(dirname(fileURLToPath(import.meta.url)), "../openapi.json"), "utf8"),
);

app.use(cors());
app.use(express.json());

const CreateUser = z.object({ email: z.string().email(), name: z.string().min(1) });
const CreatePost = z.object({
  title: z.string().min(1),
  body: z.string().min(1),
  userId: z.number().int(),
});

app.get("/health", async (_req, res) => {
  try {
    await prisma.$queryRaw`SELECT 1`;
    res.json({ ok: true, db: true, orm: "prisma" });
  } catch (error) {
    res.status(503).json({ ok: false, db: false, error: String(error) });
  }
});

app.get("/openapi.json", (_req, res) => res.json(spec));

app.get("/docs", (_req, res) => {
  res.type("html").send(`<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>Prisma CRUD OpenAPI</title>
    <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css" />
  </head>
  <body>
    <div id="swagger"></div>
    <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <script>
      SwaggerUIBundle({ url: "/openapi.json", dom_id: "#swagger" });
    </script>
  </body>
</html>`);
});

app.get("/users", async (_req, res) => {
  res.json(await prisma.user.findMany({ include: { posts: true } }));
});

app.post("/users", async (req, res) => {
  const parsed = CreateUser.safeParse(req.body);
  if (!parsed.success) {
    res.status(400).json(parsed.error.flatten());
    return;
  }
  const user = await prisma.user.create({ data: parsed.data });
  res.status(201).json(user);
});

app.get("/posts", async (_req, res) => {
  res.json(await prisma.post.findMany({ include: { user: true } }));
});

app.post("/posts", async (req, res) => {
  const parsed = CreatePost.safeParse(req.body);
  if (!parsed.success) {
    res.status(400).json(parsed.error.flatten());
    return;
  }
  const post = await prisma.post.create({ data: parsed.data });
  res.status(201).json(post);
});

app.delete("/posts/:id", async (req, res) => {
  await prisma.post.delete({ where: { id: Number(req.params.id) } });
  res.status(204).end();
});

app.listen(port, () => {
  console.log(`prisma crud on http://localhost:${port}`);
  console.log(`openapi docs on http://localhost:${port}/docs`);
});
