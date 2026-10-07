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
import type { RendererFeedback } from "./types.ts";

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

function feedbackProps(feedback: RendererFeedback, revealed = false) {
  return {
    item: { ...dragItem, mode: "typed" }, units: [], pending: false, submitError: null,
    feedback, revealed, onSubmit: vi.fn(), onContinue: vi.fn(),
    onTryAgain: vi.fn(), onShowAnswer: vi.fn(),
  };
}

const richFeedback: RendererFeedback = {
  category: "incorrect", submitted: "ship it", expected: "rolling out",
  explanation: 'Use a paragraph in context. Expected answer: “ROLLING OUT”.',
  chunks_used: ["follow through"], chunks_missed: ["rolling out"],
  natural_alternative: "deploying the change",
};

it.each(["correct", "corrected"])("fills the accepted phrase once inline for %s without a card/input", (category) => {
  render(<GapFillRenderer {...feedbackProps({ ...richFeedback, category, submitted: "  Rolling OUT  " })} />);
  const blank = screen.getByTestId("gap-fill-blank");
  expect(blank.textContent).toBe("rolling out");
  expect(blank.className).toMatch(/accepted/);
  expect(screen.getByRole("status")).toHaveTextContent(category === "correct" ? "Correct" : "Corrected");
  expect(screen.queryByRole("textbox", { name: "Answer" })).not.toBeInTheDocument();
  expect(screen.queryByText("Details")).not.toBeInTheDocument();
  expect(screen.queryByTestId("submitted-answer")).not.toBeInTheDocument();
  expect(screen.queryByTestId("reference-answer")).not.toBeInTheDocument();
  expect(screen.getByTestId("feedback-card").querySelector("article")).toBeNull();
  expect(screen.getAllByText("rolling out", { exact: true })).toHaveLength(1);
  expect(screen.queryByText("  Rolling OUT  ", { exact: true })).not.toBeInTheDocument();
});

it("keeps the solution and deferred education unmounted on an incorrect result", () => {
  const feedback = { ...richFeedback, submitted: "  ship it  " };
  render(<GapFillRenderer {...feedbackProps(feedback)} />);
  expect(screen.getByTestId("gap-fill-blank").textContent).toBe(feedback.submitted);
  expect(screen.getByRole("status")).toHaveTextContent("Incorrect");
  expect(screen.queryByRole("textbox", { name: "Answer" })).not.toBeInTheDocument();
  const result = screen.getByTestId("feedback-card");
  for (const value of [feedback.expected, feedback.explanation, "follow through", "deploying the change", "Chunks used", "Chunks missed", "Details"]) {
    expect(result.innerHTML).not.toContain(value);
  }
  expect(screen.getByRole("button", { name: "Try again" })).toBeEnabled();
  expect(screen.getByRole("button", { name: "Show answer" })).toBeEnabled();
});

it("Show answer fills the blank without recall credit or commands and keeps Try again available", async () => {
  const props = feedbackProps(richFeedback);
  const original = structuredClone(richFeedback);
  const { rerender } = render(<GapFillRenderer {...props} />);
  await userEvent.setup().click(screen.getByRole("button", { name: "Show answer" }));
  expect(props.onShowAnswer).toHaveBeenCalledExactlyOnceWith();
  rerender(<GapFillRenderer {...props} revealed />);
  expect(screen.getByTestId("gap-fill-blank")).toHaveTextContent("rolling out");
  expect(screen.getByTestId("gap-fill-blank").className).not.toMatch(/accepted/);
  expect(screen.getByRole("status")).toHaveTextContent("Incorrect");
  expect(screen.getAllByText("rolling out", { exact: true })).toHaveLength(1);
  expect(screen.queryByText("ship it", { exact: true })).not.toBeInTheDocument();
  expect(screen.getByRole("button", { name: "Try again" })).toBeEnabled();
  expect(screen.queryByRole("button", { name: "Show answer" })).not.toBeInTheDocument();
  expect(props.onSubmit).not.toHaveBeenCalled();
  expect(props.onContinue).not.toHaveBeenCalled();
  expect(props.feedback).toEqual(original);
});

it.each([false, true])("Try again clears the inline answer/result and permits entry (revealed=%s)", async (revealed) => {
  const props = feedbackProps(richFeedback, revealed);
  const { rerender } = render(<GapFillRenderer {...props} />);
  await userEvent.setup().click(screen.getByRole("button", { name: "Try again" }));
  expect(props.onTryAgain).toHaveBeenCalledExactlyOnceWith();
  expect(props.onSubmit).not.toHaveBeenCalled();
  expect(props.onContinue).not.toHaveBeenCalled();
  rerender(<GapFillRenderer {...props} feedback={null} revealed={false} />);
  expect(screen.getByTestId("gap-fill-blank")).toBeEmptyDOMElement();
  expect(screen.queryByRole("status")).not.toBeInTheDocument();
  expect(screen.queryByTestId("feedback-card")).not.toBeInTheDocument();
  expect(screen.getByRole("textbox", { name: "Answer" })).toHaveValue("");
  await userEvent.setup().type(screen.getByRole("textbox", { name: "Answer" }), "new response");
  await userEvent.setup().click(screen.getByRole("button", { name: "Submit Answer" }));
  expect(props.onSubmit).toHaveBeenCalledExactlyOnceWith({ text: "new response", submittedUnitId: null });
});

it.each(["correct", "corrected", "incorrect"])("never displays deferred educational fields for %s even after disclosure", (category) => {
  const feedback = { ...richFeedback, category, explanation: '<script>alert(1)</script> Original teaching' };
  const snapshot = structuredClone(feedback);
  render(<GapFillRenderer {...feedbackProps(feedback, true)} />);
  const result = screen.getByTestId("feedback-card");
  for (const text of ["Details", "Chunks used", "Chunks missed", "Natural alternative", "Original teaching", "follow through", "deploying the change", "alert(1)"]) {
    expect(result.innerHTML).not.toContain(text);
  }
  expect(result.querySelector("details, article, script")).toBeNull();
  expect(feedback).toEqual(snapshot);
});

it("renders hostile inline answer markup as inert text", () => {
  const expected = "<img src=x onerror=alert(1)>";
  render(<GapFillRenderer {...feedbackProps({ ...richFeedback, category: "correct", expected })} />);
  expect(screen.getByTestId("gap-fill-blank").textContent).toBe(expected);
  expect(screen.getByTestId("gap-fill-blank").querySelector("img")).toBeNull();
});

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
  expect(css).toMatch(/\.answered\s*\{[^}]*overflow-wrap:\s*anywhere/s);
  expect(css).toMatch(/\.accepted\s*\{[^}]*color:\s*var\(--color-accent\)/s);
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

it("shows a labeled typed answer and replaces entry with the inline response after grading", () => {
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
  expect(answer).toHaveAttribute("autocomplete", "off");
  expect(answer).toHaveAttribute("readonly");
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

  expect(screen.queryByRole("textbox", { name: "Answer" })).not.toBeInTheDocument();
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

it("removes chips after grading so accepted text is not duplicated", () => {
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

  expect(screen.queryByTestId("chip-bank")).not.toBeInTheDocument();
  expect(screen.getByTestId("gap-fill-blank")).toHaveTextContent("rolling out");
  expect(screen.getAllByText("rolling out", { exact: true })).toHaveLength(1);
  expect(screen.getByRole("button", { name: "Continue" })).toBeEnabled();
  expect(screen.queryByRole("button", { name: "Retry" })).not.toBeInTheDocument();
});
