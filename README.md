# developer-roadmaps

[roadmap.sh](https://roadmap.sh/) の **Frontend / Backend / Full Stack / PostgreSQL DBA / iOS** に出てくる言語・フレームワーク・ライブラリを、すぐ触れる形で置いた学習用リポジトリです。

出典: [Frontend](https://roadmap.sh/frontend) / [Backend](https://roadmap.sh/backend) / [Full Stack](https://roadmap.sh/full-stack) / [PostgreSQL DBA](https://roadmap.sh/postgresql-dba) / [iOS](https://roadmap.sh/ios)（Node 系フレームワークは [Node.js](https://roadmap.sh/nodejs) も参照）

## いちばん先にやること

```bash
cp .env.example .env
docker compose up -d postgres redis
./scripts/install-all.sh
```

各ディレクトリの起動コマンドは下の [ディレクトリと起動方法](#ディレクトリと起動方法) を見てください。ロードマップ上のノードとの対応は [TECH_MAP.md](./TECH_MAP.md) です。

---

## 入っている言語

| 言語 | 場所 | 備考 |
| --- | --- | --- |
| HTML | `front/html-css-js`, `fullstack/app/public` | マークアップ |
| CSS | `front/html-css-js`, Tailwind を使う各 front プロジェクト | スタイル |
| JavaScript | `front/html-css-js`, `fullstack/app/public` | ブラウザ JS |
| TypeScript | ほぼ全ての Node / フロントプロジェクト | 型付き JS |
| SQL / PL/pgSQL | `postgres/` | PostgreSQL |
| Python | `back/python` | 3.12+ / FastAPI |
| Go | `back/go` | 標準ライブラリ HTTP |
| Java | `back/java` | JDK の `HttpServer` |
| PHP | `back/php` | Slim 4 |
| Ruby | `back/ruby` | Webrick / Sinatra |
| Swift | `ios/` | Swift 6 / iOS 17+ |
| C# | `back/csharp` | ASP.NET Core（`dotnet` SDK が必要） |
| Rust | `back/rust` | Axum（`rustup` が必要） |
| HCL | `fullstack/terraform` | Terraform |
| YAML | `fullstack/ansible`, `.github/workflows` | Ansible / GitHub Actions |
| GraphQL | `front/graphql` | クエリ言語（Apollo / urql） |

---

## 入っているフレームワーク

### フロントエンド UI

| フレームワーク | 場所 | 同梱している関連パッケージ |
| --- | --- | --- |
| **React** | `front/react` | `react`, `react-dom`, `react-router-dom` |
| **Vue.js** | `front/vue` | `vue`, `vue-router`, `pinia` |
| **Angular** | `front/angular` | `@angular/core`, `common`, `compiler`, `forms`, `router`, `platform-browser`, `platform-browser-dynamic`, `rxjs`, `zone.js` |
| **Svelte** | `front/svelte` | `svelte` |
| **Solid JS** | `front/solid` | `solid-js` |

### メタフレームワーク（SSR / SSG）

| フレームワーク | 場所 | 同梱している関連パッケージ |
| --- | --- | --- |
| **Next.js** | `front/next.js` | `next`, `react`, `react-dom`, Tailwind |
| **Nuxt.js** | `front/nuxt` | `nuxt`, `vue`, `vue-router` |
| **SvelteKit** | `front/sveltekit` | `@sveltejs/kit`, `svelte`, `@sveltejs/adapter-auto` |
| **Astro** | `front/astro` | `astro` |

### モバイル / デスクトップ

| フレームワーク | 場所 | 同梱している関連パッケージ |
| --- | --- | --- |
| **React Native / Expo** | `front/react-native` | `expo`, `expo-status-bar`, `react-native`, `react` |
| **Electron** | `front/electron` | `electron` |
| **SwiftUI** | `ios/Sources` | Apple 標準（SPM ターゲット） |
| **UIKit 相当の題材** | `ios/README.md` | Xcode の iOS App からこの Package を追加して使う前提 |

### バックエンド HTTP

| フレームワーク | 場所 | 同梱している関連パッケージ |
| --- | --- | --- |
| **Express** | `back/express` | `express`, `cors`, `helmet`, `morgan` |
| **NestJS** | `back/nest` | `@nestjs/common`, `@nestjs/core`, `@nestjs/platform-express`, `@nestjs/jwt`, `@nestjs/cli` |
| **Hono** | `back/hono` | `hono`, `@hono/node-server`, `@hono/zod-validator` |
| **Fastify** | `back/fastify` | `fastify`, `@fastify/cors` |
| **FastAPI** | `back/python` | `fastapi`, `uvicorn`, `pydantic` / `pydantic-settings` |
| **Slim** | `back/php` | `slim/slim`, `slim/psr7` |
| **Sinatra** | `back/ruby/sinatra.rb` | gem `sinatra`（標準の `ruby app.rb` は Webrick） |
| **ASP.NET Core** | `back/csharp` | `Microsoft.NET.Sdk.Web` / net8.0 |
| **Axum** | `back/rust` | `axum`, `tokio`, `serde_json` |
| **Go net/http** | `back/go` | 標準ライブラリ |
| **Java HttpServer** | `back/java` | JDK 標準 |

### フルスタックの一本道

| フレームワーク | 場所 | 役割 |
| --- | --- | --- |
| Express + 静的 HTML | `fullstack/app` | REST / JWT / PostgreSQL / Redis をつなぐ練習用アプリ |

---

## 入っているライブラリ

パッケージ名は `package.json` / `pyproject.toml` / `Gemfile` / `composer.json` / `Package.swift` / `Cargo.toml` に入っているものです。

### React 周辺（`front/react`）

| 分類 | ライブラリ |
| --- | --- |
| ルーティング | `react-router-dom` |
| サーバー状態 | `@tanstack/react-query`, `swr`, `axios` |
| クライアント状態 | `zustand`, `jotai` |
| フォーム | `react-hook-form`, `formik`, `@hookform/resolvers` |
| バリデーション | `zod`, `valibot` |
| UI | `@mui/material`, `@emotion/react`, `@emotion/styled`, `@radix-ui/react-slot`, `lucide-react` |
| スタイリング補助 | `tailwindcss`, `@tailwindcss/vite`, `clsx`, `tailwind-merge`, `class-variance-authority` |
| アニメーション | `framer-motion` |
| テスト | `vitest`, `jsdom`, `@testing-library/react`, `@testing-library/jest-dom`, `@testing-library/user-event` |

### TanStack（`front/tanstack`）

- `@tanstack/react-query`
- `@tanstack/react-query-devtools`
- `@tanstack/react-router`
- `@tanstack/react-table`
- `@tanstack/react-form`
- `@tanstack/react-virtual`
- `zod`

### Vue 周辺（`front/vue`）

- `vue-router`
- `pinia`
- `axios`
- `tailwindcss` / `@tailwindcss/vite`
- `vue-tsc`

### GraphQL（`front/graphql`）

- `graphql`
- `@apollo/client`
- `urql`

### Angular 周辺（`front/angular`）

- `@angular/forms` / `@angular/router`
- `rxjs`, `zone.js`, `tslib`
- テスト: `jasmine-core`, `karma`, `karma-jasmine`, `karma-chrome-launcher`, `karma-coverage`, `karma-jasmine-html-reporter`

### フロントのビルド / 品質（複数ディレクトリ）

| 分類 | ライブラリ | 場所 |
| --- | --- | --- |
| バンドラ | `vite`, `@vitejs/plugin-react`, `@vitejs/plugin-vue`, `@sveltejs/vite-plugin-svelte`, `vite-plugin-solid` | 各 Vite プロジェクト |
| CSS | `tailwindcss`, `@tailwindcss/vite`, `@tailwindcss/postcss` | React / Vue / Next |
| Lint / Format | `eslint`, `@eslint/js`, `typescript-eslint`, `prettier`, `@biomejs/biome` | `front/tooling` |
| E2E | `@playwright/test` | `front/playwright` |
| 型 | `typescript`, `tsx`, 各種 `@types/*` | 各 TS プロジェクト |

### Express / フルスタック API

| 分類 | ライブラリ | 場所 |
| --- | --- | --- |
| Web | `express`, `cors`, `helmet`, `morgan` | `back/express`（fullstack は express + cors） |
| 認証 | `jsonwebtoken`, `bcryptjs` | `back/express`, `fullstack/app` |
| ログ | `winston`, `morgan` | `back/express` |
| DB | `pg` | `back/express`, `fullstack/app` |
| キャッシュ | `redis`（npm） | `fullstack/app` |
| 設定 | `dotenv` | `back/express`, `fullstack/app` |
| バリデーション | `zod` | Express / Hono / Fastify / fullstack / TypeScript |
| HTTP クライアント | `axios` | `back/express` |
| テスト | `vitest` | `back/express` |

### NestJS 周辺（`back/nest`）

- `@nestjs/jwt`
- `class-validator`, `class-transformer`
- `reflect-metadata`, `rxjs`
- `ts-node`, `tsconfig-paths`, `@nestjs/schematics`

### Python（`back/python`）

| 分類 | ライブラリ |
| --- | --- |
| Web | `fastapi`, `uvicorn[standard]`, `starlette`（FastAPI 経由） |
| ORM / DB | `sqlalchemy`, `psycopg` |
| 設定 / 型 | `pydantic`, `pydantic-settings` |
| 認証 | `python-jose[cryptography]` |
| キャッシュ | `redis` |
| HTTP クライアント | `httpx` |
| テスト | `pytest` |

### PHP / Ruby / Rust / iOS

| 言語 | ライブラリ |
| --- | --- |
| PHP | `slim/slim`, `slim/psr7`（PSR-7 HTTP） |
| Ruby | `sinatra`, `webrick` |
| Rust | `axum`, `tokio`, `serde_json` |
| Swift | [Alamofire](https://github.com/Alamofire/Alamofire) 5.x |

### iOS 標準 API（コードで使用）

- `Foundation`（`URLSession`, `JSONDecoder`, `UserDefaults`）
- `SwiftUI`（`View`, `@State`, `Button`）
- `XCTest`

品質ツール: SwiftLint（`.swiftlint.yml`）、Fastlane（`ios/fastlane/Fastfile`）、Swift Package Manager

---

## 入っているインフラ / データストア / DevOps

`docker-compose.yml` で起動します。

| 技術 | イメージ / ツール | 用途 |
| --- | --- | --- |
| **PostgreSQL 16** | `postgres:16-alpine` | メインの RDB（ロードマップの中心） |
| **Redis 7** | `redis:7-alpine` | キャッシュ |
| **MySQL 8.4** | `mysql:8.4` | Backend の Relational Databases |
| **MongoDB 7** | `mongo:7` | NoSQL |
| **RabbitMQ 3.13** | `rabbitmq:3.13-management-alpine` | メッセージブローカー |
| **Nginx 1.27** | `nginx:1.27-alpine` | Web サーバ（`:8088`） |
| **Elasticsearch 8.15** | `elasticsearch:8.15.5` | 検索エンジン（`docker compose --profile search up`） |
| **Git / GitHub** | このリポジトリ | バージョン管理 |
| **GitHub Actions** | `.github/workflows/ci.yml` | CI |
| **Terraform** | `fullstack/terraform` | IaC の骨格 |
| **Ansible** | `fullstack/ansible` | 構成管理の骨格 |
| **npm**（yarn / pnpm も利用可） | 各 `package.json` | パッケージマネージャ |
| **uv** | `back/python` | Python 依存関係 |
| **Composer** | `back/php` | PHP 依存関係 |
| **Bundler** | `back/ruby` | Ruby gems |
| **SwiftPM** | `ios/Package.swift` | iOS 依存関係 |

### PostgreSQL ラボで触れる機能（`postgres/`）

スキーマ / IDENTITY / UNIQUE / JSONB / 配列 / GIN インデックス / RANGE パーティション / `pg_stat_statements` / `pgcrypto` / JOIN / CTE / Window 関数 / LATERAL / `EXPLAIN` / PL/pgSQL 関数・トリガー・プロシージャ / ROLE / GRANT / Row Level Security

---

## ディレクトリと起動方法

| パス | 起動 |
| --- | --- |
| `front/html-css-js` | 静的ファイルを開く |
| `front/typescript` | `npm start` |
| `front/react` | `npm run dev` → :5173 |
| `front/vue` | `npm run dev` → :5174 |
| `front/angular` | `npm start` → :4200 |
| `front/svelte` | `npm run dev` → :5175 |
| `front/solid` | `npm run dev` → :5176 |
| `front/next.js` | `npm run dev` → :3000 |
| `front/nuxt` | `npm run dev` → :3005 |
| `front/sveltekit` | `npm run dev` → :5178 |
| `front/astro` | `npm run dev` → :4321 |
| `front/tanstack` | `npm run dev` → :5177 |
| `front/graphql` | `npm run dev` → :5180 |
| `front/electron` | `npm start` |
| `front/react-native` | `npx expo start` |
| `front/playwright` | `npx playwright install chromium && npm test` |
| `front/tooling` | `npm run check` / `npm run lint` / `npm run format` |
| `back/express` | `npm run dev` → :3001 |
| `back/nest` | `npm run dev` → :3002 |
| `back/hono` | `npm run dev` → :3003 |
| `back/fastify` | `npm run dev` → :3004 |
| `back/python` | `uv sync && uv run uvicorn main:app --reload --port 8000` |
| `back/go` | `go run .` → :8090 |
| `back/java` | `javac App.java && java App` → :8081 |
| `back/php` | `composer install && php -S localhost:8082 -t public` |
| `back/ruby` | `ruby app.rb` → :4567（Sinatra は `bundle exec ruby sinatra.rb`） |
| `back/csharp` | `dotnet run`（SDK が必要） |
| `back/rust` | `cargo run`（rustup が必要） |
| `back/nginx` | `docker compose up -d nginx` → :8088 |
| `postgres` | `docker compose up -d postgres` |
| `fullstack/app` | `npm run dev` → :3010 |
| `fullstack/terraform` | 資格情報なしの骨格 |
| `fullstack/ansible` | `ansible-playbook playbook.yml` |
| `ios` | `swift test` |

概念だけのノード（HTTP の仕組み、CAP 定理、HIG など）はインストール対象ではないので、コードではなく README とコメントで扱っています。
