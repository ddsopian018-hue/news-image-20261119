// news-image-20261119 (Node 22, standard library only): the entry is the
// front page drawn by draw.py and stored here as entry.png. This program
// copies that fixed image to the output directory, so running it twice
// writes identical bytes. The gate takes a whole PNG of at most 1 MiB and
// 1024 by 1024 pixels; the judge sees exactly the bytes copied.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, 'entry.png'), join(outDir, 'entry.png'));
