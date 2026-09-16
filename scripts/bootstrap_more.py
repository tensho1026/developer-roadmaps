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


def pkg(name: str, scripts: dict, deps=None, dev=None) -> str:
    data = {"name": name, "private": True, "version": "0.1.0", "type": "module", "scripts": scripts}
    if deps:
        data["dependencies"] = {d: "*" for d in deps}
    if dev:
        data["devDependencies"] = {d: "*" for d in dev}
    return json.dumps(data, indent=2) + "\n"


# ---------------------------------------------------------------------------
# front remaining: graphql, electron, playwright, biome
# ---------------------------------------------------------------------------
write(
    "front/graphql/package.json",
    pkg(
        "front-graphql",
        {"dev": "vite --port 5180", "build": "vite build"},
        deps=["react", "react-dom", "graphql", "@apollo/client", "urql"],
        dev=["typescript", "vite", "@vitejs/plugin-react", "@types/react", "@types/react-dom"],
    ),
)
write(
    "front/graphql/index.html",
    """<!doctype html>
<html lang="ja"><head><meta charset="UTF-8" /><title>GraphQL</title></head>
<body><div id="root"></div><script type="module" src="/src/main.tsx"></script></body></html>
""",
)
write("front/graphql/vite.config.ts", """import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
export default defineConfig({ plugins: [react()] });
""")
write(
    "front/graphql/tsconfig.json",
    """{"compilerOptions":{"target":"ES2022","module":"ESNext","moduleResolution":"bundler","jsx":"react-jsx","strict":true,"skipLibCheck":true,"noEmit":true,"lib":["ES2022","DOM"]},"include":["src"]}""",
)
write(
    "front/graphql/src/main.tsx",
    """import { ApolloClient, ApolloProvider, InMemoryCache, gql, useQuery } from "@apollo/client";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

const client = new ApolloClient({
  uri: "https://countries.trevorblades.com/",
  cache: new InMemoryCache(),
});

const QUERY = gql`
  query {
    country(code: "JP") {
      name
      capital
    }
  }
`;

function Country() {
  const { data, loading, error } = useQuery(QUERY);
  if (loading) return <p>loading...</p>;
  if (error) return <p>{error.message}</p>;
  return (
    <main style={{ padding: 24 }}>
      <h1>GraphQL / Apollo</h1>
      <p>
        {data.country.name} / {data.country.capital}
      </p>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ApolloProvider client={client}>
      <Country />
    </ApolloProvider>
  </StrictMode>,
);
""",
)
write("front/graphql/README.md", "# GraphQL\n\nApollo Client。`npm run dev` → http://localhost:5180\n")

write(
    "front/electron/package.json",
    pkg(
        "front-electron",
        {"start": "electron .", "dev": "electron ."},
        deps=["electron"],
    ),
)
write(
    "front/electron/main.cjs",
    """const { app, BrowserWindow } = require("electron");

const createWindow = () => {
  const win = new BrowserWindow({ width: 900, height: 700 });
  win.loadFile("index.html");
};

app.whenReady().then(createWindow);
""",
)
write(
    "front/electron/index.html",
    """<!doctype html>
<html><head><meta charset="utf-8" /><title>Electron</title></head>
<body><h1>Electron playground</h1><p>Frontend roadmap: Desktop Apps</p></body></html>
""",
)
write("front/electron/README.md", "# Electron\n\n`npm start`\n")

write(
    "front/playwright/package.json",
    pkg(
        "front-playwright",
        {"test": "playwright test", "test:ui": "playwright test --ui"},
        dev=["@playwright/test"],
    ),
)
write(
    "front/playwright/playwright.config.ts",
    """import { defineConfig } from "@playwright/test";
export default defineConfig({
  testDir: "./tests",
  use: { headless: true },
});
""",
)
write(
    "front/playwright/tests/example.spec.ts",
    """import { test, expect } from "@playwright/test";
test("example.com has title", async ({ page }) => {
  await page.goto("https://example.com");
  await expect(page).toHaveTitle(/Example/);
});
""",
)
write(
    "front/playwright/README.md",
    """# Playwright / Cypress 相当の E2E

ブラウザバイナリはリポジトリに含めません。初回だけ:

```bash
npx playwright install chromium
npm test
```
""",
)

