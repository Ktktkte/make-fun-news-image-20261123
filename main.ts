import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Entry for news-image-20261123: place the drawn front page into the
// grader's output directory as entry.png.
const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const targetDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(targetDir, "entry.png");

if (!existsSync(source)) {
  console.error(`missing entry image: ${source}`);
  process.exit(1);
}

mkdirSync(targetDir, { recursive: true });
copyFileSync(source, target);

if (!existsSync(target)) {
  console.error(`copy failed: ${target} was not created`);
  process.exit(1);
}
console.log(`wrote ${target}`);
