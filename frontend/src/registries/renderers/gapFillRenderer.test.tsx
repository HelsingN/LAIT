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
import { GapFillRenderer } from "./GapFillRenderer.tsx";

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
  await user.click(screen.getByRole("button", { name: "Exercises", expanded: false }));
  await user.click(
    within(screen.getByRole("region", { name: "Exercises" })).getByRole("button", {
      name: "Generate Exercises",
    }),
  );
  await user.click(await screen.findByRole("button", { name: "Start Practice" }));

  const blank = await screen.findByTestId("gap-fill-blank");
  expect(blank.textContent ?? "").not.toMatch(/_/);
  expect(getComputedStyle(blank).display).not.toBe("block");
  const sentence = screen.getByTestId("gap-fill-sentence");
  expect(sentence).toHaveTextContent("I was responsible for");
  expect(sentence).toHaveTextContent("the migration.");
  expect(screen.queryByText("kept-off-screen")).not.toBeInTheDocument();
  expect(screen.queryByText("official.exercise.gap-fill")).not.toBeInTheDocument();

  const css = readFileSync(join(testDirectory, "GapFillRenderer.module.css"), "utf8");
  expect(css).toMatch(/\.sentence\s*\{[^}]*overflow-wrap:\s*anywhere/s);
  expect(css).toMatch(/\.sentence\s*\{[^}]*font-family:\s*var\(--font-source\)/s);
  expect(css).toMatch(/\.blank\s*\{[^}]*display:\s*inline-block/s);
  expect(css).toMatch(/\.blank\s*\{[^}]*min-width:\s*4\.5rem/s);
  expect(css).toMatch(/\.blank\s*\{[^}]*border-bottom:\s*2px solid var\(--color-accent\)/s);
  expect(css).not.toMatch(/\.blank\s*\{[^}]*text-decoration/s);
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

it("renders chips in chip_unit_ids order", () => {
  const reversed = {
    ...dragItem,
    chip_unit_ids: ["unit-2", "unit-1"],
  };
  render(
    <GapFillRenderer
      item={reversed}
      units={[
        { id: "unit-1", text: "rolling out" },
        { id: "unit-2", text: "the migration" },
      ]}
      pending={false}
      submitError={null}
      feedback={null}
      onSubmit={() => undefined}
      onContinue={() => undefined}
    />,
  );

  const buttons = within(screen.getByTestId("chip-bank")).getAllByRole("button");
  expect(buttons.map((button) => button.textContent)).toEqual(["the migration", "rolling out"]);
});

it("strips emphasis markers and leaves identifier underscores", () => {
  render(
    <GapFillRenderer
      item={{
        ...dragItem,
        segments: [
          { kind: "text", text: "*responsible* **rolling** _out_ file_name " },
          { kind: "blank", text: "______" },
        ],
      }}
      units={[]}
      pending={false}
      submitError={null}
      feedback={null}
      onSubmit={() => undefined}
      onContinue={() => undefined}
    />,
  );

  const sentence = screen.getByTestId("gap-fill-sentence");
  expect(sentence).toHaveTextContent("responsible rolling out file_name");
  expect(sentence).not.toHaveTextContent("*");
  expect(screen.getByTestId("gap-fill-blank").textContent ?? "").not.toMatch(/_/);
});

it("shows a labeled typed answer and locks it after a grade", () => {
  const { rerender } = render(
    <GapFillRenderer
      item={{ ...dragItem, mode: "typed" }}
      units={[]}
      pending={false}
      submitError={null}
      feedback={null}
      onSubmit={() => undefined}
      onContinue={() => undefined}
    />,
  );

  const answer = screen.getByRole("textbox", { name: "Answer" });
  expect(screen.getByText("Type the missing words.")).toBeVisible();
  expect(answer).toHaveAccessibleDescription("Type the missing words.");
  const css = readFileSync(join(testDirectory, "GapFillRenderer.module.css"), "utf8");
  expect(css).toMatch(/\.answer\s*\{[^}]*border:\s*1px solid var\(--color-text\)/s);

  rerender(
    <GapFillRenderer
      item={{ ...dragItem, mode: "typed" }}
      units={[]}
      pending={false}
      submitError={null}
      feedback={{
        category: "incorrect",
        submitted: "nope",
        expected: "rolling out",
        explanation: "miss",
        chunks_used: [],
        chunks_missed: [],
        natural_alternative: null,
      }}
      onSubmit={() => undefined}
      onContinue={() => undefined}
    />,
  );

  expect(screen.getByRole("textbox", { name: "Answer" })).toBeDisabled();
  expect(screen.getByRole("button", { name: "Continue" })).toBeEnabled();
  expect(screen.getByRole("button", { name: "Try again" })).toBeEnabled();
  expect(screen.getByRole("button", { name: "Show answer" })).toBeEnabled();
  expect(screen.queryByRole("button", { name: "Retry" })).not.toBeInTheDocument();
  expect(screen.getByTestId("feedback-card")).toHaveTextContent("Incorrect");
  expect(screen.getByTestId("feedback-card")).toHaveTextContent("nope");
  expect(screen.getByTestId("feedback-card")).not.toHaveTextContent("rolling out");
});

it("clears a typed draft when the grade is cleared for another try", async () => {
  const user = userEvent.setup();
  const item = { ...dragItem, mode: "typed" };
  const props = {
    item,
    units: [],
    pending: false,
    submitError: null,
    onSubmit: () => undefined,
    onContinue: () => undefined,
  };
  const { rerender } = render(<GapFillRenderer {...props} feedback={null} />);
  await user.type(screen.getByRole("textbox", { name: "Answer" }), "nope");
  rerender(
    <GapFillRenderer
      {...props}
      feedback={{
        category: "incorrect",
        submitted: "nope",
        expected: "rolling out",
        explanation: "miss",
        chunks_used: [],
        chunks_missed: [],
        natural_alternative: null,
      }}
    />,
  );
  rerender(<GapFillRenderer {...props} feedback={null} />);
  expect(screen.getByRole("textbox", { name: "Answer" })).toHaveValue("");
  expect(screen.getByRole("button", { name: "Submit Answer" })).toBeDisabled();
});

it("ignores chip clicks after a grade", async () => {
  const user = userEvent.setup();
  render(
    <GapFillRenderer
      item={dragItem}
      units={[
        { id: "unit-1", text: "rolling out" },
        { id: "unit-2", text: "the migration" },
      ]}
      pending={false}
      submitError={null}
      feedback={{
        category: "correct",
        submitted: "rolling out",
        expected: "rolling out",
        explanation: "matched",
        chunks_used: [],
        chunks_missed: [],
        natural_alternative: null,
      }}
      onSubmit={() => undefined}
      onContinue={() => undefined}
    />,
  );

  const chips = within(screen.getByTestId("chip-bank")).getAllByRole("button");
  expect(chips.every((chip) => chip.hasAttribute("disabled"))).toBe(true);
  await user.click(chips[0]!);
  expect(chips.every((chip) => chip.getAttribute("aria-pressed") !== "true")).toBe(true);
  expect(screen.getByRole("button", { name: "Continue" })).toBeEnabled();
  expect(screen.queryByRole("button", { name: "Retry" })).not.toBeInTheDocument();
});
