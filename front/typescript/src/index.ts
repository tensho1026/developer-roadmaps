import { z } from "zod";

const User = z.object({
  id: z.number(),
  email: z.string().email(),
});

const user = User.parse({ id: 1, email: "ada@example.com" });
console.log("TypeScript + Zod:", user);
