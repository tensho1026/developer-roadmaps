import * as grpc from "@grpc/grpc-js";
import { loadNotesPackage, type Note } from "./proto.js";

const notes: Note[] = [{ id: "1", title: "gRPC lab", body: "in-memory unary RPC" }];
const port = Number(process.env.PORT ?? 50051);
const proto = loadNotesPackage();

const server = new grpc.Server();
server.addService(proto.notes.Notes.service, {
  ListNotes: (
    _call: grpc.ServerUnaryCall<Record<string, never>, { notes: Note[] }>,
    callback: grpc.sendUnaryData<{ notes: Note[] }>,
  ) => {
    callback(null, { notes });
  },
  AddNote: (
    call: grpc.ServerUnaryCall<{ title: string; body: string }, Note>,
    callback: grpc.sendUnaryData<Note>,
  ) => {
    const title = call.request.title?.trim() ?? "";
    const body = call.request.body?.trim() ?? "";
    if (!title || !body) {
      callback({
        code: grpc.status.INVALID_ARGUMENT,
        details: "title and body are required",
        message: "title and body are required",
        name: "INVALID_ARGUMENT",
        metadata: new grpc.Metadata(),
      });
      return;
    }
    const note: Note = { id: String(notes.length + 1), title, body };
    notes.push(note);
    callback(null, note);
  },
});

server.bindAsync(`0.0.0.0:${port}`, grpc.ServerCredentials.createInsecure(), (error, bound) => {
  if (error) {
    console.error(error);
    process.exit(1);
  }
  console.log(`grpc notes on localhost:${bound}`);
});
