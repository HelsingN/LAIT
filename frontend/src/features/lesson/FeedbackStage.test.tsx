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

import { LessonWorkspacePage } from "./LessonWorkspacePage.tsx";

const lessonId = "lesson-1";
const testDirectory = dirname(fileURLToPath(import.meta.url));

const lesson = {
  id: lessonId,
  title: "Rolling out",
  source: "I was responsible for rolling out the migration.",
  created_at: "2026-10-01T00:00:00+00:00",
};

const unit = {
  id: "unit-1",
  lesson_id: lessonId,
  start: 22,
  end: 33,
  text: "rolling out",
  status: "accepted",
  created_at: "2026-10-01T00:00:00+00:00",
  removed_at: null,
};

const typedItem = {
  mode: "typed",
  learning_unit_id: "unit-1",
  exercise_type: "gap-fill",
  position: 0,
  start: 22,
  end: 33,
  target_text: "rolling out",
  sentence: "I was responsible for ______ the migration.",
  segments: [
    { kind: "text", text: "I was responsible for " },
    { kind: "blank", text: "______" },
    { kind: "text", text: "the migration." },
  ],
  chip_unit_ids: ["unit-1"],
};

const attempt = {
  attempt_id: "attempt-1",
  session_open: true,
  cursor: 1,
  category: "incorrect",
  submitted: "nope",
  expected: "rolling out",
  explanation: 'Your answer: "nope". Expected: "rolling out".',
  chunks_used: [],
  chunks_missed: ["rolling out"],
  natural_alternative: null,
  learning_unit_id: "unit-1",
  span_start: 22,
  span_end: 33,
  unit_text: "rolling out",
};

function jsonResponse(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json" },
  });
}

function renderWorkspace() {
  const client = new QueryClient({
    defaultOptions: { queries: { retry: false, refetchOnWindowFocus: false } },
  });
  return render(
    <QueryClientProvider client={client}>
      <MemoryRouter initialEntries={[`/lessons/${lessonId}`]}>
        <Routes>
          <Route path="/lessons/:id" element={<LessonWorkspacePage />} />
        </Routes>
      </MemoryRouter>
    </QueryClientProvider>,
  );
}

function installFetch() {
  let submitted = false;
  vi.stubGlobal(
    "fetch",
    vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      const method = (init?.method ?? "GET").toUpperCase();
      if (url.includes("/api/exercise-registry")) {
        return jsonResponse({
          exercises: [{ exercise_type: "gap-fill", visibility: "learner", module_id: "official.exercise.gap-fill" }],
        });
      }
      if (url.includes("/exercises/latest") && method === "GET") {
        return jsonResponse({
          restorable: false,
          generation_id: null,
          accepted_unit_ids: [],
        });
      }
      if (url.includes("/learning-units") && method === "GET") {
        return jsonResponse({ learning_units: [unit] });
      }
      if (url.includes("/exercises/generate") && method === "POST") {
        return jsonResponse({
          id: "gen-1",
          lesson_id: lessonId,
          status: "completed",
          accepted_unit_ids: ["unit-1"],
          definition_count: 1,
        });
      }
      if (url === "/api/practice-sessions" && method === "POST") {
        return jsonResponse(
          { session_id: "session-1", lesson_id: lessonId, open: true, cursor: 0, current: typedItem },
          201,
        );
      }
      if (url.includes("/practice-sessions/") && url.endsWith("/attempts") && method === "POST") {
        submitted = true;
        return jsonResponse(attempt);
      }
      if (url.includes("/lessons/") && url.endsWith("/attempts") && method === "GET") {
        return jsonResponse({
          attempts: submitted
            ? [
                {
                  attempt_id: attempt.attempt_id,
                  session_id: "session-1",
                  session_disposition: "exited",
                  mode: "typed",
                  category: attempt.category,
                  submitted: attempt.submitted,
                  expected: attempt.expected,
                  explanation: attempt.explanation,
                  unit_text: attempt.unit_text,
                  span_start: attempt.span_start,
                  span_end: attempt.span_end,
                  created_at: "2026-10-01T00:00:00+00:00",
                },
              ]
            : [],
        });
      }
      if (url.endsWith("/finish") && method === "POST") {
        return jsonResponse({
          session_id: "session-1",
          lesson_id: lessonId,
          open: false,
          cursor: 1,
          current: null,
        });
      }
      if (url.endsWith("/start-over") && method === "POST") {
        return jsonResponse({
          session_id: "session-2",
          lesson_id: lessonId,
          open: true,
          cursor: 0,
          current: typedItem,
        });
      }
      if (url.includes(`/api/lessons/${lessonId}`) && method === "GET") {
        return jsonResponse(lesson);
      }
      return new Response("missing", { status: 404 });
    }),
  );
}

