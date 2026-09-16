import { useQuery } from "@tanstack/react-query";
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
