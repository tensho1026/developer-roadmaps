import { StrictMode } from "react";
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
