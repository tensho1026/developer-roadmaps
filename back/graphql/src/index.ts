import { createServer } from "node:http";
import { createSchema, createYoga } from "graphql-yoga";

type Note = { id: string; title: string; body: string };
const notes: Note[] = [{ id: "1", title: "GraphQL lab", body: "local yoga server" }];

const yoga = createYoga({
  graphqlEndpoint: "/graphql",
  cors: { origin: "*" },
  schema: createSchema({
    typeDefs: /* GraphQL */ `
      type Note {
        id: ID!
        title: String!
        body: String!
      }
      type Query {
        notes: [Note!]!
        note(id: ID!): Note
      }
      type Mutation {
        addNote(title: String!, body: String!): Note!
      }
    `,
    resolvers: {
      Query: {
        notes: () => notes,
        note: (_: unknown, args: { id: string }) => notes.find((n) => n.id === args.id) ?? null,
      },
      Mutation: {
        addNote: (_: unknown, args: { title: string; body: string }) => {
          const note = { id: String(notes.length + 1), ...args };
          notes.push(note);
          return note;
        },
      },
    },
  }),
});

createServer(yoga).listen(4000, () => {
  console.log("graphql yoga on http://localhost:4000/graphql");
});