write(
    "front/tooling/package.json",
    pkg(
        "front-tooling",
        {"lint": "eslint .", "format": "prettier --check .", "check": "biome check ."},
        dev=["eslint", "prettier", "@eslint/js", "typescript", "typescript-eslint", "@biomejs/biome"],
    ),
)
write("front/tooling/README.md", "# Linters & Formatters\n\nESLint / Prettier / Biome（Frontend ロードマップ）。\n")
write("front/tooling/eslint.config.js", """import js from "@eslint/js";
export default [js.configs.recommended];
""")
write("front/tooling/.prettierrc", '{ "singleQuote": true }\\n'.replace("\\\\n", "\n") if False else '{\n  "singleQuote": true\n}\n')
write("front/tooling/biome.json", """{"$schema":"https://biomejs.dev/schemas/2.2.0/schema.json","linter":{"enabled":true},"formatter":{"enabled":true}}""")

# ---------------------------------------------------------------------------
# fullstack
# ---------------------------------------------------------------------------
write(
    "fullstack/app/package.json",
    pkg(
        "fullstack-app",
        {"dev": "tsx watch src/server.ts", "start": "tsx src/server.ts"},
        deps=["express", "cors", "jsonwebtoken", "pg", "redis", "zod", "dotenv", "bcryptjs"],
        dev=["typescript", "tsx", "@types/node", "@types/express", "@types/cors", "@types/jsonwebtoken", "@types/bcryptjs"],
    ),
)
write(
    "fullstack/app/tsconfig.json",
    """{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "outDir": "dist",
    "rootDir": "src"
  },
  "include": ["src"]
}
""",
)
write(
    "fullstack/app/.env.example",
    """PORT=3010
JWT_SECRET=dev-only-change-me
DATABASE_URL=postgresql://roadmaps:roadmaps@localhost:5432/roadmaps
REDIS_URL=redis://localhost:6379
""",
)
write(
    "fullstack/app/src/server.ts",
    """import "dotenv/config";
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
""",
)
write(
    "fullstack/app/public/index.html",
    """<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Full Stack playground</title>
  <style>
    :root { font-family: system-ui, sans-serif; }
    body { max-width: 40rem; margin: 2rem auto; }
    label, input, button { display: block; width: 100%; margin-top: 0.5rem; }
    input, button { font: inherit; padding: 0.5rem; }
    pre { background: #111; color: #eee; padding: 1rem; overflow: auto; }
  </style>
</head>
<body>
  <h1>Full Stack playground</h1>
  <p>HTML / CSS / JS + Node REST + JWT。Postgres / Redis は docker compose で起動。</p>
  <form id="login">
    <label>email <input name="email" type="email" value="ada@example.com" required /></label>
    <label>password <input name="password" type="password" value="password" required /></label>
    <button>ログインして /api/health を叩く</button>
  </form>
  <pre id="out"></pre>
  <script>
    const out = document.querySelector("#out");
    document.querySelector("#login").addEventListener("submit", async (e) => {
      e.preventDefault();
      const body = Object.fromEntries(new FormData(e.target));
      const login = await fetch("/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      }).then((r) => r.json());
      const health = await fetch("/api/health").then((r) => r.json());
      out.textContent = JSON.stringify({ login, health }, null, 2);
    });
  </script>
</body>
</html>
""",
)
write(
    "fullstack/app/README.md",
    """# Full Stack app

[roadmap.sh/full-stack](https://roadmap.sh/full-stack) の一本道を小さな CRUD/JWT アプリにしたものです。

```bash
cp .env.example .env
npm run dev
```
""",
)

write(
    "fullstack/github-actions/.github/workflows/ci.yml",
    """name: fullstack-ci
on:
  push:
    branches: [main]
jobs:
  health-docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: echo "GitHub Actions playground from the full-stack roadmap"
""",
)
write("fullstack/github-actions/README.md", "# GitHub Actions\n\nフルスタックロードマップの CI/CD ノード。実運用の workflow はリポジトリ直下 `.github/workflows` を使います。\n")

write(
    "fullstack/terraform/main.tf",
    """terraform {
  required_version = ">= 1.5.0"
}

output "note" {
  value = "Full-stack roadmap Terraform lab. Replace with real providers when you have cloud credentials."
}
""",
)
write("fullstack/terraform/README.md", "# Terraform\n\nフルスタックロードマップの IaC。資格情報は入れないこと。\n")

