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
    if deps:
        data["dependencies"] = {d: "*" for d in deps}
    if dev:
        data["devDependencies"] = {d: "*" for d in dev}
    if extra:
        data.update(extra)
    return json.dumps(data, indent=2) + "\n"


# Fix files from bootstrap.py that used escaped newlines incorrectly
write("front/typescript/README.md", "# TypeScript\n\n`npm start` で Zod 付きの型チェック例を実行します。\n")
write("front/react/README.md", "# React\n\n`npm run dev` → http://localhost:5173\n")
write("front/vue/src/App.vue", "<template>\n  <router-view />\n</template>\n")
write("front/vue/README.md", "# Vue.js\n\n`npm run dev` → http://localhost:5174\n")
write(
    "front/svelte/svelte.config.js",
    "import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';\nexport default { preprocess: vitePreprocess() };\n",
)
write("front/svelte/README.md", "# Svelte\n\n`npm run dev` → http://localhost:5175\n")
write("front/solid/README.md", "# Solid JS\n\n`npm run dev` → http://localhost:5176\n")

# ---------------------------------------------------------------------------
# front/next.js
# ---------------------------------------------------------------------------
write(
    "front/next.js/package.json",
    pkg(
        "front-nextjs",
        {"dev": "next dev -p 3000", "build": "next build", "start": "next start -p 3000"},
        deps=["next", "react", "react-dom"],
        dev=["typescript", "@types/react", "@types/react-dom", "@types/node", "tailwindcss", "@tailwindcss/postcss"],
    ),
)
write("front/next.js/next.config.ts", "import type { NextConfig } from 'next';\nconst nextConfig: NextConfig = {};\nexport default nextConfig;\n")
write(
    "front/next.js/tsconfig.json",
    """{
  "compilerOptions": {
    "target": "ES2017",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": { "@/*": ["./src/*"] }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
""",
)
write("front/next.js/postcss.config.mjs", "const config = { plugins: { '@tailwindcss/postcss': {} } };\nexport default config;\n")
write("front/next.js/src/app/globals.css", '@import "tailwindcss";\n')
write(
    "front/next.js/src/app/layout.tsx",
    """export const metadata = { title: "Next.js playground" };
import "./globals.css";
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ja">
      <body>{children}</body>
    </html>
  );
}
""",
)
write(
    "front/next.js/src/app/page.tsx",
    """export default async function Page() {
  return (
    <main className="p-8">
      <h1 className="text-2xl font-bold">Next.js playground</h1>
      <p>SSR / SSG / App Router / Tailwind。フルスタック版は ../../fullstack/app を参照。</p>
    </main>
  );
}
""",
)
write("front/next.js/README.md", "# Next.js\n\nFrontend の SSR / SSG ノード。`npm run dev` → http://localhost:3000\n")

# ---------------------------------------------------------------------------
# front/nuxt
# ---------------------------------------------------------------------------
write(
    "front/nuxt/package.json",
    pkg("front-nuxt", {"dev": "nuxt dev --port 3005", "build": "nuxt build", "preview": "nuxt preview"}, deps=["nuxt", "vue", "vue-router"]),
)
write("front/nuxt/nuxt.config.ts", "export default defineNuxtConfig({ compatibilityDate: '2025-01-01' });\n")
write(
    "front/nuxt/app.vue",
    """<template>
  <main style="padding: 2rem">
    <h1>Nuxt.js playground</h1>
    <p>Vue SSR / SSG (roadmap.sh Frontend)</p>
  </main>
</template>
""",
)
write("front/nuxt/README.md", "# Nuxt.js\n\n`npm run dev` → http://localhost:3005\n")

# ---------------------------------------------------------------------------
# front/sveltekit
# ---------------------------------------------------------------------------
write(
    "front/sveltekit/package.json",
    pkg(
        "front-sveltekit",
        {"dev": "vite dev --port 5178", "build": "vite build", "preview": "vite preview"},
        deps=["@sveltejs/kit", "svelte"],
        dev=["@sveltejs/adapter-auto", "@sveltejs/vite-plugin-svelte", "typescript", "vite"],
    ),
)
write(
    "front/sveltekit/svelte.config.js",
    """import adapter from '@sveltejs/adapter-auto';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';
const config = { preprocess: vitePreprocess(), kit: { adapter: adapter() } };
export default config;
""",
)
write(
    "front/sveltekit/vite.config.ts",
    """import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
export default defineConfig({ plugins: [sveltekit()] });
""",
)
write("front/sveltekit/tsconfig.json", """{"extends":"./.svelte-kit/tsconfig.json","compilerOptions":{"strict":true}}""")
write("front/sveltekit/src/app.html", """<!doctype html>
<html lang="ja">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    %sveltekit.head%
  </head>
  <body data-sveltekit-preload-data="hover">
    <div style="display: contents">%sveltekit.body%</div>
  </body>
</html>
""")
write(
    "front/sveltekit/src/routes/+page.svelte",
    """<h1>SvelteKit playground</h1>
<p>Frontend roadmap: SvelteKit SSR</p>
""",
)
write("front/sveltekit/README.md", "# SvelteKit\n\n`npm run dev` → http://localhost:5178\n")

