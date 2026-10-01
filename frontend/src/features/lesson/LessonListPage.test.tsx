// @vitest-environment jsdom
import "@testing-library/jest-dom/vitest";
import { cleanup, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, expect, it, vi } from "vitest";
import { MemoryRouter } from "react-router";

import { LessonListPage } from "./LessonListPage.tsx";

const directory = dirname(fileURLToPath(import.meta.url));

function jsonResponse(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json" },
  });
}

function renderList() {
  const client = new QueryClient({
    defaultOptions: { queries: { retry: false, refetchOnWindowFocus: false } },
  });
  return render(
    <QueryClientProvider client={client}>
      <MemoryRouter>
        <LessonListPage />
      </MemoryRouter>
    </QueryClientProvider>,
  );
}

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

it("shows the empty lesson list copy and Create Lesson", async () => {
  vi.stubGlobal("fetch", vi.fn(async () => jsonResponse({ lessons: [] })));
  renderList();
  expect(await screen.findByRole("heading", { name: "No lessons yet" })).toBeInTheDocument();
  expect(
    screen.getByText(
      "Paste a short English text to create your first lesson, then mark phrases to practice.",
    ),
  ).toBeInTheDocument();
  expect(screen.getByRole("button", { name: "Create Lesson" })).toBeInTheDocument();
});

it("shows Loading… in the header without replacing the page", () => {
  vi.stubGlobal("fetch", vi.fn(() => new Promise<Response>(() => {})));
  renderList();
  expect(screen.getByRole("heading", { name: "Lessons" })).toBeInTheDocument();
  expect(screen.getByText("Loading…")).toBeInTheDocument();
  expect(screen.getByRole("button", { name: "Create Lesson" })).toBeInTheDocument();
});

it("shows the load error and a link back to the lesson list", async () => {
  vi.stubGlobal("fetch", vi.fn(async () => new Response("nope", { status: 500 })));
  renderList();
  expect(
    await screen.findByText("Could not load this lesson. Return to the lesson list and open it again."),
  ).toBeInTheDocument();
  expect(screen.getByRole("link", { name: "Lessons" })).toHaveAttribute("href", "/");
});

it("falls back to Untitled Lesson and puts the full title in the title attribute", async () => {
  const longTitle = "A lesson title that is far too long to fit on one line in the list";
  vi.stubGlobal(
    "fetch",
    vi.fn(async () =>
      jsonResponse({
        lessons: [
          {
            id: "blank",
            title: "   ",
            source: "text",
            created_at: "2026-10-01T00:00:00+00:00",
          },
          {
            id: "long",
            title: longTitle,
            source: "text",
            created_at: "2026-10-01T00:00:00+00:00",
          },
        ],
      }),
    ),
  );
  renderList();
  expect(await screen.findByText("Untitled Lesson")).toBeInTheDocument();
  expect(screen.getByTitle(longTitle)).toHaveTextContent(longTitle);
  expect(screen.getAllByRole("link", { name: "Open" })).toHaveLength(2);
  const listCss = readFileSync(join(directory, "LessonListPage.module.css"), "utf8");
  expect(listCss).toMatch(/\.rowTitle\s*\{[^}]*text-overflow:\s*ellipsis/s);
  expect(listCss).toMatch(/white-space:\s*nowrap/);
});

it("shows Creating… and keeps the pasted source when create fails", async () => {
  const user = userEvent.setup();
  let releaseCreate: ((response: Response) => void) | undefined;
  vi.stubGlobal(
    "fetch",
    vi.fn((input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      const method = (init?.method ?? "GET").toUpperCase();
      if (method === "POST" && url.includes("/api/lessons")) {
        return new Promise<Response>((resolve) => {
          releaseCreate = resolve;
        });
      }
      return Promise.resolve(jsonResponse({ lessons: [] }));
    }),
  );
  renderList();
  await screen.findByRole("heading", { name: "No lessons yet" });
  await user.type(screen.getByLabelText("Source"), "I was responsible for the migration.");
  await user.click(screen.getByRole("button", { name: "Create Lesson" }));
  expect(screen.getByRole("button", { name: "Creating…" })).toBeDisabled();
  releaseCreate?.(new Response("nope", { status: 500 }));
  expect(
    await screen.findByText("Could not create the lesson. Check the pasted text and try Create Lesson again."),
  ).toBeInTheDocument();
  expect(screen.getByLabelText("Source")).toHaveValue("I was responsible for the migration.");
});

it("suggests Untitled Lesson and wraps the title field to two lines", async () => {
  vi.stubGlobal("fetch", vi.fn(async () => jsonResponse({ lessons: [] })));
  const user = userEvent.setup();
  renderList();
  await screen.findByRole("heading", { name: "No lessons yet" });
  const title = screen.getByLabelText("Title");
  expect(title.tagName).toBe("TEXTAREA");
  await user.type(screen.getByLabelText("Source"), "!!!");
  expect(title).toHaveValue("Untitled Lesson");
  const listCss = readFileSync(join(directory, "LessonListPage.module.css"), "utf8");
  expect(listCss).toMatch(/\.titleInput\s*\{[^}]*max-height:[^}]*overflow:\s*auto/s);
});
