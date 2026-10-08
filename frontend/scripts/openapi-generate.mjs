import { spawnSync } from "node:child_process";
import { existsSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const frontendRoot = dirname(dirname(fileURLToPath(import.meta.url)));
const specPath = join(frontendRoot, "openapi.json");

if (!existsSync(specPath)) {
  console.error(
    "frontend/openapi.json is missing. Run: uv run python -m lait.adapters.http.export_openapi",
  );
  process.exit(1);
}

// Generate in place. Do not restore or delete the output if this process dies:
// a partial client must leave the tree dirty so the CI diff fails closed.
const cli = join(frontendRoot, "node_modules", "@hey-api", "openapi-ts", "bin", "run.js");
const result = spawnSync(process.execPath, [cli], {
  cwd: frontendRoot,
  stdio: "inherit",
});

if (result.error) {
  console.error(result.error);
  process.exit(1);
}

process.exit(result.status === null ? 1 : result.status);
