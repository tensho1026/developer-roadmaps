import { ApolloClient, ApolloProvider, InMemoryCache, gql, useMutation, useQuery } from "@apollo/client";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

const uri = import.meta.env.VITE_GRAPHQL_URL ?? "http://localhost:4000/graphql";

const client = new ApolloClient({
  uri,
  cache: new InMemoryCache(),
});

const NOTES = gql`
  query Notes {
    notes {
      id
      title
      body
    }
  }
`;

const ADD = gql`
  mutation AddNote($title: String!, $body: String!) {
    addNote(title: $title, body: $body) {
      id
      title
      body
    }
  }
`;

function Notes() {
  const { data, loading, error, refetch } = useQuery(NOTES);
  const [addNote] = useMutation(ADD);

  if (loading) return <p>loading...</p>;
  if (error) {
    return (
      <main style={{ padding: 24 }}>
        <h1>GraphQL / Apollo</h1>
        <p>ローカル Yoga（{uri}）に接続できません。`back/graphql` で `npm run dev` してください。</p>
        <p>{error.message}</p>
      </main>
    );
  }

  return (
    <main style={{ padding: 24 }}>
      <h1>GraphQL / Apollo</h1>
      <p>endpoint: {uri}</p>
      <ul>
        {data.notes.map((note: { id: string; title: string; body: string }) => (
          <li key={note.id}>
            <strong>{note.title}</strong> — {note.body}
          </li>
        ))}
      </ul>
      <button
        type="button"
        onClick={async () => {
          await addNote({ variables: { title: "from apollo", body: String(Date.now()) } });
          await refetch();
        }}
      >
        add note
      </button>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ApolloProvider client={client}>
      <Notes />
    </ApolloProvider>
  </StrictMode>,
);
