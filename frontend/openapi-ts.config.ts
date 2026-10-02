import { defineConfig } from "@hey-api/openapi-ts";

export default defineConfig({
  input: "./openapi.json",
  output: "./src/api/generated",
  plugins: [
    {
      name: "@hey-api/client-fetch",
      baseUrl: false,
      bundle: true,
      throwOnError: false,
      runtimeConfigPath: "./src/api/client-config.ts",
    },
    "@hey-api/typescript",
    {
      name: "@hey-api/sdk",
      auth: false,
    },
  ],
});
