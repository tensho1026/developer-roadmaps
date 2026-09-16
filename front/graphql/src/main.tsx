import { ApolloClient, ApolloProvider, InMemoryCache, gql, useQuery } from "@apollo/client";
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

const client = new ApolloClient({
  uri: "https://countries.trevorblades.com/",
  cache: new InMemoryCache(),
});

const QUERY = gql`
  query {
    country(code: "JP") {
      name
      capital
    }
  }
`;

function Country() {
  const { data, loading, error } = useQuery(QUERY);
  if (loading) return <p>loading...</p>;
  if (error) return <p>{error.message}</p>;
  return (
    <main style={{ padding: 24 }}>
      <h1>GraphQL / Apollo</h1>
      <p>
        {data.country.name} / {data.country.capital}
      </p>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ApolloProvider client={client}>
      <Country />
    </ApolloProvider>
  </StrictMode>,
);
