# ロードマップ技術とこのリポジトリの対応

出典: [roadmap.sh/frontend](https://roadmap.sh/frontend), [backend](https://roadmap.sh/backend), [full-stack](https://roadmap.sh/full-stack), [postgresql-dba](https://roadmap.sh/postgresql-dba), [ios](https://roadmap.sh/ios)。Node のフレームワーク名は Frontend/Backend から辿る [Node.js roadmap](https://roadmap.sh/nodejs) も使っています。

## Frontend

| ノード | 場所 |
| --- | --- |
| HTML / CSS / JavaScript | `front/html-css-js` |
| TypeScript / Zod | `front/typescript`, `front/react` |
| npm / yarn / pnpm | 各 `package.json`（このマシンでは 3 つとも利用可） |
| Git / GitHub | このリポジトリそのもの |
| React | `front/react` |
| Vue.js | `front/vue` |
| Angular | `front/angular` |
| Svelte / SvelteKit | `front/svelte`, `front/sveltekit` |
| Solid JS | `front/solid` |
| Tailwind | `front/react`, `front/next.js` |
| Vite / esbuild | Vite ベースの front 配下 |
| ESLint / Prettier / Biome | `front/tooling` |
| Vitest / Jest / Testing Library | `front/react` |
| Playwright / Cypress | `front/playwright`（Cypress バイナリは未ダウンロード） |
| Next.js | `front/next.js` |
| Nuxt.js | `front/nuxt` |
| Astro | `front/astro` |
| TanStack Query / Table / Form | `front/tanstack` |
| TanStack Start | `front/tanstack-start` |
| GraphQL / Apollo | `front/graphql` + `back/graphql` |
| PWA / Service Worker | `front/pwa` |
| Web Components | `front/web-components` |
| Electron | `front/electron` |
| React Native | `front/react-native` |
| Auth / JWT（フロントから叩く） | `fullstack/app`, `back/express` |

## Backend

| ノード | 場所 |
| --- | --- |
| JavaScript / Node | `back/express` `back/nest` `back/hono` `back/fastify` |
| Python | `back/python` |
| Go | `back/go` |
| Java | `back/java` |
| PHP | `back/php` |
| Ruby | `back/ruby` |
| C# | `back/csharp` |
| Rust | `back/rust` |
| Express / Nest / Hono / Fastify | `back/` 配下の同名ディレクトリ |
| PostgreSQL | `postgres/` + Docker |
| MySQL / Redis | `docker-compose.yml` / `fullstack/app` |
| MongoDB / Mongoose | `back/mongoose` + compose |
| RabbitMQ | `back/rabbitmq` + compose |
| gRPC | `back/grpc` |
| Nginx | `back/nginx` + compose |
| REST / JSON APIs / JWT / bcrypt | `back/express`, `fullstack/app` |
| Prisma / OpenAPI | `back/prisma` |
| WebSockets / SSE | `back/realtime` |
| GraphQL server | `back/graphql` |
| OAuth | `back/oauth` |
| CLI (commander) | `back/cli` |
| Testing | 各 Node プロジェクトの vitest / XCTest |

## Full Stack

| ノード | 場所 |
| --- | --- |
| HTML/CSS/JS → Node → REST → JWT → Redis → PostgreSQL CRUD | `fullstack/app` + compose |
| CLI Apps | `back/cli` |
| GitHub Actions | `.github/workflows/ci.yml` |
| Terraform | `fullstack/terraform` |
| Ansible | `fullstack/ansible` |

## PostgreSQL DBA

`postgres/init` と `postgres/sql`。パーティション、GIN、JSONB、PL/pgSQL、RLS、EXPLAIN。

## iOS

| ノード | 場所 |
| --- | --- |
| Swift / SwiftUI | `ios/Sources`, `ios/RoadmapsApp` |
| UIKit / Combine / Core Data | `ios/RoadmapsApp` |
| URLSession / Alamofire | `ios/Sources/IosPlayground/Networking.swift` |
| UserDefaults | `Persistence.swift` |
| Swift Package Manager | `ios/Package.swift` |
| XCTest | `ios/Tests` |
| SwiftLint / Fastlane | `ios/.swiftlint.yml`, `ios/fastlane` |
