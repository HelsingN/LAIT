// @vitest-environment jsdom
import "@testing-library/jest-dom/vitest";
import { cleanup, render, screen, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { afterEach, expect, it, vi } from "vitest";
import { MemoryRouter, Route, Routes } from "react-router";

import { LessonWorkspacePage } from "./LessonWorkspacePage.tsx";

const lessonId = "lesson-1";
const sourceText = "I was responsible for rolling out the migration.";

const lesson = {
  id: lessonId,
  title: "Rolling out",
  source: sourceText,
  created_at: "2026-10-01T00:00:00+00:00",
};

type UnitRecord = {
  id: string;
  lesson_id: string;
  start: number;
  end: number;
  text: string;
  status: string;
  created_at: string;
  removed_at: string | null;
};

const rollingOut: UnitRecord = {
  id: "unit-1",
  lesson_id: lessonId,
  start: 23,
  end: 34,
  text: "rolling out",
  status: "accepted",
  created_at: "2026-10-01T00:00:00+00:00",
  removed_at: null,
};

const migration: UnitRecord = {
  id: "unit-2",
  lesson_id: lessonId,
  start: 35,
  end: 48,
  text: "the migration",
  status: "accepted",
  created_at: "2026-10-01T00:00:00+00:00",
  removed_at: null,
};

type Segment = { kind: string; text: string };

type PracticeItem = {
  mode: string;
  learning_unit_id: string;
  exercise_type: string;
  position: number;
  start: number;
  end: number;
  target_text: string;
  sentence: string;
  segments: Segment[];
  chip_unit_ids: string[];
};

type FetchCall = { url: string; method: string; body: unknown };

const blankedSentence: Segment[] = [
  { kind: "text", text: "I was responsible for " },
  { kind: "blank", text: "______" },
  { kind: "text", text: "the migration." },
];

function typedItem(exerciseType: string): PracticeItem {
  return {
    mode: "typed",
    learning_unit_id: "unit-1",
    exercise_type: exerciseType,
    position: 0,
    start: 23,
    end: 34,
    target_text: "rolling out",
    sentence: "I was responsible for ______ the migration.",
    segments: blankedSentence,
    chip_unit_ids: ["unit-1"],
  };
}

function dragItem(): PracticeItem {
  return {
    mode: "drag",
    learning_unit_id: "unit-1",
    exercise_type: "gap-fill",
    position: 0,
    start: 23,
    end: 34,
    target_text: "rolling out",
    sentence: "I was responsible for ______ the migration.",
    segments: blankedSentence,
    chip_unit_ids: ["unit-1", "unit-2"],
  };
}

function practiceView(current: PracticeItem | null, sessionId = "session-1") {
  return {
    session_id: sessionId,
    lesson_id: lessonId,
    open: current !== null,
    cursor: current ? current.position : 1,
    current,
  };
}

function feedbackBody(overrides: Record<string, unknown> = {}) {
  return {
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
    span_start: 23,
    span_end: 34,
    unit_text: "rolling out",
    ...overrides,
  };
}

function jsonResponse(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json" },
  });
}

function deferred<T>() {
  let resolve!: (value: T) => void;
  const promise = new Promise<T>((res) => {
    resolve = res;
  });
  return { promise, resolve };
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

type Script = {
  units: UnitRecord[];
  exerciseType: string;
  startItem: PracticeItem;
  continueItem: PracticeItem | null;
  submit: (body: unknown) => Response | Promise<Response>;
  startOverItem?: PracticeItem;
};

function installFetch(script: Script): FetchCall[] {
  const calls: FetchCall[] = [];
  vi.stubGlobal(
    "fetch",
    vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      const method = (init?.method ?? "GET").toUpperCase();
      const body = init?.body ? (JSON.parse(String(init.body)) as unknown) : null;
      calls.push({ url, method, body });

      if (url.includes("/api/exercise-registry")) {
        return jsonResponse({
          exercises: [
            {
              exercise_type: script.exerciseType,
              visibility: "learner",
              module_id: "official.exercise.gap-fill",
            },
          ],
        });
      }
      if (url.includes("/learning-units") && method === "GET") {
        return jsonResponse({ learning_units: script.units });
      }
      if (url.includes("/exercises/generate") && method === "POST") {
        return jsonResponse({
          id: "gen-1",
          lesson_id: lessonId,
          status: "completed",
          accepted_unit_ids: script.units.map((unit) => unit.id),
          definition_count: script.units.length,
        });
      }
      if (url === "/api/practice-sessions" && method === "POST") {
        return jsonResponse(practiceView(script.startItem), 201);
      }
      if (url.includes(`/api/lessons/${lessonId}/attempts`) && method === "GET") {
        return jsonResponse({ attempts: [] });
      }
      if (url.includes("/practice-sessions/") && url.endsWith("/attempts") && method === "POST") {
        return script.submit(body);
      }
      if (url.endsWith("/finish") && method === "POST") {
        return jsonResponse({ ...practiceView(null), open: false });
      }
      if (url.endsWith("/start-over") && method === "POST") {
        return jsonResponse(practiceView(script.startOverItem ?? script.startItem, "session-2"));
      }
      if (/\/api\/practice-sessions\/[^/]+$/.test(url) && method === "GET") {
        return jsonResponse(practiceView(script.continueItem, "session-1"));
      }
      if (url.includes(`/api/lessons/${lessonId}`) && method === "GET") {
        return jsonResponse(lesson);
      }
      return new Response("missing", { status: 404 });
    }),
  );
  return calls;
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