write(
    "fullstack/ansible/playbook.yml",
    """---
- name: Full-stack roadmap ansible lab
  hosts: localhost
  connection: local
  gather_facts: false
  tasks:
    - name: Ping locally
      ansible.builtin.debug:
        msg: "Ansible is ready"
""",
)
write("fullstack/ansible/README.md", "# Ansible\n\n`ansible-playbook playbook.yml`\n")

# ---------------------------------------------------------------------------
# iOS
# ---------------------------------------------------------------------------
write(
    "ios/Package.swift",
    """// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "IosPlayground",
    platforms: [
        .iOS(.v17),
        .macOS(.v14)
    ],
    products: [
        .library(name: "IosPlayground", targets: ["IosPlayground"])
    ],
    dependencies: [
        .package(url: "https://github.com/Alamofire/Alamofire.git", from: "5.10.0")
    ],
    targets: [
        .target(
            name: "IosPlayground",
            dependencies: ["Alamofire"]
        ),
        .testTarget(
            name: "IosPlaygroundTests",
            dependencies: ["IosPlayground"]
        )
    ]
)
""",
)
write(
    "ios/Sources/IosPlayground/Networking.swift",
    """import Foundation
#if canImport(Alamofire)
import Alamofire
#endif

public struct RemoteTodo: Decodable, Sendable {
    public let id: Int
    public let title: String
}

public enum RoadmapNetworking {
    public static func sampleURL() -> URL {
        URL(string: "https://jsonplaceholder.typicode.com/todos/1")!
    }

    public static func fetchTodo() async throws -> RemoteTodo {
        let (data, _) = try await URLSession.shared.data(from: sampleURL())
        return try JSONDecoder().decode(RemoteTodo.self, from: data)
    }
}
""",
)
write(
    "ios/Sources/IosPlayground/Persistence.swift",
    """import Foundation

public enum RoadmapPersistence {
    public static func savePreviewName(_ name: String) {
        UserDefaults.standard.set(name, forKey: "previewName")
    }

    public static func previewName() -> String? {
        UserDefaults.standard.string(forKey: "previewName")
    }
}
""",
)
write(
    "ios/Sources/IosPlayground/SwiftUISamples.swift",
    """import SwiftUI

public struct CounterView: View {
    @State private var count = 0

    public init() {}

    public var body: some View {
        VStack(spacing: 16) {
            Text("iOS playground")
                .font(.title)
            Text("count: \\(count)")
            Button("Increment") { count += 1 }
        }
        .padding()
    }
}
""",
)
write(
    "ios/Tests/IosPlaygroundTests/IosPlaygroundTests.swift",
    """import XCTest
@testable import IosPlayground

final class IosPlaygroundTests: XCTestCase {
    func testSampleURL() {
        XCTAssertEqual(RoadmapNetworking.sampleURL().host, "jsonplaceholder.typicode.com")
    }
}
""",
)
write(
    "ios/.swiftlint.yml",
    """opt_in_rules:
  - empty_count
excluded:
  - .build
""",
)
write(
    "ios/fastlane/Fastfile",
    """default_platform(:ios)

platform :ios do
  desc "Run Swift package tests"
  lane :tests do
    sh("cd .. && swift test")
  end
end
""",
)
write(
    "ios/README.md",
    """# iOS

[roadmap.sh/ios](https://roadmap.sh/ios) 向けの Swift Package。

- Swift / SwiftUI / URLSession / Alamofire / UserDefaults / XCTest / SwiftLint / Fastlane / SPM

Xcode でこの `ios` フォルダを開くか:

```bash
cd ios
swift build
swift test
```

UIKit / Core Data / Combine は Xcode の iOS App テンプレートにこの Package を追加して使います。
""",
)

# ---------------------------------------------------------------------------
# GitHub Actions at repo root (fullstack CI node)
# ---------------------------------------------------------------------------
write(
    ".github/workflows/ci.yml",
    """name: ci
on:
  push:
    branches: [main]
  pull_request:
jobs:
  node-health:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "22"
      - name: Install express playground
        working-directory: back/express
        run: npm install
      - name: Typecheck express
        working-directory: back/express
        run: npx tsc --noEmit
""",
)

print("fullstack ios extra front done")
