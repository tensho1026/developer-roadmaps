import * as grpc from "@grpc/grpc-js";
import { loadNotesPackage, type Note } from "./proto.js";

const address = process.env.GRPC_ADDRESS ?? "localhost:50051";
const proto = loadNotesPackage();
const client = new proto.notes.Notes(address, grpc.credentials.createInsecure());

function waitForReady(timeoutMs = 3000): Promise<void> {
  return new Promise((resolve, reject) => {
    client.waitForReady(Date.now() + timeoutMs, (error) => {
      if (error) reject(error);
      else resolve();
    });
  });
}

function listNotes(): Promise<{ notes: Note[] }> {
  return new Promise((resolve, reject) => {
    client.ListNotes({}, (error, response) => {
      if (error) reject(error);
      else resolve(response);
    });
  });
}

function addNote(title: string, body: string): Promise<Note> {
  return new Promise((resolve, reject) => {
    client.AddNote({ title, body }, (error, response) => {
      if (error) reject(error);
      else resolve(response);
    });
  });
}

try {
  await waitForReady();
  const added = await addNote("from client", "npm run client");
  const listed = await listNotes();
  console.log("added", added);
  console.log("notes", listed.notes);
} catch (error) {
  console.error("grpc client failed:", error);
  process.exitCode = 1;
} finally {
  client.close();
}