async function generateAndStart(user: ReturnType<typeof userEvent.setup>) {
  await screen.findByRole("heading", { name: "Rolling out" });
  await user.click(screen.getByRole("button", { name: "Exercises", expanded: false }));
  await user.click(
    within(screen.getByRole("region", { name: "Exercises" })).getByRole("button", {
      name: "Generate Exercises",
    }),
  );
  await user.click(await screen.findByRole("button", { name: "Start Practice" }));
}

afterEach(() => {
  cleanup();
  localStorage.clear();
  vi.unstubAllGlobals();
});

it("shows the empty copy after leaving practice with no attempts", async () => {
  const user = userEvent.setup();
  installFetch();
  renderWorkspace();
  await screen.findByRole("heading", { name: "Rolling out" });
  expect(screen.getByRole("button", { name: "Feedback" })).toBeDisabled();

  await generateAndStart(user);
  await user.click(screen.getByRole("button", { name: "Exit Practice" }));

  const feedback = await screen.findByRole("region", { name: "Feedback" });
  expect(feedback).toHaveTextContent("No attempts yet. Start Practice to begin.");
  expect(screen.getByRole("button", { name: "Feedback" })).toBeEnabled();
});

it("lists category explanation and an excerpt jump", async () => {
  const user = userEvent.setup();
  installFetch();
  renderWorkspace();
  await generateAndStart(user);
  await user.type(screen.getByRole("textbox", { name: "Answer" }), "nope");
  await user.click(screen.getByRole("button", { name: "Submit Answer" }));
  await screen.findByTestId("feedback-card");
  await user.click(screen.getByRole("button", { name: "Exit Practice" }));

  const feedback = await screen.findByRole("region", { name: "Feedback" });
  expect(feedback).toHaveTextContent("incorrect");
  expect(feedback).toHaveTextContent('Your answer: "nope". Expected: "rolling out".');
  await user.click(within(feedback).getByRole("button", { name: "rolling out" }));

  expect(screen.getByRole("button", { name: "Source", expanded: true })).toBeInTheDocument();
  expect(document.getElementById("source-highlight")).toHaveTextContent("rolling out");

  const css = readFileSync(join(testDirectory, "stages", "FeedbackStage.module.css"), "utf8");
  expect(css).toMatch(/overflow-wrap:\s*anywhere/);
});

it("keeps listed attempts after start over", async () => {
  const user = userEvent.setup();
  installFetch();
  renderWorkspace();
  await generateAndStart(user);
  await user.type(screen.getByRole("textbox", { name: "Answer" }), "nope");
  await user.click(screen.getByRole("button", { name: "Submit Answer" }));
  await screen.findByTestId("feedback-card");
  await user.click(screen.getByRole("button", { name: "Start Over" }));
  await user.click(within(screen.getByRole("alertdialog")).getByRole("button", { name: "Start Over" }));
  await user.click(screen.getByRole("button", { name: "Exit Practice" }));

  const feedback = await screen.findByRole("region", { name: "Feedback" });
  expect(feedback).toHaveTextContent("incorrect");
  expect(feedback).toHaveTextContent('Your answer: "nope". Expected: "rolling out".');
  expect(feedback).not.toHaveTextContent("No attempts yet. Start Practice to begin.");
});
