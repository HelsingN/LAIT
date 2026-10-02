import type { CreateClientConfig } from "./generated/client.gen.ts";

function sameOriginBase(): string {
  const origin = globalThis.location?.origin;
  if (!origin || origin === "null") {
    return "";
  }
  return origin;
}

export const createClientConfig: CreateClientConfig = (override) => ({
  ...override,
  baseUrl: override?.baseUrl || sameOriginBase(),
  // The generator calls fetch with a Request. Tests stub global fetch as (url, init).
  fetch: async (input: RequestInfo | URL, init?: RequestInit) => {
    if (input instanceof Request && init === undefined) {
      const method = input.method.toUpperCase();
      const body =
        method === "GET" || method === "HEAD" ? undefined : await input.clone().text();
      const parsed = new URL(input.url);
      return globalThis.fetch(`${parsed.pathname}${parsed.search}`, {
        method,
        headers: input.headers,
        body: body ? body : undefined,
      });
    }
    return globalThis.fetch(input, init);
  },
});
