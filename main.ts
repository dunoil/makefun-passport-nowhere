import { copyFileSync, readFileSync, mkdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const dest = join(outDir, "entry.png");

const buf = readFileSync(src);
const PNG_SIG = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (buf.length < 8 || !buf.subarray(0, 8).equals(PNG_SIG)) {
  throw new Error("entry.png: invalid PNG signature");
}
if (buf.length > 1_048_576) {
  throw new Error(`entry.png: ${buf.length} bytes exceeds 1 MiB limit`);
}
mkdirSync(outDir, { recursive: true });
copyFileSync(src, dest);
// Re-read the copied file so a truncated copy fails loudly instead of shipping.
const written = readFileSync(dest);
if (!written.equals(buf)) {
  throw new Error("entry.png: copied file does not match source");
}
console.log(`Wrote ${dest} (${buf.length} bytes)`);
