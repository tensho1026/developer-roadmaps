# developer-roadmaps

[roadmap.sh](https://roadmap.sh/) の **Frontend / Backend / Full Stack / PostgreSQL DBA / iOS** に出てくる言語・フレームワーク・ライブラリを、すぐ触れる形で置いた学習用リポジトリです。

## いちばん先にやること

```bash
cp .env.example .env
docker compose up -d postgres redis
```

Node 系は各ディレクトリで `npm install`、またはまとめて:

```bash
./scripts/install-all.sh
```

## ディレクトリ

| パス | ロードマップ | 起動 |
| --- | --- | --- |
| `front/html-css-js` | HTML / CSS / JavaScript | 静的ファイルを開く |
| `front/typescript` | TypeScript / Zod | `npm start` |
| `front/react` | React, React Router, Query, Zustand, RHF, Tailwind | `npm run dev` :5173 |
| `front/vue` | Vue, Vue Router, Pinia | `npm run dev` :5174 |
| `front/angular` | Angular | `npm start` :4200 |
| `front/svelte` | Svelte | `npm run dev` :5175 |
| `front/solid` | Solid JS | `npm run dev` :5176 |
| `front/next.js` | Next.js SSR/SSG | `npm run dev` :3000 |
| `front/nuxt` | Nuxt.js | `npm run dev` :3005 |
| `front/sveltekit` | SvelteKit | `npm run dev` :5178 |
| `front/astro` | Astro SSG | `npm run dev` :4321 |
| `front/tanstack` | TanStack Query/Table/Form | `npm run dev` :5177 |
| `front/graphql` | GraphQL / Apollo | `npm run dev` :5180 |
| `front/electron` | Desktop (Electron) | `npm start` |
| `front/react-native` | React Native (Expo) | `npx expo start` |
| `front/playwright` | Playwright | `npx playwright install chromium && npm test` |
| `front/tooling` | ESLint / Prettier / Biome | `npm run check` |
| `back/express` | Express, JWT, Helmet, Morgan, Winston | `npm run dev` :3001 |
| `back/nest` | NestJS | `npm run dev` :3002 |
| `back/hono` | Hono | `npm run dev` :3003 |
| `back/fastify` | Fastify | `npm run dev` :3004 |
| `back/python` | Python / FastAPI | `uv sync && uv run uvicorn main:app --reload --port 8000` |
| `back/go` | Go | `go run .` :8090 |
| `back/java` | Java HTTP | `javac App.java && java App` :8081 |
| `back/php` | PHP / Slim | `composer install && php -S localhost:8082 -t public` |
| `back/ruby` | Ruby / Sinatra | `bundle install && ruby app.rb` |
| `back/csharp` | C# ASP.NET | `dotnet run`（SDK が必要） |
| `back/rust` | Rust / Axum | `cargo run`（rustup が必要） |
| `back/nginx` | Nginx | `docker compose up -d nginx` :8088 |
| `postgres` | PostgreSQL DBA | `docker compose up -d postgres` |
| `fullstack/app` | Full Stack の一本道 | `npm run dev` :3010 |
| `fullstack/terraform` | Terraform | 資格情報なしの骨格 |
| `fullstack/ansible` | Ansible | `ansible-playbook playbook.yml` |
| `ios` | Swift / SwiftUI / Alamofire / XCTest | `swift test` |

インフラ系（MySQL, MongoDB, RabbitMQ, Elasticsearch）はルートの `docker-compose.yml` にあります。Elasticsearch は重いので `docker compose --profile search up -d elasticsearch` です。

## ロードマップとの対応

詳細は [TECH_MAP.md](./TECH_MAP.md) を見てください。概念だけのノード（HTTP の仕組み、CAP 定理、HIG など）はコードではなく README とコメントで扱っています。
