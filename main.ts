// news-image-20261119 — ship the finished front page.
//
// The artwork itself is baked into entry.png by draw.py (Pillow). This
// little launcher has one job: place an exact copy of that PNG in the
// directory the grader reads from, so the bytes the judge sees are the
// bytes we drew. Nothing is generated or altered at run time.
//
// Where the file goes:
//   * Inside the grading container the destination is /output.
//   * Anywhere else, MAKEFUN_OUTPUT_DIR overrides it, e.g.:
//         mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
//
// Node 22, standard library only — no dependencies to install.

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// The folder this script lives in is also where entry.png lives.
const scriptDir = dirname(fileURLToPath(import.meta.url));

// Resolve the destination, then make sure it exists before copying.
const destination = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(destination, { recursive: true });

copyFileSync(join(scriptDir, "entry.png"), join(destination, "entry.png"));
