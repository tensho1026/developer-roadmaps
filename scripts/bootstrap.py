#!/usr/bin/env python3
"""Generate playground projects for roadmap.sh technologies."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def write(rel: str, content: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.lstrip("\n") if content.startswith("\n") else content)
    if not content.endswith("\n"):
        path.write_text(path.read_text() + "\n")


# ---------------------------------------------------------------------------
# Shared snippets
# ---------------------------------------------------------------------------

VITE_HTML = """<!doctype html>
<html lang="ja">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.{ext}"></script>
  </body>
</html>
"""

TSCONFIG = """{
  "compilerOptions": {
    "target": "ES2022",
    "useDefineForClassFields": true,
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "isolatedModules": true,
    "moduleDetection": "force",
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": false,
    "noUnusedParameters": false
  },
  "include": ["src"]
}
"""

NODE_TSCONFIG = """{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "dist",
    "rootDir": "src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "declaration": false
  },
  "include": ["src"]
}
"""


def pkg(name: str, scripts: dict, deps: list[str] | None = None, dev: list[str] | None = None, extra: dict | None = None) -> str:
    import json
    data = {
        "name": name,
        "private": True,
        "version": "0.1.0",
        "type": "module",
        "scripts": scripts,
    }
    if deps:
        data["dependencies"] = {d: "*" for d in deps}
    if dev:
        data["devDependencies"] = {d: "*" for d in dev}
    if extra:
        data.update(extra)
    return json.dumps(data, indent=2) + "\n"


# ---------------------------------------------------------------------------
# front/html-css-js
# ---------------------------------------------------------------------------
write(
    "front/html-css-js/index.html",
    """<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>HTML / CSS / JavaScript</title>
  <link rel="stylesheet" href="./styles.css" />
</head>
<body>
  <header>
    <h1>Frontend basics</h1>
    <p>roadmap.sh: HTML, CSS, JavaScript, Accessibility, Web APIs</p>
  </header>
  <main>
    <form id="echo-form" aria-describedby="hint">
      <label for="message">メッセージ</label>
      <input id="message" name="message" required />
      <button type="submit">表示する</button>
    </form>
    <p id="hint">Enter で Web API の <code>fetch</code> を試せます（httpbin）。</p>
    <output id="result" for="message"></output>
  </main>
  <script src="./app.js"></script>
</body>
</html>
""",
)

write(
    "front/html-css-js/styles.css",
    """:root {
  color-scheme: light dark;
  font-family: system-ui, sans-serif;
}
body { max-width: 40rem; margin: 2rem auto; padding: 0 1rem; }
form { display: grid; gap: 0.5rem; }
input, button { font: inherit; padding: 0.5rem; }
button { cursor: pointer; }
output { display: block; margin-top: 1rem; padding: 1rem; border: 1px solid currentColor; }
""",
)

write(
    "front/html-css-js/app.js",
    """const form = document.querySelector("#echo-form");
const output = document.querySelector("#result");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = new FormData(form).get("message");
  output.textContent = `ローカル: ${message}`;
  try {
    const res = await fetch("https://httpbin.org/post", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });
    const data = await res.json();
    output.textContent += `\\nfetch: ${JSON.stringify(data.json)}`;
  } catch (error) {
    output.textContent += `\\nfetch failed: ${error}`;
  }
});
""",
)

write(
    "front/html-css-js/README.md",
    """# HTML / CSS / JavaScript

Frontend ロードマップの土台。`npx serve .` または VS Code Live Preview で開けます。
""",
)

# ---------------------------------------------------------------------------
# front/typescript
# ---------------------------------------------------------------------------
write(
    "front/typescript/package.json",
    pkg(
        "front-typescript",
        {"start": "tsx src/index.ts", "build": "tsc -p tsconfig.json"},
        deps=["zod"],
        dev=["typescript", "tsx", "@types/node"],
    ),
)
write(
    "front/typescript/tsconfig.json",
    """{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "outDir": "dist",
    "skipLibCheck": true
  },
  "include": ["src"]
}
""",
)
write(
    "front/typescript/src/index.ts",
    """import { z } from "zod";

const User = z.object({
  id: z.number(),
  email: z.string().email(),
});

