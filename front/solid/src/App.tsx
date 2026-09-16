import { createSignal } from "solid-js";
export default function App() {
  const [count, setCount] = createSignal(0);
  return (
    <main>
      <h1>Solid JS playground</h1>
      <button onClick={() => setCount(count() + 1)}>count: {count()}</button>
    </main>
  );
}