it("submits one typed answer then continues inside the session", async () => {
  const user = userEvent.setup();
  const pendingSubmit = deferred<Response>();
  const calls = installFetch({
    units: [rollingOut],
    exerciseType: "gap-fill",
    startItem: typedItem("gap-fill"),
    continueItem: null,
    submit: () => pendingSubmit.promise,
  });
  renderWorkspace();
  await generateAndStart(user);

  expect(screen.queryByTestId("stage-column")).not.toBeInTheDocument();
  expect(screen.queryByTestId("proof-renderer")).not.toBeInTheDocument();
  expect(screen.getByText("______")).toBeInTheDocument();
  expect(screen.getByText("I was responsible for")).toBeInTheDocument();
  expect(screen.queryByTestId("chip-bank")).not.toBeInTheDocument();
  expect(
    screen.getByText("Learning units are locked while practice is open. Exit Practice to edit them."),
  ).toBeInTheDocument();

  const answer = screen.getByRole("textbox", { name: "Answer" });
  await user.type(answer, "nope");
  await user.click(screen.getByRole("button", { name: "Submit Answer" }));

  const checking = screen.getByRole("button", { name: "Checking…" });
  expect(checking).toBeDisabled();
  pendingSubmit.resolve(jsonResponse(feedbackBody()));

  const card = await screen.findByTestId("feedback-card");
  expect(card).toHaveTextContent("incorrect");
  expect(card).toHaveTextContent("nope");
  expect(card).toHaveTextContent("rolling out");
  expect(card).toHaveTextContent('Your answer: "nope". Expected: "rolling out".');
  expect(card).toHaveTextContent("missed");
  expect(card).not.toHaveTextContent("natural");
  expect(screen.queryByRole("button", { name: "Submit Answer" })).not.toBeInTheDocument();

  const submitCall = calls.find(
    (call) => call.method === "POST" && call.url.includes("/practice-sessions/") && call.url.endsWith("/attempts"),
  );
  expect(submitCall?.body).toMatchObject({ kind: "typed", text: "nope" });
  expect(submitCall?.body).not.toHaveProperty("category");

  await user.click(screen.getByRole("button", { name: "Continue" }));
  expect(screen.queryByTestId("feedback-card")).not.toBeInTheDocument();
  expect(screen.getByRole("button", { name: "Exit Practice" })).toBeInTheDocument();
  expect(screen.queryByTestId("stage-column")).not.toBeInTheDocument();
  expect(calls.some((call) => call.url.endsWith("/finish"))).toBe(false);
  expect(calls.some((call) => call.method === "GET" && /\/api\/practice-sessions\/session-1$/.test(call.url))).toBe(
    true,
  );
});

it("submits a drag chip by unit id and displays the server category", async () => {
  const user = userEvent.setup();
  const calls = installFetch({
    units: [rollingOut, migration],
    exerciseType: "gap-fill",
    startItem: dragItem(),
    continueItem: typedItem("gap-fill"),
    submit: () =>
      jsonResponse(
        feedbackBody({
          category: "correct",
          submitted: "the migration",
          explanation: 'Correct. The expected answer is "rolling out".',
          chunks_used: ["rolling out"],
          chunks_missed: [],
        }),
      ),
  });
  renderWorkspace();
  await generateAndStart(user);

  const bank = screen.getByTestId("chip-bank");
  await user.click(within(bank).getByRole("button", { name: "the migration" }));
  await user.click(screen.getByRole("button", { name: "Submit Answer" }));

  const card = await screen.findByTestId("feedback-card");
  expect(card).toHaveTextContent("correct");
  expect(card).not.toHaveTextContent("incorrect");
  const submitCall = calls.find(
    (call) => call.method === "POST" && call.url.includes("/practice-sessions/") && call.url.endsWith("/attempts"),
  );
  expect(submitCall?.body).toMatchObject({
    kind: "drag",
    text: "the migration",
    submitted_unit_id: "unit-2",
  });
  expect(submitCall?.body).not.toHaveProperty("category");
});

