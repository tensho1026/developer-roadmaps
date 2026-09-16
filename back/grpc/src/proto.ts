import * as grpc from "@grpc/grpc-js";
import * as protoLoader from "@grpc/proto-loader";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

export type Note = { id: string; title: string; body: string };

export type NotesClient = grpc.Client & {
  ListNotes: (
    request: Record<string, never>,
    callback: (error: grpc.ServiceError | null, response: { notes: Note[] }) => void,
  ) => void;
  AddNote: (
    request: { title: string; body: string },
    callback: (error: grpc.ServiceError | null, response: Note) => void,
  ) => void;
};

type NotesPackage = {
  notes: {
    Notes: {
      service: grpc.ServiceDefinition;
      new (address: string, credentials: grpc.ChannelCredentials): NotesClient;
    };
  };
};

const PROTO_PATH = join(dirname(fileURLToPath(import.meta.url)), "../proto/notes.proto");

export function loadNotesPackage(): NotesPackage {
  const definition = protoLoader.loadSync(PROTO_PATH, {
    keepCase: true,
    longs: String,
    enums: String,
    defaults: true,
    oneofs: true,
  });
  return grpc.loadPackageDefinition(definition) as unknown as NotesPackage;
}
