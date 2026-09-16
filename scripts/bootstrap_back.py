#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]


def write(rel: str, content: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    if not content.endswith("\n"):
        content += "\n"
    path.write_text(content)


def pkg(name: str, scripts: dict, deps=None, dev=None, extra=None) -> str:
    data = {"name": name, "private": True, "version": "0.1.0", "type": "module", "scripts": scripts}
    if extra:
        data.update(extra)
    if deps:
        data["dependencies"] = {d: "*" for d in deps}
    if dev:
        data["devDependencies"] = {d: "*" for d in dev}
    return json.dumps(data, indent=2) + "\n"


NODE_TS = """{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "dist",
    "rootDir": "src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src"]
}
"""

# ---------------------------------------------------------------------------
# back/express
# ---------------------------------------------------------------------------
write(
    "back/express/package.json",
    pkg(
        "back-express",
        {"dev": "tsx watch src/index.ts", "start": "tsx src/index.ts", "test": "vitest run"},
        deps=[
            "express",
            "cors",
            "helmet",
            "morgan",
            "winston",
            "dotenv",
            "jsonwebtoken",
            "bcryptjs",
            "pg",
            "zod",
            "axios",
        ],
        dev=["typescript", "tsx", "@types/node", "@types/express", "@types/cors", "@types/jsonwebtoken", "@types/bcryptjs", "@types/morgan", "vitest"],
    ),
)
write("back/express/tsconfig.json", NODE_TS)
write("back/express/.env.example", "PORT=3001\nJWT_SECRET=dev-only-change-me\nDATABASE_URL=postgresql://roadmaps:roadmaps@localhost:5432/roadmaps\n")
write(
    "back/express/src/index.ts",
    """import "dotenv/config";
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
""",
)
write("back/express/README.md", "# Express.js\n\nNode.js ロードマップ。`npm run dev` → http://localhost:3001\n")

# ---------------------------------------------------------------------------
# back/hono
# ---------------------------------------------------------------------------
write(
    "back/hono/package.json",
    pkg(
        "back-hono",
        {"dev": "tsx watch src/index.ts", "start": "tsx src/index.ts"},
        deps=["hono", "@hono/node-server", "@hono/zod-validator", "zod"],
        dev=["typescript", "tsx", "@types/node"],
    ),
)
write("back/hono/tsconfig.json", NODE_TS)
write(
    "back/hono/src/index.ts",
    """import { serve } from "@hono/node-server";
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
""",
)
write("back/hono/README.md", "# Hono\n\n`npm run dev` → http://localhost:3003\n")

# ---------------------------------------------------------------------------
# back/fastify
# ---------------------------------------------------------------------------
write(
    "back/fastify/package.json",
    pkg(
        "back-fastify",
        {"dev": "tsx watch src/index.ts", "start": "tsx src/index.ts"},
        deps=["fastify", "@fastify/cors", "zod"],
        dev=["typescript", "tsx", "@types/node"],
    ),
)
write("back/fastify/tsconfig.json", NODE_TS)
write(
    "back/fastify/src/index.ts",
    """import Fastify from "fastify";
import cors from "@fastify/cors";

const app = Fastify({ logger: true });
await app.register(cors, { origin: true });

app.get("/health", async () => ({ ok: true, framework: "fastify" }));

app.post<{ Body: { message: string } }>("/echo", async (req) => ({ echo: req.body.message }));

await app.listen({ port: 3004, host: "0.0.0.0" });
""",
)
write("back/fastify/README.md", "# Fastify\n\n`npm run dev` → http://localhost:3004\n")

# ---------------------------------------------------------------------------
# back/nest
# ---------------------------------------------------------------------------
write(
    "back/nest/package.json",
    json.dumps(
        {
            "name": "back-nest",
            "private": True,
            "version": "0.1.0",
            "scripts": {
                "dev": "nest start --watch",
                "start": "nest start",
                "build": "nest build",
            },
            "dependencies": {
                "@nestjs/common": "*",
                "@nestjs/core": "*",
                "@nestjs/platform-express": "*",
                "@nestjs/jwt": "*",
                "reflect-metadata": "*",
                "rxjs": "*",
                "class-validator": "*",
                "class-transformer": "*",
            },
            "devDependencies": {
                "@nestjs/cli": "*",
                "@nestjs/schematics": "*",
                "@types/node": "*",
                "typescript": "*",
                "ts-node": "*",
                "tsconfig-paths": "*",
            },
        },
        indent=2,
    )
    + "\n",
)
write(
    "back/nest/tsconfig.json",
    """{
  "compilerOptions": {
    "module": "nodenext",
    "moduleResolution": "nodenext",
    "resolvePackageJsonExports": true,
    "esModuleInterop": true,
    "isolatedModules": true,
    "declaration": true,
    "removeComments": true,
    "emitDecoratorMetadata": true,
    "experimentalDecorators": true,
    "allowSyntheticDefaultImports": true,
    "target": "ES2022",
    "sourceMap": true,
    "outDir": "./dist",
    "baseUrl": "./",
    "incremental": true,
    "skipLibCheck": true,
    "strictNullChecks": true,
    "forceConsistentCasingInFileNames": true,
    "noImplicitAny": false,
    "strictBindCallApply": false,
    "noFallthroughCasesInSwitch": false
  }
}
""",
)
write(
    "back/nest/nest-cli.json",
    """{"$schema":"https://json.schemastore.org/nest-cli","collection":"@nestjs/schematics","sourceRoot":"src","compilerOptions":{"deleteOutDir":true}}""",
)
write(
    "back/nest/src/main.ts",
    """import "reflect-metadata";
import { NestFactory } from "@nestjs/core";
import { AppModule } from "./app.module";

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.enableCors();
  await app.listen(3002);
  console.log("nest listening on http://localhost:3002");
}
bootstrap();
""",
)
write(
    "back/nest/src/app.module.ts",
    """import { Module } from "@nestjs/common";
import { AppController } from "./app.controller";
import { AppService } from "./app.service";

@Module({
  imports: [],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
""",
)
write(
    "back/nest/src/app.controller.ts",
    """import { Controller, Get } from "@nestjs/common";
import { AppService } from "./app.service";

@Controller()
export class AppController {
  constructor(private readonly appService: AppService) {}

  @Get("health")
  health() {
    return this.appService.health();
  }
}
""",
)
write(
    "back/nest/src/app.service.ts",
    """import { Injectable } from "@nestjs/common";

@Injectable()
export class AppService {
  health() {
    return { ok: true, framework: "nest" };
  }
}
""",
)
write("back/nest/README.md", "# NestJS\n\n`npm run dev` → http://localhost:3002\n")

# ---------------------------------------------------------------------------
# back/python
# ---------------------------------------------------------------------------
write(
    "back/python/pyproject.toml",
    """[project]
name = "back-python"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
  "fastapi",
  "uvicorn[standard]",
  "sqlalchemy",
  "psycopg[binary]",
  "pydantic-settings",
  "python-jose[cryptography]",
  "redis",
  "httpx",
  "pytest",
]
""",
)
write(
    "back/python/main.py",
    """from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Python backend playground")


class Echo(BaseModel):
    message: str


@app.get("/health")
def health():
    return {"ok": True, "language": "python", "framework": "fastapi"}


@app.post("/echo")
def echo(body: Echo):
    return {"echo": body.message}
""",
)
write(
    "back/python/README.md",
    """# Python

Backend ロードマップの言語ノード。FastAPI で HTTP API をすぐ起動できます。

```bash
uv sync
uv run uvicorn main:app --reload --port 8000
```
""",
)

# ---------------------------------------------------------------------------
# back/go
# ---------------------------------------------------------------------------
write(
    "back/go/go.mod",
    """module github.com/tensho1026/developer-roadmaps/back/go

go 1.22
""",
)
write(
    "back/go/main.go",
    """package main

import (
	"encoding/json"
	"log"
	"net/http"
)

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("GET /health", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]any{"ok": true, "language": "go"})
	})
	log.Println("go listening on http://localhost:8080")
	log.Fatal(http.ListenAndServe(":8080", mux))
}
""",
)
write("back/go/README.md", "# Go\n\n`go run .` → http://localhost:8080\n")

# ---------------------------------------------------------------------------
# back/java
# ---------------------------------------------------------------------------
write(
    "back/java/App.java",
    """import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;

public class App {
  public static void main(String[] args) throws IOException {
    HttpServer server = HttpServer.create(new InetSocketAddress(8081), 0);
    server.createContext("/health", exchange -> {
      byte[] body = "{\\"ok\\":true,\\"language\\":\\"java\\"}".getBytes(StandardCharsets.UTF_8);
      exchange.getResponseHeaders().add("Content-Type", "application/json");
      exchange.sendResponseHeaders(200, body.length);
      exchange.getResponseBody().write(body);
      exchange.close();
    });
    server.start();
    System.out.println("java listening on http://localhost:8081");
  }
}
""",
)
write(
    "back/java/README.md",
    """# Java

Maven なしでも JDK だけで起動できます。

```bash
javac App.java && java App
```
""",
)

# ---------------------------------------------------------------------------
# back/php
# ---------------------------------------------------------------------------
write(
    "back/php/composer.json",
    """{
  "name": "roadmaps/back-php",
  "require": {
    "slim/slim": "^4.14",
    "slim/psr7": "^1.7"
  }
}
""",
)
write(
    "back/php/public/index.php",
    """<?php
require __DIR__ . '/../vendor/autoload.php';

use Psr\\Http\\Message\\ResponseInterface as Response;
use Psr\\Http\\Message\\ServerRequestInterface as Request;
use Slim\\Factory\\AppFactory;

$app = AppFactory::create();

$app->get('/health', function (Request $request, Response $response) {
    $response->getBody()->write(json_encode(['ok' => true, 'language' => 'php', 'framework' => 'slim']));
    return $response->withHeader('Content-Type', 'application/json');
});

$app->run();
""",
)
write("back/php/README.md", "# PHP\n\n`composer install && php -S localhost:8082 -t public`\n")

# ---------------------------------------------------------------------------
# back/ruby
# ---------------------------------------------------------------------------
write(
    "back/ruby/Gemfile",
    """source "https://rubygems.org"
gem "sinatra"
gem "rackup"
gem "puma"
""",
)
write(
    "back/ruby/app.rb",
    """require "sinatra"
require "json"

set :port, 4567
set :bind, "0.0.0.0"

get "/health" do
  content_type :json
  { ok: true, language: "ruby", framework: "sinatra" }.to_json
end
""",
)
write("back/ruby/README.md", "# Ruby\n\n`bundle install && ruby app.rb`\n")

# ---------------------------------------------------------------------------
# back/csharp
# ---------------------------------------------------------------------------
write(
    "back/csharp/Program.cs",
    """var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();
app.MapGet("/health", () => Results.Json(new { ok = true, language = "csharp" }));
app.Run("http://localhost:5080");
""",
)
write(
    "back/csharp/BackendCSharp.csproj",
    """<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>
</Project>
""",
)
write(
    "back/csharp/README.md",
    """# C#

dotnet SDK 導入後:

```bash
dotnet run
```
""",
)

# ---------------------------------------------------------------------------
# back/rust
# ---------------------------------------------------------------------------
write(
    "back/rust/Cargo.toml",
    """[package]
name = "back-rust"
version = "0.1.0"
edition = "2021"

[dependencies]
axum = "0.8"
tokio = { version = "1", features = ["full"] }
serde_json = "1"
""",
)
write(
    "back/rust/src/main.rs",
    """use axum::{routing::get, Json, Router};
use serde_json::{json, Value};

#[tokio::main]
async fn main() {
    let app = Router::new().route("/health", get(health));
    let listener = tokio::net::TcpListener::bind("0.0.0.0:3006").await.unwrap();
    println!("rust listening on http://localhost:3006");
    axum::serve(listener, app).await.unwrap();
}

async fn health() -> Json<Value> {
    Json(json!({ "ok": true, "language": "rust" }))
}
""",
)
write(
    "back/rust/README.md",
    """# Rust

rustup 導入後:

```bash
cargo run
```
""",
)

print("backend done")