it("keeps the typed answer when submit fails", async () => {
  const user = userEvent.setup();
  installFetch({
    units: [rollingOut],
    exerciseType: "gap-fill",
    startItem: typedItem("gap-fill"),
    continueItem: null,
    submit: () => new Response("nope", { status: 500 }),
  });
  renderWorkspace();
  await generateAndStart(user);

  const answer = screen.getByRole("textbox", { name: "Answer" });
  await user.type(answer, "nope");
  await user.click(screen.getByRole("button", { name: "Submit Answer" }));

  expect(await screen.findByRole("alert")).toHaveTextContent("Could not submit. Try again.");
  expect(answer).toHaveValue("nope");
  expect(screen.queryByTestId("feedback-card")).not.toBeInTheDocument();
  expect(screen.getByRole("button", { name: "Exit Practice" })).toBeInTheDocument();
  expect(screen.queryByTestId("stage-column")).not.toBeInTheDocument();
});

it("exit practice calls finish and restores the workspace", async () => {
  const user = userEvent.setup();
  const calls = installFetch({
    units: [rollingOut],
    exerciseType: "gap-fill",
    startItem: typedItem("gap-fill"),
    continueItem: null,
    submit: () => jsonResponse(feedbackBody()),
  });
  renderWorkspace();
  await generateAndStart(user);
  await user.click(screen.getByRole("button", { name: "Exit Practice" }));

  expect(await screen.findByTestId("stage-column")).toBeInTheDocument();
  expect(screen.queryByRole("button", { name: "Exit Practice" })).not.toBeInTheDocument();
  expect(
    screen.queryByText("Learning units are locked while practice is open. Exit Practice to edit them."),
  ).not.toBeInTheDocument();
  expect(calls.filter((call) => call.url === "/api/practice-sessions/session-1/finish" && call.method === "POST")).toHaveLength(
    1,
  );
  expect(calls.some((call) => call.url === "/api/practice-sessions" && call.method === "POST")).toBe(true);
});

it("start over confirms then calls start_over only", async () => {
  const user = userEvent.setup();
  const calls = installFetch({
    units: [rollingOut],
    exerciseType: "gap-fill",
    startItem: typedItem("gap-fill"),
    continueItem: null,
    startOverItem: {
      ...typedItem("gap-fill"),
      sentence: "Started over ______.",
      segments: [
        { kind: "text", text: "Started over " },
        { kind: "blank", text: "______" },
        { kind: "text", text: "." },
      ],
    },
    submit: () => jsonResponse(feedbackBody()),
  });
  renderWorkspace();
  await generateAndStart(user);
  await user.click(screen.getByRole("button", { name: "Start Over" }));
  expect(
    screen.getByText(
      "Start over: Abandon this practice run and start a new session on the same units? Submitted answers stay saved.",
    ),
  ).toBeInTheDocument();
  expect(calls.some((call) => call.url.endsWith("/start-over"))).toBe(false);

  await user.click(within(screen.getByRole("alertdialog")).getByRole("button", { name: "Start Over" }));
  expect(await screen.findByText("Started over")).toBeInTheDocument();
  expect(screen.queryByTestId("stage-column")).not.toBeInTheDocument();
  expect(calls.filter((call) => call.url === "/api/practice-sessions" && call.method === "POST")).toHaveLength(1);
  expect(calls.filter((call) => call.url === "/api/practice-sessions/session-1/start-over")).toHaveLength(1);
  expect(calls.some((call) => call.url.endsWith("/finish"))).toBe(false);
});

it("renders server feedback as text and omits a null natural alternative", async () => {
  const user = userEvent.setup();
  installFetch({
    units: [rollingOut],
    exerciseType: "gap-fill",
    startItem: typedItem("gap-fill"),
    continueItem: null,
    submit: () =>
      jsonResponse(
        feedbackBody({
          category: "correct",
          submitted: "rolling out",
          explanation: 'Correct. The expected answer is "rolling out". <script>alert(1)</script>',
          chunks_used: ["rolling out"],
          chunks_missed: [],
          natural_alternative: null,
        }),
      ),
  });
  renderWorkspace();
  await generateAndStart(user);
  await user.type(screen.getByRole("textbox", { name: "Answer" }), "rolling out");
  await user.click(screen.getByRole("button", { name: "Submit Answer" }));

  const card = await screen.findByTestId("feedback-card");
  expect(card.querySelector("script")).toBeNull();
  expect(card).toHaveTextContent('<script>alert(1)</script>');
  expect(card).toHaveTextContent("used");
  expect(card).not.toHaveTextContent("null");
  expect(screen.getAllByTestId("feedback-card")).toHaveLength(1);
});
