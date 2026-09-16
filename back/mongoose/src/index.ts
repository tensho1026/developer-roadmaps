import "dotenv/config";
import cors from "cors";
import express from "express";
import mongoose from "mongoose";
import { z } from "zod";

const app = express();
const port = Number(process.env.PORT ?? 3030);
const mongoUrl =
  process.env.MONGO_URL ??
  "mongodb://roadmaps:roadmaps@localhost:27017/roadmaps?authSource=admin";

app.use(cors());
app.use(express.json());

const noteSchema = new mongoose.Schema(
  {
    title: { type: String, required: true },
    body: { type: String, required: true },
  },
  { timestamps: true },
);

const Note = mongoose.model("Note", noteSchema);
const CreateNote = z.object({
  title: z.string().min(1),
  body: z.string().min(1),
});

function mongoReady() {
  return mongoose.connection.readyState === 1;
}

async function seedIfEmpty() {
  if ((await Note.countDocuments()) > 0) return;
  await Note.create({ title: "Mongo lab", body: "seeded by mongoose playground" });
  console.log("mongoose: seeded empty notes collection");
}

app.get("/health", (_req, res) => {
  const db = mongoReady();
  res.status(db ? 200 : 503).json({ ok: db, db, odm: "mongoose" });
});

app.get("/notes", async (_req, res) => {
  if (!mongoReady()) {
    res.status(503).json({ error: "mongodb not connected" });
    return;
  }
  res.json(await Note.find().sort({ createdAt: -1 }).lean());
});

app.post("/notes", async (req, res) => {
  if (!mongoReady()) {
    res.status(503).json({ error: "mongodb not connected" });
    return;
  }
  const parsed = CreateNote.safeParse(req.body);
  if (!parsed.success) {
    res.status(400).json(parsed.error.flatten());
    return;
  }
  const note = await Note.create(parsed.data);
  res.status(201).json(note);
});

app.delete("/notes/:id", async (req, res) => {
  if (!mongoReady()) {
    res.status(503).json({ error: "mongodb not connected" });
    return;
  }
  try {
    const deleted = await Note.findByIdAndDelete(req.params.id);
    if (!deleted) {
      res.status(404).json({ error: "not found" });
      return;
    }
    res.status(204).end();
  } catch (error) {
    res.status(400).json({ error: String(error) });
  }
});

async function main() {
  try {
    await mongoose.connect(mongoUrl, { serverSelectionTimeoutMS: 3000 });
    await seedIfEmpty();
    console.log("mongoose connected");
  } catch (error) {
    console.warn("mongodb not connected:", error);
  }
  app.listen(port, () => {
    console.log(`mongoose crud on http://localhost:${port}`);
  });
}

void main();
