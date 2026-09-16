import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import chalk from "chalk";
import { Command } from "commander";

type Note = { id: number; text: string };
const file = join(dirname(fileURLToPath(import.meta.url)), "../notes.json");

function load(): Note[] {
  try {
    return JSON.parse(readFileSync(file, "utf8")) as Note[];
  } catch {
    return [];
  }
}

function save(notes: Note[]) {
  writeFileSync(file, JSON.stringify(notes, null, 2));
}

const program = new Command();
program.name("roadmaps").description("Full-stack roadmap CLI checkpoint");

program
  .command("notes")
  .description("list notes")
  .action(() => {
    const notes = load();
    if (notes.length === 0) {
      console.log(chalk.dim("no notes yet. try: npm start -- add \"hello\""));
      return;
    }
    for (const note of notes) {
      console.log(`${chalk.cyan(String(note.id))} ${note.text}`);
    }
  });

program
  .command("add")
  .argument("<text>")
  .action((text: string) => {
    const notes = load();
    const note = { id: (notes.at(-1)?.id ?? 0) + 1, text };
    notes.push(note);
    save(notes);
    console.log(chalk.green(`added #${note.id}`));
  });

program.parse();
