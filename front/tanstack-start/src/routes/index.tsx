import * as fs from "node:fs";
import { createFileRoute, useRouter } from "@tanstack/react-router";
import { createServerFn } from "@tanstack/react-start";

const filePath = "count.txt";

async function readCount() {
  return parseInt(await fs.promises.readFile(filePath, "utf-8").catch(() => "0"), 10);
}

const getCount = createServerFn({ method: "GET" }).handler(() => readCount());

const updateCount = createServerFn({ method: "POST" })
  .validator((d: number) => d)
  .handler(async ({ data }) => {
    const count = await readCount();
    await fs.promises.writeFile(filePath, `${count + data}`);
  });

export const Route = createFileRoute("/")({
  component: Home,
  loader: async () => await getCount(),
});

function Home() {
  const router = useRouter();
  const state = Route.useLoaderData();

  return (
    <main style={{ fontFamily: "system-ui", padding: 24 }}>
      <h1>TanStack Start</h1>
      <p>サーバー関数で count.txt を更新します。</p>
      <button
        type="button"
        onClick={() => {
          updateCount({ data: 1 }).then(() => router.invalidate());
        }}
      >
        Add 1 to {state}?
      </button>
    </main>
  );
}
