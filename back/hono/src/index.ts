import { serve } from "@hono/node-server";
import { Hono } from "hono";
import { cors } from "hono/cors";
import { logger } from "hono/logger";
import { zValidator } from "@hono/zod-validator";
import { z } from "zod";

const app = new Hono();
app.use("*", logger());
app.use("*", cors());

app.get("/health", (c) => c.json({ ok: true, framework: "hono" }));

app.post(
  "/echo",
  zValidator("json", z.object({ message: z.string() })),
  (c) => c.json({ echo: c.req.valid("json").message }),
);

serve({ fetch: app.fetch, port: 3003 }, (info) => {
  console.log(`hono listening on http://localhost:${info.port}`);
});
