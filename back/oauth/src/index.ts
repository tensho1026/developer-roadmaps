import { randomBytes } from "node:crypto";
import express from "express";
import jwt from "jsonwebtoken";

const app = express();
app.use(express.urlencoded({ extended: false }));
app.use(express.json());

const codes = new Map<string, { clientId: string; redirectUri: string }>();
const CLIENT_ID = "roadmaps-lab";
const CLIENT_SECRET = "roadmaps-secret";
const ISSUER_SECRET = "oauth-lab-signing-key";

app.get("/", (_req, res) => {
  res.type("html").send(`<!doctype html>
<html lang="ja"><body style="font-family:system-ui;max-width:40rem;margin:2rem auto">
  <h1>OAuth 2.0 Authorization Code lab</h1>
  <p>GitHub アプリなしで code flow を体験します。</p>
  <a href="/login">ログインを開始</a>
</body></html>`);
});

app.get("/login", (_req, res) => {
  const state = randomBytes(8).toString("hex");
  const redirect = encodeURIComponent("http://localhost:3022/callback");
  res.redirect(`/oauth/authorize?client_id=${CLIENT_ID}&redirect_uri=${redirect}&state=${state}`);
});

app.get("/oauth/authorize", (req, res) => {
  const redirectUri = String(req.query.redirect_uri ?? "");
  const clientId = String(req.query.client_id ?? "");
  const state = String(req.query.state ?? "");
  res.type("html").send(`<!doctype html>
<html lang="ja"><body style="font-family:system-ui;max-width:40rem;margin:2rem auto">
  <h1>認可サーバー</h1>
  <p>アプリ <code>${clientId}</code> がプロフィール読み取りを求めています。</p>
  <form method="post" action="/oauth/authorize">
    <input type="hidden" name="redirect_uri" value="${redirectUri}" />
    <input type="hidden" name="client_id" value="${clientId}" />
    <input type="hidden" name="state" value="${state}" />
    <button>許可する</button>
  </form>
</body></html>`);
});

app.post("/oauth/authorize", (req, res) => {
  const code = randomBytes(12).toString("hex");
  const redirectUri = String(req.body.redirect_uri);
  const clientId = String(req.body.client_id);
  const state = String(req.body.state);
  codes.set(code, { clientId, redirectUri });
  const url = new URL(redirectUri);
  url.searchParams.set("code", code);
  url.searchParams.set("state", state);
  res.redirect(url.toString());
});

app.post("/oauth/token", (req, res) => {
  const { code, client_id, client_secret } = req.body as Record<string, string>;
  const saved = codes.get(code);
  if (!saved || client_id !== CLIENT_ID || client_secret !== CLIENT_SECRET) {
    res.status(400).json({ error: "invalid_grant" });
    return;
  }
  codes.delete(code);
  res.json({
    token_type: "Bearer",
    access_token: jwt.sign({ sub: "ada@example.com", provider: "lab" }, ISSUER_SECRET, {
      expiresIn: "1h",
    }),
  });
});

app.get("/callback", async (req, res) => {
  const code = String(req.query.code ?? "");
  const tokenRes = await fetch("http://localhost:3022/oauth/token", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      code,
      client_id: CLIENT_ID,
      client_secret: CLIENT_SECRET,
    }),
  });
  const token = await tokenRes.json();
  res.type("html").send(`<!doctype html>
<html lang="ja"><body style="font-family:system-ui;max-width:40rem;margin:2rem auto">
  <h1>コールバック</h1>
  <pre>${JSON.stringify(token, null, 2)}</pre>
</body></html>`);
});

app.listen(3022, () => {
  console.log("oauth lab on http://localhost:3022");
});
