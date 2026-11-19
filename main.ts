// news-image-20261119 — entry program (Node 22, standard library only).
//
// The picture is the entry.png beside this file: it was drawn for the news of
// Thursday 19 November 2026 and is shipped as bytes, so the program's job is to
// put those exact bytes at /output/entry.png. The grader looks at the bytes, so
// nothing here may re-encode, rescale or re-render the image.
//
// The program refuses to hand the grader anything the competition would reject,
// which is cheaper to debug than a silent refusal downstream: the file must
// start with the PNG signature, its IHDR must say at most 1024 by 1024 pixels,
// and it must not be larger than one mebibyte.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, 'entry.png');
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const target = join(outputDir, 'entry.png');

const ONE_MEBIBYTE = 1024 * 1024;
const MAX_SIDE = 1024;

function fail(reason: string): never {
  console.error(`entry.png refused: ${reason}`);
  process.exit(1);
}

const bytes = readFileSync(source);

// PNG: an 8-byte signature, then the IHDR chunk, whose data starts at byte 16
// and holds width and height as big-endian 32-bit integers.
const signature = Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]);
if (bytes.length < 33 || !bytes.subarray(0, 8).equals(signature)) {
  fail('not a PNG file');
}
if (bytes.subarray(12, 16).toString('latin1') !== 'IHDR') {
  fail('first chunk is not IHDR');
}

const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width > MAX_SIDE || height > MAX_SIDE) {
  fail(`${width} by ${height} pixels is larger than ${MAX_SIDE} by ${MAX_SIDE}`);
}
if (bytes.length > ONE_MEBIBYTE) {
  fail(`${bytes.length} bytes is more than ${ONE_MEBIBYTE}`);
}

mkdirSync(outputDir, { recursive: true });
writeFileSync(target, bytes);

console.log(`wrote ${target}: ${width} by ${height}, ${bytes.length} bytes`);