# ---------------------------------------------------------------------------
# front/astro
# ---------------------------------------------------------------------------
write(
    "front/astro/package.json",
    pkg("front-astro", {"dev": "astro dev --port 4321", "build": "astro build", "preview": "astro preview"}, deps=["astro"]),
)
write("front/astro/astro.config.mjs", "import { defineConfig } from 'astro/config';\nexport default defineConfig({});\n")
write("front/astro/tsconfig.json", """{"extends":"astro/tsconfigs/strict"}""")
write(
    "front/astro/src/pages/index.astro",
    """---
const title = "Astro playground";
---
<html lang="ja">
  <head><meta charset="utf-8" /><title>{title}</title></head>
  <body>
    <h1>{title}</h1>
    <p>SSG: Astro / Eleventy 相当の静的サイト生成。</p>
  </body>
</html>
""",
)
write("front/astro/README.md", "# Astro\n\n`npm run dev` → http://localhost:4321\n")

# ---------------------------------------------------------------------------
# front/tanstack
# ---------------------------------------------------------------------------
write(
    "front/tanstack/package.json",
    pkg(
        "front-tanstack",
        {"dev": "vite --port 5177", "build": "vite build"},
        deps=[
            "react",
            "react-dom",
            "@tanstack/react-query",
            "@tanstack/react-query-devtools",
            "@tanstack/react-router",
            "@tanstack/react-table",
            "@tanstack/react-form",
            "@tanstack/react-virtual",
            "zod",
        ],
        dev=["typescript", "vite", "@vitejs/plugin-react", "@types/react", "@types/react-dom"],
    ),
)
write(
    "front/tanstack/index.html",
    """<!doctype html>
<html lang="ja">
  <head><meta charset="UTF-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" /><title>TanStack</title></head>
  <body><div id="root"></div><script type="module" src="/src/main.tsx"></script></body>
</html>
""",
)
write(
    "front/tanstack/vite.config.ts",
    """import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
export default defineConfig({ plugins: [react()], server: { port: 5177 } });
""",
)
write(
    "front/tanstack/tsconfig.json",
    """{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "strict": true,
    "skipLibCheck": true,
    "noEmit": true,
    "lib": ["ES2022", "DOM"]
  },
  "include": ["src"]
}
""",
)
write(
    "front/tanstack/src/main.tsx",
    """import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { QueryClient, QueryClientProvider, useQuery } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import {
  createColumnHelper,
  flexRender,
  getCoreRowModel,
  useReactTable,
} from "@tanstack/react-table";
import { useForm } from "@tanstack/react-form";

const queryClient = new QueryClient();

type Todo = { id: number; title: string; completed: boolean };
const helper = createColumnHelper<Todo>();
const columns = [
  helper.accessor("id", { header: "ID" }),
  helper.accessor("title", { header: "Title" }),
  helper.accessor("completed", { header: "Done" }),
];

function Todos() {
  const { data = [] } = useQuery({
    queryKey: ["todos"],
    queryFn: async () => {
      const res = await fetch("https://jsonplaceholder.typicode.com/todos?_limit=5");
      return res.json() as Promise<Todo[]>;
    },
  });
  const table = useReactTable({ data, columns, getCoreRowModel: getCoreRowModel() });
  const form = useForm({
    defaultValues: { note: "" },
    onSubmit: async ({ value }) => alert(value.note),
  });

  return (
    <main style={{ padding: 24, fontFamily: "system-ui" }}>
      <h1>TanStack playground</h1>
      <p>Query / Table / Form / Virtual / Router 相当の API をこのディレクトリで扱えます。</p>
      <table border={1} cellPadding={6} style={{ marginTop: 16, borderCollapse: "collapse" }}>
        <thead>
          {table.getHeaderGroups().map((hg) => (
            <tr key={hg.id}>
              {hg.headers.map((h) => (
                <th key={h.id}>{flexRender(h.column.columnDef.header, h.getContext())}</th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody>
          {table.getRowModel().rows.map((row) => (
            <tr key={row.id}>
              {row.getVisibleCells().map((cell) => (
                <td key={cell.id}>{flexRender(cell.column.columnDef.cell, cell.getContext())}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
      <form
        style={{ marginTop: 16 }}
        onSubmit={(e) => {
          e.preventDefault();
          form.handleSubmit();
        }}
      >
        <form.Field
          name="note"
          children={(field) => (
            <input
              value={field.state.value}
              onChange={(e) => field.handleChange(e.target.value)}
              placeholder="tanstack form"
            />
          )}
        />
        <button type="submit">save</button>
      </form>
      <ReactQueryDevtools />
    </main>
  );
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <Todos />
    </QueryClientProvider>
  </StrictMode>,
);
""",
)
write("front/tanstack/README.md", "# TanStack\n\nQuery / Table / Form / Router。`npm run dev` → http://localhost:5177\n")

print("front extra done")