const user = User.parse({ id: 1, email: "ada@example.com" });
console.log("TypeScript + Zod:", user);
""",
)
write("front/typescript/README.md", "# TypeScript\\n\\n`npm start` で Zod 付きの型チェック例を実行します。\\n")

# ---------------------------------------------------------------------------
# front/react
# ---------------------------------------------------------------------------
write(
    "front/react/package.json",
    pkg(
        "front-react",
        {
            "dev": "vite",
            "build": "tsc -b && vite build",
            "preview": "vite preview",
            "test": "vitest run",
        },
        deps=[
            "react",
            "react-dom",
            "react-router-dom",
            "@tanstack/react-query",
            "zustand",
            "jotai",
            "axios",
            "swr",
            "react-hook-form",
            "formik",
            "zod",
            "valibot",
            "@hookform/resolvers",
            "framer-motion",
            "clsx",
            "tailwind-merge",
            "class-variance-authority",
            "lucide-react",
            "@radix-ui/react-slot",
            "@mui/material",
            "@emotion/react",
            "@emotion/styled",
        ],
        dev=[
            "typescript",
            "vite",
            "@vitejs/plugin-react",
            "@types/react",
            "@types/react-dom",
            "vitest",
            "jsdom",
            "@testing-library/react",
            "@testing-library/jest-dom",
            "@testing-library/user-event",
            "tailwindcss",
            "@tailwindcss/vite",
        ],
    ),
)
write("front/react/index.html", VITE_HTML.format(title="React playground", ext="tsx"))
write(
    "front/react/vite.config.ts",
    """import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: { port: 5173 },
});
""",
)
write("front/react/tsconfig.json", TSCONFIG)
write("front/react/tsconfig.node.json", """{"compilerOptions":{"composite":true,"skipLibCheck":true,"module":"ESNext","moduleResolution":"bundler","strict":true},"include":["vite.config.ts"]}""")
write(
    "front/react/src/index.css",
    """@import "tailwindcss";
body { margin: 0; font-family: system-ui, sans-serif; }
""",
)
write(
    "front/react/src/main.tsx",
    """import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter } from "react-router-dom";
import App from "./App";
import "./index.css";

const queryClient = new QueryClient();

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </QueryClientProvider>
  </StrictMode>,
);
""",
)
write(
    "front/react/src/store.ts",
    """import { create } from "zustand";

type CounterState = { count: number; inc: () => void };

export const useCounter = create<CounterState>((set) => ({
  count: 0,
  inc: () => set((s) => ({ count: s.count + 1 })),
}));
""",
)
write(
    "front/react/src/App.tsx",
    """import { useQuery } from "@tanstack/react-query";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { motion } from "framer-motion";
import { useCounter } from "./store";

const schema = z.object({ name: z.string().min(1) });
type FormValues = z.infer<typeof schema>;

export default function App() {
  const { count, inc } = useCounter();
  const { register, handleSubmit } = useForm<FormValues>({ resolver: zodResolver(schema) });
  const { data } = useQuery({
    queryKey: ["todo"],
    queryFn: async () => {
      const res = await fetch("https://jsonplaceholder.typicode.com/todos/1");
      return res.json() as Promise<{ title: string }>;
    },
  });

  return (
    <main className="mx-auto max-w-xl p-8">
      <h1 className="text-2xl font-bold">React playground</h1>
      <p className="mt-2 text-sm opacity-80">
        React Router / TanStack Query / Zustand / React Hook Form / Zod / Framer Motion / Tailwind
      </p>
      <motion.button
        whileTap={{ scale: 0.96 }}
        className="mt-6 rounded bg-black px-4 py-2 text-white"
        onClick={inc}
      >
        Zustand count: {count}
      </motion.button>
      <p className="mt-4">Query: {data?.title ?? "loading..."}</p>
      <form className="mt-6 grid gap-2" onSubmit={handleSubmit((v) => alert(v.name))}>
        <input className="border px-3 py-2" placeholder="name" {...register("name")} />
        <button className="border px-3 py-2" type="submit">submit</button>
      </form>
    </main>
  );
}
""",
)
write(
    "front/react/src/App.test.tsx",
    """import { render, screen } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter } from "react-router-dom";
import { expect, test } from "vitest";
import App from "./App";

test("renders heading", () => {
  render(
    <QueryClientProvider client={new QueryClient()}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </QueryClientProvider>,
  );
  expect(screen.getByText(/React playground/)).toBeTruthy();
});
""",
)
write(
    "front/react/vitest.config.ts",
    """import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  test: { environment: "jsdom" },
});
""",
)
write("front/react/README.md", "# React\\n\\n`npm run dev` → http://localhost:5173\\n")

# ---------------------------------------------------------------------------
# front/vue
# ---------------------------------------------------------------------------
write(
    "front/vue/package.json",
    pkg(
        "front-vue",
        {"dev": "vite", "build": "vue-tsc -b && vite build", "preview": "vite preview"},
        deps=["vue", "vue-router", "pinia", "axios"],
        dev=["typescript", "vite", "@vitejs/plugin-vue", "vue-tsc", "tailwindcss", "@tailwindcss/vite"],
    ),
)
write("front/vue/index.html", VITE_HTML.format(title="Vue playground", ext="ts"))
write(
    "front/vue/vite.config.ts",
    """import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import tailwindcss from "@tailwindcss/vite";
