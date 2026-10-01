// @vitest-environment jsdom
import "@testing-library/jest-dom/vitest";
import { cleanup, render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, expect, it, vi } from "vitest";
import { MemoryRouter, Route, Routes } from "react-router";

import { LessonWorkspacePage } from "../../features/lesson/LessonWorkspacePage.tsx";

const lessonId = "lesson-1";
const testDirectory = dirname(fileURLToPath(import.meta.url));

const lesson = {
  id: lessonId,
  title: "Rolling out",
  source: "I was responsible for rolling out the migration.",
  created_at: "2026-10-01T00:00:00+00:00",
};

const units = [
  {
    id: "unit-1",
    lesson_id: lessonId,
    start: 23,
    end: 34,
    text: "rolling out",
    status: "accepted",
    created_at: "2026-10-01T00:00:00+00:00",
    removed_at: null,
  },
  {
    id: "unit-2",
    lesson_id: lessonId,
    start: 35,
    end: 48,
    text: "the migration",
    status: "accepted",
    created_at: "2026-10-01T00:00:00+00:00",
    removed_at: null,
  },
];

const dragItem = {
  mode: "drag",
  learning_unit_id: "unit-1",
  exercise_type: "gap-fill",
  position: 0,
  start: 23,
  end: 34,
  target_text: "rolling out",
  sentence: "I was responsible for ______ the migration.",
  segments: [
    { kind: "text", text: "I was responsible for " },
    { kind: "blank", text: "______" },
    { kind: "text", text: "the migration." },
  ],
  chip_unit_ids: ["unit-1", "unit-2"],
};

function jsonResponse(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json" },
  });
}

afterEach(() => {
  cleanup();
  localStorage.clear();
  vi.unstubAllGlobals();
});

it("wraps the blank inline and scrolls the chip bank", async () => {
  const user = userEvent.setup();
  vi.stubGlobal(
    "fetch",
    vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      const method = (init?.method ?? "GET").toUpperCase();
      if (url.includes("/api/exercise-registry")) {
        return jsonResponse({
          exercises: [{ exercise_type: "gap-fill", visibility: "learner", module_id: "kept-off-screen" }],
        });
      }
      if (url.includes("/learning-units") && method === "GET") {
        return jsonResponse({ learning_units: units });
      }
      if (url.includes("/exercises/generate") && method === "POST") {
        return jsonResponse({
          id: "gen-1",
          lesson_id: lessonId,
          status: "completed",
          accepted_unit_ids: ["unit-1", "unit-2"],
          definition_count: 2,
        });
      }
      if (url === "/api/practice-sessions" && method === "POST") {
        return jsonResponse(
          {
            session_id: "session-1",
            lesson_id: lessonId,
            open: true,
            cursor: 0,
            current: dragItem,
          },
          201,
        );
      }
      if (url.includes(`/api/lessons/${lessonId}`) && method === "GET") {
        return jsonResponse(lesson);
      }
      return new Response("missing", { status: 404 });
    }),
  );

  const client = new QueryClient({
    defaultOptions: { queries: { retry: false, refetchOnWindowFocus: false } },
  });
  render(
    <QueryClientProvider client={client}>
      <MemoryRouter initialEntries={[`/lessons/${lessonId}`]}>
        <Routes>
          <Route path="/lessons/:id" element={<LessonWorkspacePage />} />
        </Routes>
      </MemoryRouter>
    </QueryClientProvider>,
  );

  await screen.findByRole("heading", { name: "Rolling out" });
  await user.click(screen.getByRole("button", { name: "Generate Exercises", expanded: false }));
  await user.click(
    within(screen.getByRole("region", { name: "Generate Exercises" })).getByRole("button", {
      name: "Generate Exercises",
    }),
  );
  await user.click(await screen.findByRole("button", { name: "Start Practice" }));

  const blank = await screen.findByTestId("gap-fill-blank");
  expect(blank).toHaveTextContent("______");
  expect(getComputedStyle(blank).display).not.toBe("block");
  const sentence = screen.getByTestId("gap-fill-sentence");
  expect(sentence).toHaveTextContent("I was responsible for");
  expect(sentence).toHaveTextContent("the migration.");
  expect(screen.queryByText("kept-off-screen")).not.toBeInTheDocument();
  expect(screen.queryByText("official.exercise.gap-fill")).not.toBeInTheDocument();

  const css = readFileSync(join(testDirectory, "GapFillRenderer.module.css"), "utf8");
  expect(css).toMatch(/\.sentence\s*\{[^}]*overflow-wrap:\s*anywhere/s);
  expect(css).toMatch(/\.sentence\s*\{[^}]*font-family:\s*var\(--font-source\)/s);
  expect(css).toMatch(/\.blank\s*\{[^}]*display:\s*inline/s);
  expect(css).toMatch(/\.chipBank\s*\{[^}]*flex-wrap:\s*wrap/s);
  expect(css).toMatch(/\.chipBank\s*\{[^}]*max-height:\s*40vh/s);
  expect(css).toMatch(/\.chipBank\s*\{[^}]*overflow-y:\s*auto/s);
  expect(css).toMatch(/\.card\s*\{[^}]*overflow-wrap:\s*anywhere/s);
  expect(css).not.toMatch(/overflow-x:\s*scroll/);

  const focusCss = readFileSync(
    join(testDirectory, "../../features/lesson/FocusPracticeMode.module.css"),
    "utf8",
  );
  expect(focusCss).toMatch(/overflow-x:\s*hidden/);
});
