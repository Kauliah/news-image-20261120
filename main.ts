// Entry program for make.fun news-image-20261120.
//
// Copies the built image (entry.png, sitting next to this file) into the
// output directory named by the MAKEFUN_OUTPUT_DIR environment variable
// ("out" when the variable is not set), creating that directory first.
// Standard library only; runs on Node 22.

import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const targetDir = process.env.MAKEFUN_OUTPUT_DIR || "out";

if (!existsSync(source)) {
  console.error(`entry.png not found next to main.ts (${source})`);
  process.exit(1);
}

mkdirSync(targetDir, { recursive: true });
copyFileSync(source, join(targetDir, "entry.png"));
console.log(`entry.png -> ${join(targetDir, "entry.png")}`);