export default defineConfig({ plugins: [vue(), tailwindcss()], server: { port: 5174 } });
""",
)
write(
    "front/vue/tsconfig.json",
    """{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "jsx": "preserve",
    "lib": ["ES2022", "DOM"],
    "skipLibCheck": true,
    "noEmit": true
  },
  "include": ["src/**/*", "src/**/*.vue"]
}
""",
)
write("front/vue/src/vite-env.d.ts", """/// <reference types="vite/client" />
declare module "*.vue" {
  import type { DefineComponent } from "vue";
  const component: DefineComponent<{}, {}, any>;
  export default component;
}
""")
write(
    "front/vue/src/main.ts",
    """import { createApp } from "vue";
import { createPinia } from "pinia";
import { createRouter, createWebHistory } from "vue-router";
import App from "./App.vue";
import Home from "./Home.vue";
import "./index.css";

const router = createRouter({
  history: createWebHistory(),
  routes: [{ path: "/", component: Home }],
});

createApp(App).use(createPinia()).use(router).mount("#root");
""",
)
write("front/vue/src/index.css", '@import "tailwindcss";\n')
write("front/vue/src/App.vue", "<template>\\n  <router-view />\\n</template>\\n")
write(
    "front/vue/src/Home.vue",
    """<script setup lang="ts">
import { useCounter } from "./store";
const counter = useCounter();
</script>
<template>
  <main class="p-8">
    <h1 class="text-2xl font-bold">Vue playground</h1>
    <p>Vue Router / Pinia / Tailwind</p>
    <button class="mt-4 border px-3 py-2" @click="counter.inc">count: {{ counter.count }}</button>
  </main>
</template>
""",
)
write(
    "front/vue/src/store.ts",
    """import { defineStore } from "pinia";
export const useCounter = defineStore("counter", {
  state: () => ({ count: 0 }),
  actions: { inc() { this.count += 1; } },
});
""",
)
write("front/vue/README.md", "# Vue.js\\n\\n`npm run dev` → http://localhost:5174\\n")

# ---------------------------------------------------------------------------
# front/svelte
# ---------------------------------------------------------------------------
write(
    "front/svelte/package.json",
    pkg(
        "front-svelte",
        {"dev": "vite", "build": "vite build", "preview": "vite preview"},
        deps=["svelte"],
        dev=["typescript", "vite", "@sveltejs/vite-plugin-svelte"],
    ),
)
write("front/svelte/index.html", VITE_HTML.format(title="Svelte playground", ext="ts"))
write(
    "front/svelte/vite.config.ts",
    """import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";
export default defineConfig({ plugins: [svelte()], server: { port: 5175 } });
""",
)
write("front/svelte/svelte.config.js", "import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';\\nexport default { preprocess: vitePreprocess() };\\n")
write("front/svelte/tsconfig.json", """{"compilerOptions":{"strict":true,"moduleResolution":"bundler","target":"ES2022","module":"ESNext","verbatimModuleSyntax":true},"include":["src"]}""")
write(
    "front/svelte/src/main.ts",
    """import { mount } from "svelte";
import App from "./App.svelte";
mount(App, { target: document.getElementById("root")! });
""",
)
write(
    "front/svelte/src/App.svelte",
    """<script lang="ts">
  let count = $state(0);
</script>
<main>
  <h1>Svelte playground</h1>
  <button onclick={() => count++}>count: {count}</button>
</main>
""",
)
write("front/svelte/README.md", "# Svelte\\n\\n`npm run dev` → http://localhost:5175\\n")

# ---------------------------------------------------------------------------
# front/solid
# ---------------------------------------------------------------------------
write(
    "front/solid/package.json",
    pkg(
        "front-solid",
        {"dev": "vite", "build": "vite build", "preview": "vite preview"},
        deps=["solid-js"],
        dev=["typescript", "vite", "vite-plugin-solid"],
    ),
)
write("front/solid/index.html", VITE_HTML.format(title="Solid playground", ext="tsx"))
write(
    "front/solid/vite.config.ts",
    """import { defineConfig } from "vite";
import solid from "vite-plugin-solid";
export default defineConfig({ plugins: [solid()], server: { port: 5176 } });
""",
)
write(
    "front/solid/tsconfig.json",
    """{"compilerOptions":{"strict":true,"jsx":"preserve","jsxImportSource":"solid-js","moduleResolution":"bundler","target":"ES2022","module":"ESNext"},"include":["src"]}""",
)
write(
    "front/solid/src/main.tsx",
    """import { render } from "solid-js/web";
import App from "./App";
render(() => <App />, document.getElementById("root")!);
""",
)
write(
    "front/solid/src/App.tsx",
    """import { createSignal } from "solid-js";
export default function App() {
  const [count, setCount] = createSignal(0);
  return (
    <main>
      <h1>Solid JS playground</h1>
      <button onClick={() => setCount(count() + 1)}>count: {count()}</button>
    </main>
  );
}
""",
)
write("front/solid/README.md", "# Solid JS\\n\\n`npm run dev` → http://localhost:5176\\n")

print("partial 1 done")
