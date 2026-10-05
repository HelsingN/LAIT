// @vitest-environment jsdom
import "@testing-library/jest-dom/vitest";
import { cleanup, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { readFileSync, readdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, describe, expect, it, vi } from "vitest";
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

const acceptedUnit: UnitRecord = {
  id: "unit-1",
  lesson_id: lessonId,
  start: 23,
  end: 34,
  text: "rolling out",
  status: "accepted",
  created_at: "2026-10-01T00:00:00+00:00",
  removed_at: null,
};

type FetchCall = { url: string; method: string; body: unknown };

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

function stageLabels(column: HTMLElement): string[] {
  return ["Source", "Learning Units", "Exercises", "Practice", "Feedback"].filter(
    (label) => column.textContent?.includes(label),
  );
}

afterEach(() => {
  cleanup();
  localStorage.clear();
  vi.unstubAllGlobals();
});

describe("Lesson workspace shell", () => {
  it("shell-has-no-outer-empty-loading-error", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(() => new Promise<Response>(() => {})),
    );
    renderWorkspace();

    const column = screen.getByTestId("stage-column");
    expect(stageLabels(column)).toEqual([
      "Source",
      "Learning Units",
      "Exercises",
      "Practice",
      "Feedback",
    ]);
    expect(column).toHaveTextContent("Loading…");
    expect(screen.queryByRole("heading", { name: "No lessons yet" })).not.toBeInTheDocument();
    expect(screen.getByRole("main").compareDocumentPosition(column) & Node.DOCUMENT_POSITION_CONTAINED_BY).toBeTruthy();
  });

  it("keeps the stage shell mounted when the lesson request fails", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn(async () => new Response("nope", { status: 500 })),
    );
    renderWorkspace();

    const column = await screen.findByTestId("stage-column");
    expect(stageLabels(column)).toEqual([
      "Source",
      "Learning Units",
      "Exercises",
      "Practice",
      "Feedback",
    ]);
    expect(
      await within(column).findByText(
        "Could not load this lesson. Return to the lesson list and open it again.",
      ),
    ).toBeInTheDocument();
    expect(within(column).getByRole("link", { name: "Lessons" })).toHaveAttribute("href", "/");
  });

  it("stage-column-scroll-fixed-labels", async () => {
    installFetch({ units: [] });
    renderWorkspace();

    const column = await screen.findByTestId("stage-column");
    expect(stageLabels(column)).toEqual([
      "Source",
      "Learning Units",
      "Exercises",
      "Practice",
      "Feedback",
    ]);
    const workspaceCss = readFileSync(join(testDirectory, "LessonWorkspacePage.module.css"), "utf8");
    const unitsCss = readFileSync(join(testDirectory, "stages", "LearningUnitsStage.module.css"), "utf8");
    expect(workspaceCss).toMatch(/height:\s*100dvh/);
    expect(workspaceCss).toMatch(/\.workspace\s*\{[^}]*overflow:\s*hidden/s);
    expect(workspaceCss).toMatch(/@media\s*\(\s*min-width:\s*960px\s*\)/);
    expect(workspaceCss).toMatch(/grid-template-columns:\s*minmax\(0,\s*1fr\)\s+320px/);
    expect(workspaceCss).toMatch(/grid-template-rows:\s*minmax\(88px,\s*1fr\)\s+minmax\(232px,\s*1fr\)/);
    expect(workspaceCss).toMatch(/grid-template-rows:\s*minmax\(188px,\s*1fr\)/);
    expect(workspaceCss).toMatch(/\.prepSlot\s*\{[^}]*flex:\s*1\s+1\s+0/s);
    expect(workspaceCss).toMatch(/\.prepSlot\s*\{[^}]*min-height:\s*332px/s);
    expect(workspaceCss).toMatch(/max-height:\s*calc\(100dvh - 188px - 102px\)/);
    expect(workspaceCss).toMatch(/max-height:\s*calc\(100dvh - 332px - 102px\)/);
    expect(workspaceCss).toMatch(/min-height:\s*694px/);
    expect(workspaceCss).toMatch(/max-height:\s*837px/);
    expect(workspaceCss).toMatch(/\.actions > \.feedbackStage\s*\{[^}]*flex:\s*1\s+1\s+0/s);
    expect(workspaceCss).toMatch(/\.actions:has\(> \.feedbackStage\)\s*\{[^}]*height:\s*calc\(100dvh - 188px - 102px\)/s);
    expect(workspaceCss).toMatch(/\.actions > \.allowShrink\s*\{[^}]*flex:\s*0\s+1\s+auto/s);
    expect(workspaceCss).toMatch(/grid-template-rows:\s*auto\s+minmax\(0,\s*1fr\)/);
    expect(workspaceCss).toMatch(/\.feedbackCover\s*\{[^}]*position:\s*absolute/s);
    expect(workspaceCss).toMatch(/\.header\s*\{[^}]*flex:\s*0\s+0\s+auto/s);
    expect(workspaceCss).not.toMatch(/52vh/);
    expect(workspaceCss).not.toMatch(/min-height:\s*8rem/);
    expect(workspaceCss).not.toMatch(/minmax\(min-content/);
    expect(workspaceCss).not.toMatch(/32dvh/);
    expect(unitsCss).toMatch(/\.list\s*\{[^}]*min-height:\s*0/s);
    expect(column.className).not.toBe("");
  });

  it("source-panel-body-scrolls", async () => {
    installFetch({ units: [], source: "hello <script>alert(1)</script>" });
    renderWorkspace();

    await screen.findByRole("heading", { name: "Rolling out" });
    const sourceBody = await screen.findByTestId("source-body");
    const sourceCss = readFileSync(join(testDirectory, "stages", "SourceStage.module.css"), "utf8");
    expect(sourceCss).toMatch(/\.sourceBody\s*\{[^}]*overflow-y:\s*auto/s);
    expect(sourceCss).toMatch(/\.sourceBody\s*\{[^}]*min-height:\s*0/s);
    expect(sourceCss).toMatch(/overflow-wrap:\s*anywhere/);
    expect(sourceBody.querySelector("script")).toBeNull();
    expect(sourceBody).toHaveTextContent("hello <script>alert(1)</script>");
  });

  it("shows learner exercise types from list_visible_for and never describe", async () => {
    const calls = installFetch({ units: [] });
    renderWorkspace();
    await userEvent.setup().click(
      await screen.findByRole("button", { name: "Exercises", expanded: false }),
    );

    expect(await screen.findByText("learner-type-from-registry")).toBeInTheDocument();
    expect(screen.queryByText("official.exercise.gap-fill")).not.toBeInTheDocument();
    expect(calls.some((call) => call.url.includes("/api/module-registry"))).toBe(false);
    expect(
      calls.some(
        (call) =>
          call.url.includes("/api/exercise-registry") && call.url.includes("visibility=learner"),
      ),
    ).toBe(true);
  });

  it("shows Generating… then the no-accepted failure copy", async () => {
    const user = userEvent.setup();
    const generate = deferred<Response>();
    installFetch({ units: [], generate });
    renderWorkspace();

    await screen.findByRole("heading", { name: "Rolling out" });
    await user.click(screen.getByRole("button", { name: "Exercises", expanded: false }));
    await user.click(within(screen.getByRole("region", { name: "Exercises" })).getByRole("button", { name: "Generate Exercises" }));

    expect(screen.getByRole("button", { name: "Generating…" })).toBeDisabled();
    generate.resolve(
      jsonResponse({
        id: "gen-failed",
        lesson_id: lessonId,
        status: "failed",
        accepted_unit_ids: [],
        definition_count: 0,
      }),
    );
    expect(
      await screen.findByText(
        "No accepted units to practice. Accept at least one draft unit, then generate again.",
      ),
    ).toBeInTheDocument();
    expect(
      within(screen.getByRole("region", { name: "Exercises" })).getByRole("button", {
        name: "Generate Exercises",
      }),
    ).toBeEnabled();
  });

  it("shows the generic generation failure when accepted units exist", async () => {
    const user = userEvent.setup();
    installFetch({
      units: [acceptedUnit],
      generateResult: jsonResponse({
        id: "gen-failed",
        lesson_id: lessonId,
        status: "failed",
        accepted_unit_ids: [],
        definition_count: 0,
      }),
    });
    renderWorkspace();
    await screen.findByRole("heading", { name: "Rolling out" });
    await user.click(screen.getByRole("button", { name: "Exercises", expanded: false }));
    await user.click(
      within(screen.getByRole("region", { name: "Exercises" })).getByRole("button", {
        name: "Generate Exercises",
      }),
    );
    expect(
      await screen.findByText(
        "Exercise generation failed. Check your accepted units and try Generate Exercises again.",
      ),
    ).toBeInTheDocument();
    expect(
      screen.queryByText(
        "No accepted units to practice. Accept at least one draft unit, then generate again.",
      ),
    ).not.toBeInTheDocument();
  });

  it("enables Start Practice only for the generated accepted set", async () => {
    const user = userEvent.setup();
    const generate = deferred<Response>();
    installFetch({ units: [acceptedUnit], generate });
    renderWorkspace();

    await screen.findByRole("heading", { name: "Rolling out" });
    expect(screen.getByRole("button", { name: "Practice" })).toBeDisabled();
    expect(screen.getByRole("button", { name: "Feedback" })).toBeDisabled();

    await user.click(screen.getByRole("button", { name: "Exercises", expanded: false }));
    await user.click(
      within(screen.getByRole("region", { name: "Exercises" })).getByRole("button", {
        name: "Generate Exercises",
      }),
    );
    expect(screen.getByRole("button", { name: "Generating…" })).toBeDisabled();
    generate.resolve(
      jsonResponse({
        id: "gen-1",
        lesson_id: lessonId,
        status: "completed",
        accepted_unit_ids: ["unit-1"],
        definition_count: 1,
      }),
    );

    expect(await screen.findByText("Exercises are ready.")).toBeInTheDocument();
    expect(screen.queryByText("completed")).not.toBeInTheDocument();
    expect(
      within(screen.getByRole("region", { name: "Exercises" })).queryByRole("button", {
        name: "Generate Exercises",
      }),
    ).not.toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Practice", expanded: true })).toBeInTheDocument();
    const start = screen.getByRole("button", { name: "Start Practice" });
    expect(start).toBeEnabled();
    expect(screen.queryByRole("button", { name: "Submit Answer" })).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Exit Practice" })).not.toBeInTheDocument();

    const sourceBody = await screen.findByTestId("source-body");
    const textNode = sourceBody.firstChild;
    if (!textNode) {
      throw new Error("source text node missing");
    }
    const range = document.createRange();
    range.setStart(textNode, 0);
    range.setEnd(textNode, 4);
    const selection = window.getSelection();
    selection?.removeAllRanges();
    selection?.addRange(range);
    fireEvent.mouseUp(sourceBody);
    await user.click(screen.getByRole("button", { name: "Add Learning Unit" }));

    await waitFor(() => {
      expect(screen.getByRole("button", { name: "Accept" })).toBeInTheDocument();
    });
    expect(screen.getAllByText("draft span")).toHaveLength(1);
    expect(screen.queryByText("draft")).not.toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Start Practice" })).toBeEnabled();

    await user.click(screen.getByRole("button", { name: "Accept" }));
    await waitFor(() => {
      expect(screen.getByRole("button", { name: "Start Practice" })).toBeDisabled();
    });
    expect(screen.queryByText("Exercises are ready.")).not.toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Generate Exercises" })).toBeEnabled();
  });

  it("remembers stage expansion per lesson id", async () => {
    const user = userEvent.setup();
    installFetch({ units: [] });
    const view = renderWorkspace();
    await screen.findByRole("heading", { name: "Rolling out" });

    const sourceHeader = screen.getByRole("button", { name: "Source", expanded: true });
    expect(sourceHeader.querySelector("[aria-hidden='true']")).toHaveTextContent("▾");
    expect(screen.getByRole("button", { name: "Learning Units", expanded: true })).toBeInTheDocument();
    await user.click(sourceHeader);
    expect(screen.getByRole("button", { name: "Source", expanded: false }).querySelector("[aria-hidden='true']")).toHaveTextContent(
      "▸",
    );
    await user.click(screen.getByRole("button", { name: "Learning Units", expanded: true }));

    const stored = JSON.parse(localStorage.getItem(`lait.lesson-stages.${lessonId}`) ?? "{}") as {
      source: boolean;
      "learning-units": boolean;
    };
    expect(stored.source).toBe(false);
    expect(stored["learning-units"]).toBe(false);

    view.unmount();
    renderWorkspace();
    expect(await screen.findByRole("button", { name: "Source", expanded: false })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Learning Units", expanded: false })).toBeInTheDocument();
  });

  it("renders persisted source on a direct reopen and can add a unit from it", async () => {
    const user = userEvent.setup();
    const persisted = "Persisted source survives a fresh load.";
    const calls = installFetch({ units: [], source: persisted });
    renderWorkspace();

    const sourceBody = await screen.findByTestId("source-body");
    expect(sourceBody).toHaveTextContent(persisted);
    expect(screen.getByRole("button", { name: "Source", expanded: true })).toBeInTheDocument();

    const textNode = sourceBody.firstChild;
    if (!textNode) {
      throw new Error("source text node missing");
    }
    const range = document.createRange();
    range.setStart(textNode, 0);
    range.setEnd(textNode, "Persisted".length);
    const selection = window.getSelection();
    selection?.removeAllRanges();
    selection?.addRange(range);
    fireEvent.mouseUp(sourceBody);
    await user.click(screen.getByRole("button", { name: "Add Learning Unit" }));

    await waitFor(() => {
      expect(screen.getByText("draft span")).toBeInTheDocument();
    });
    expect(screen.getAllByText("draft span")).toHaveLength(1);
    expect(calls).toContainEqual(
      expect.objectContaining({
        url: `/api/lessons/${lessonId}/learning-units`,
        method: "POST",
        body: { start: 0, end: "Persisted".length },
      }),
    );
  });

  it("isPracticeOpen locks while a stored session is pending and then follows session.open", async () => {
    const stageState = await import("./stageState.ts");
    expect("isPracticeOpen" in stageState && "loadOpenPracticeSessionId" in stageState).toBe(true);
    const isPracticeOpen = (
      stageState as {
        isPracticeOpen?: (pendingStoredSession: boolean, sessionOpen: boolean) => boolean;
      }
    ).isPracticeOpen;
    expect(isPracticeOpen).toHaveLength(2);
    expect(isPracticeOpen?.(true, false)).toBe(true);
    expect(isPracticeOpen?.(false, true)).toBe(true);
    expect(isPracticeOpen?.(false, false)).toBe(false);
  });

  it("resumes a stored open session into Focus Practice after the frozen hint", async () => {
    const sessionId = "session-stored";
    localStorage.setItem(`lait.practice-session.${lessonId}`, sessionId);
    const practiceGet = deferred<Response>();
    const calls = installFetch({ units: [acceptedUnit], practiceGet });
    renderWorkspace();

    const column = await screen.findByTestId("stage-column");
    expect(screen.queryByRole("button", { name: "Exit Practice" })).not.toBeInTheDocument();
    expect(
      await within(column).findByText(
        "Learning units are locked while practice is open. Exit Practice to edit them.",
      ),
    ).toBeInTheDocument();
    expect(
      calls.some(
        (call) => call.method === "GET" && call.url === `/api/practice-sessions/${sessionId}`,
      ),
    ).toBe(true);
    expect(calls.some((call) => call.url === "/api/practice-sessions" && call.method === "POST")).toBe(
      false,
    );
    expect(calls.some((call) => call.url.includes("/finish"))).toBe(false);

    practiceGet.resolve(
      jsonResponse({
        session_id: sessionId,
        lesson_id: lessonId,
        open: true,
        cursor: 0,
        current: {
          mode: "typed",
          learning_unit_id: "unit-1",
          exercise_type: "not-mounted",
          position: 0,
          start: 0,
          end: 1,
          target_text: "x",
          sentence: "x",
          segments: [],
          chip_unit_ids: [],
        },
      }),
    );

    expect(await screen.findByRole("button", { name: "Exit Practice" })).toBeInTheDocument();
    expect(screen.queryByTestId("stage-column")).not.toBeInTheDocument();
  });

  it("clears a stored session that is not open and leaves the workspace unlocked", async () => {
    const sessionId = "session-closed";
    localStorage.setItem(`lait.practice-session.${lessonId}`, sessionId);
    const practiceGet = deferred<Response>();
    installFetch({ units: [acceptedUnit], practiceGet });
    renderWorkspace();

    const column = await screen.findByTestId("stage-column");
    practiceGet.resolve(
      jsonResponse({
        session_id: sessionId,
        lesson_id: lessonId,
        open: false,
        cursor: 0,
        current: null,
      }),
    );

    await waitFor(() => {
      expect(localStorage.getItem(`lait.practice-session.${lessonId}`)).toBeNull();
    });
    expect(
      screen.queryByText(
        "Learning units are locked while practice is open. Exit Practice to edit them.",
      ),
    ).not.toBeInTheDocument();
    expect(column).toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Exit Practice" })).not.toBeInTheDocument();
  });

  it("disables Start Practice until the first start request settles", async () => {
    const user = userEvent.setup();
    const start = deferred<Response>();
    const calls = installFetch({
      units: [acceptedUnit],
      generateResult: jsonResponse({
        id: "gen-1",
        lesson_id: lessonId,
        status: "completed",
        accepted_unit_ids: ["unit-1"],
        definition_count: 1,
      }),
      start,
    });
    renderWorkspace();

    await screen.findByRole("heading", { name: "Rolling out" });
    await user.click(screen.getByRole("button", { name: "Exercises", expanded: false }));
    await user.click(
      within(screen.getByRole("region", { name: "Exercises" })).getByRole("button", {
        name: "Generate Exercises",
      }),
    );
    const startButton = await screen.findByRole("button", { name: "Start Practice" });
    expect(startButton).toBeEnabled();
    await user.click(startButton);
    expect(startButton).toBeDisabled();
    await user.click(startButton);
    expect(
      calls.filter((call) => call.url === "/api/practice-sessions" && call.method === "POST"),
    ).toHaveLength(1);

    start.resolve(
      jsonResponse({
        session_id: "session-1",
        lesson_id: lessonId,
        open: true,
        cursor: 0,
        current: null,
      }),
    );
    expect(await screen.findByRole("button", { name: "Exit Practice" })).toBeInTheDocument();
    expect(screen.queryByTestId("stage-column")).not.toBeInTheDocument();
  });

  it("enables Start Practice again after the start request rejects", async () => {
    const user = userEvent.setup();
    const start = deferred<Response>();
    const calls = installFetch({
      units: [acceptedUnit],
      generateResult: jsonResponse({
        id: "gen-1",
        lesson_id: lessonId,
        status: "completed",
        accepted_unit_ids: ["unit-1"],
        definition_count: 1,
      }),
      start,
    });
    renderWorkspace();

    await screen.findByRole("heading", { name: "Rolling out" });
    await user.click(screen.getByRole("button", { name: "Exercises", expanded: false }));
    await user.click(
      within(screen.getByRole("region", { name: "Exercises" })).getByRole("button", {
        name: "Generate Exercises",
      }),
    );
    const startButton = await screen.findByRole("button", { name: "Start Practice" });
    await user.click(startButton);
    expect(startButton).toBeDisabled();
    start.resolve(new Response("nope", { status: 500 }));
    expect(await screen.findByRole("alert")).toHaveTextContent("Could not start practice. Try again.");
    expect(screen.getByRole("button", { name: "Start Practice" })).toBeEnabled();
    expect(
      calls.filter((call) => call.url === "/api/practice-sessions" && call.method === "POST"),
    ).toHaveLength(1);
  });

  it("does not reference module_registry.describe in lesson feature source", () => {
    const root = testDirectory;
    const files = walk(root).filter((file) => /\.(ts|tsx)$/.test(file) && !file.endsWith(".test.tsx"));
    const source = files.map((file) => readFileSync(file, "utf8")).join("\n");
    expect(source).not.toContain("/api/module-registry");
    expect(source).not.toContain("module_registry.describe");
    expect(source).not.toContain("official.exercise.gap-fill");
  });

  it("reloads a matching generation and saved attempts without generate", async () => {
    const calls = installFetch({
      units: [acceptedUnit],
      latest: {
        restorable: true,
        generation_id: "gen-restored",
        accepted_unit_ids: ["unit-1"],
      },
      attemptList: [historyAttempt("session-saved", "completed", "attempt-saved")],
    });
    renderWorkspace();

    expect(await screen.findByRole("button", { name: "Start Practice" })).toBeEnabled();
    await userEvent.setup().click(screen.getByRole("button", { name: "Exercises", expanded: false }));
    expect(screen.getByText("Exercises are ready.")).toBeInTheDocument();
    expect(
      within(screen.getByRole("region", { name: "Exercises" })).queryByRole("button", {
        name: "Generate Exercises",
      }),
    ).not.toBeInTheDocument();
    expect(
      within(screen.getByRole("region", { name: "Exercises" })).queryByText("completed"),
    ).not.toBeInTheDocument();
    const feedback = await screen.findByRole("region", { name: "Feedback" });
    expect(screen.getByTestId("prep-slot").contains(feedback)).toBe(false);
    expect(feedback).toHaveTextContent("session-saved");
    expect(feedback).toHaveTextContent("correct");
    await waitFor(() => {
      expect(calls.some((call) => call.url.includes("/exercises/latest") && call.method === "GET")).toBe(
        true,
      );
    });
    expect(calls.some((call) => call.method === "POST" && call.url.includes("/exercises/generate"))).toBe(
      false,
    );
  });

  it("keeps Start Practice disabled when the accepted set is not restorable", async () => {
    const calls = installFetch({
      units: [acceptedUnit],
      latest: {
        restorable: false,
        generation_id: "stale-gen",
        accepted_unit_ids: ["other-unit"],
      },
    });
    renderWorkspace();

    await screen.findByRole("heading", { name: "Rolling out" });
    await waitFor(() => {
      expect(calls.some((call) => call.url.includes("/exercises/latest"))).toBe(true);
    });
    expect(screen.getByRole("button", { name: "Practice" })).toBeDisabled();
    expect(screen.queryByRole("button", { name: "Start Practice" })).not.toBeInTheDocument();
    expect(screen.queryByText("stale-gen")).not.toBeInTheDocument();
    expect(screen.queryByText("completed")).not.toBeInTheDocument();
    expect(calls.some((call) => call.method === "POST" && call.url.includes("/exercises/generate"))).toBe(
      false,
    );
  });

  it("closes an exhausted session on Continue and keeps the other session under Earlier passes", async () => {
    const user = userEvent.setup();
    const calls = installFetch({
      units: [acceptedUnit],
      latest: {
        restorable: true,
        generation_id: "gen-1",
        accepted_unit_ids: ["unit-1"],
      },
      startResult: jsonResponse({
        session_id: "session-now",
        lesson_id: lessonId,
        open: true,
        cursor: 0,
        current: typedItem,
      }),
      practiceView: jsonResponse({
        session_id: "session-now",
        lesson_id: lessonId,
        open: true,
        cursor: 8,
        current: null,
      }),
      attemptList: [
        historyAttempt("session-old", "completed", "attempt-old"),
        historyAttempt("session-now", "completed", "attempt-now"),
      ],
    });
    renderWorkspace();

    await user.click(await screen.findByRole("button", { name: "Start Practice" }));
    await user.type(await screen.findByRole("textbox", { name: "Answer" }), "rolling out");
    await user.click(screen.getByRole("button", { name: "Submit Answer" }));
    await user.click(await screen.findByRole("button", { name: "Continue" }));

    const feedback = await screen.findByRole("region", { name: "Feedback" });
    const current = within(feedback).getByRole("region", { name: "Current pass" });
    expect(current).toHaveTextContent("session-now");
    expect(current).not.toHaveTextContent("session-old");
    expect(within(feedback).getByRole("region", { name: "Earlier passes" })).toHaveTextContent(
      "session-old",
    );
    expect(screen.queryByRole("button", { name: "Exit Practice" })).not.toBeInTheDocument();
    expect(calls.some((call) => call.method === "POST" && call.url.includes("/finish"))).toBe(true);
    expect(calls.some((call) => call.method === "POST" && call.url.includes("/exercises/generate"))).toBe(
      false,
    );
  });

  it("labels an early Exit as left early and keeps the older session separate", async () => {
    const user = userEvent.setup();
    installFetch({
      units: [acceptedUnit],
      latest: {
        restorable: true,
        generation_id: "gen-1",
        accepted_unit_ids: ["unit-1"],
      },
      startResult: jsonResponse({
        session_id: "session-now",
        lesson_id: lessonId,
        open: true,
        cursor: 0,
        current: typedItem,
      }),
      attemptList: [
        historyAttempt("session-old", "completed", "attempt-old"),
        historyAttempt("session-now", "exited", "attempt-now"),
      ],
    });
    renderWorkspace();

    await user.click(await screen.findByRole("button", { name: "Start Practice" }));
    await user.click(await screen.findByRole("button", { name: "Exit Practice" }));

    const feedback = await screen.findByRole("region", { name: "Feedback" });
    const current = within(feedback).getByRole("region", { name: "Current pass" });
    expect(current).toHaveTextContent("left early");
    expect(current).toHaveTextContent("session-now");
    expect(current).not.toHaveTextContent("completed");
    expect(within(feedback).getByRole("region", { name: "Earlier passes" })).toHaveTextContent(
      "session-old",
    );
  });

  it("finishes a stored open session with no current item instead of mounting Focus", async () => {
    const sessionId = "session-empty";
    localStorage.setItem(`lait.practice-session.${lessonId}`, sessionId);
    const calls = installFetch({
      units: [acceptedUnit],
      practiceView: jsonResponse({
        session_id: sessionId,
        lesson_id: lessonId,
        open: true,
        cursor: 8,
        current: null,
      }),
      attemptList: [historyAttempt(sessionId, "completed", "attempt-empty")],
    });
    renderWorkspace();

    const feedback = await screen.findByRole("region", { name: "Feedback" });
    const current = within(feedback).getByRole("region", { name: "Current pass" });
    expect(current).toHaveTextContent(sessionId);
    expect(screen.queryByRole("button", { name: "Exit Practice" })).not.toBeInTheDocument();
    expect(localStorage.getItem(`lait.practice-session.${lessonId}`)).toBeNull();
    expect(calls.some((call) => call.method === "POST" && call.url.includes("/finish"))).toBe(true);
    expect(calls.some((call) => call.method === "POST" && call.url.includes("/exercises/generate"))).toBe(
      false,
    );
    expect(calls.some((call) => call.url === "/api/practice-sessions" && call.method === "POST")).toBe(
      false,
    );
  });

  it("clears a stored id when finish returns 404 and still shows the listed pass", async () => {
    const sessionId = "session-closed-already";
    localStorage.setItem(`lait.practice-session.${lessonId}`, sessionId);
    const calls = installFetch({
      units: [acceptedUnit],
      practiceView: jsonResponse({
        session_id: sessionId,
        lesson_id: lessonId,
        open: true,
        cursor: 8,
        current: null,
      }),
      finishStatus: 404,
      attemptList: [historyAttempt(sessionId, "completed", "attempt-closed")],
    });
    renderWorkspace();

    const feedback = await screen.findByRole("region", { name: "Feedback" });
    expect(within(feedback).getByRole("region", { name: "Current pass" })).toHaveTextContent(sessionId);
    await waitFor(() => {
      expect(localStorage.getItem(`lait.practice-session.${lessonId}`)).toBeNull();
    });
    expect(screen.queryByRole("button", { name: "Exit Practice" })).not.toBeInTheDocument();
    const unitsPanel = screen.getByRole("region", { name: "Learning Units" });
    await userEvent.setup().click(within(unitsPanel).getByRole("button", { name: "rolling out" }));
    expect(within(unitsPanel).getByRole("button", { name: "Remove rolling out" })).toBeEnabled();
    expect(calls.some((call) => call.method === "POST" && call.url.includes("/exercises/generate"))).toBe(
      false,
    );
    expect(calls.some((call) => call.url === "/api/practice-sessions" && call.method === "POST")).toBe(
      false,
    );
  });

  it("keeps the stored id and skips the summary when finish returns 500", async () => {
    const sessionId = "session-stuck";
    localStorage.setItem(`lait.practice-session.${lessonId}`, sessionId);
    const calls = installFetch({
      units: [acceptedUnit],
      practiceView: jsonResponse({
        session_id: sessionId,
        lesson_id: lessonId,
        open: true,
        cursor: 8,
        current: null,
      }),
      finishStatuses: [500, 200],
    });
    renderWorkspace();

    expect(await screen.findByRole("alert")).toHaveTextContent(
      "Could not finish this practice. Try again.",
    );
    expect(localStorage.getItem(`lait.practice-session.${lessonId}`)).toBe(sessionId);
    expect(screen.queryByRole("region", { name: "Current pass" })).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Exit Practice" })).not.toBeInTheDocument();
    const unitsPanel = screen.getByRole("region", { name: "Learning Units" });
    await userEvent.setup().click(await within(unitsPanel).findByRole("button", { name: "rolling out" }));
    expect(within(unitsPanel).getByRole("button", { name: "Remove rolling out" })).toBeDisabled();
    expect(
      screen.getByText("Learning units are locked while practice is open. Exit Practice to edit them."),
    ).toBeInTheDocument();

    await userEvent.setup().click(screen.getByRole("button", { name: "Try again" }));
    await waitFor(() => {
      expect(localStorage.getItem(`lait.practice-session.${lessonId}`)).toBeNull();
    });
    expect(screen.queryByText("Could not finish this practice. Try again.")).not.toBeInTheDocument();
    expect(screen.queryByRole("region", { name: "Current pass" })).not.toBeInTheDocument();
    expect(calls.filter((call) => call.method === "POST" && call.url.includes("/finish"))).toHaveLength(2);
  });

  it("retries only the attempt list after finish already succeeded", async () => {
    const sessionId = "session-history";
    localStorage.setItem(`lait.practice-session.${lessonId}`, sessionId);
    const calls = installFetch({
      units: [acceptedUnit],
      practiceView: jsonResponse({
        session_id: sessionId,
        lesson_id: lessonId,
        open: true,
        cursor: 8,
        current: null,
      }),
      attemptListFailures: 2,
      attemptList: [historyAttempt(sessionId, "completed", "attempt-history")],
    });
    renderWorkspace();

    expect(await screen.findByRole("alert")).toHaveTextContent(
      "Could not load practice history. Try again.",
    );
    expect(calls.filter((call) => call.method === "POST" && call.url.includes("/finish"))).toHaveLength(1);

    await userEvent.setup().click(screen.getByRole("button", { name: "Try again" }));
    expect(await screen.findByRole("region", { name: "Current pass" })).toHaveTextContent(sessionId);
    expect(calls.filter((call) => call.method === "POST" && call.url.includes("/finish"))).toHaveLength(1);
  });

  it("covers preparation with open Feedback on a short window and keeps scroll", async () => {
    const media = {
      matches: true,
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
    };
    vi.stubGlobal("matchMedia", () => media);
    installFetch({
      units: [acceptedUnit],
      latest: { restorable: false },
      attemptList: [historyAttempt("session-saved", "completed", "attempt-saved")],
    });
    renderWorkspace();

    const feedback = await screen.findByRole("region", { name: "Feedback" });
    expect(screen.getByTestId("prep-slot").contains(feedback)).toBe(true);
    expect(feedback.className).toMatch(/feedbackCover/);
    expect(screen.getByText(sourceText)).toBeInTheDocument();

    const source = screen.getByTestId("source-body");
    let sourceTop = 0;
    Object.defineProperty(source, "scrollTop", {
      configurable: true,
      get: () => sourceTop,
      set: (value: number) => {
        sourceTop = value;
      },
    });
    source.scrollTop = 40;
    const units = document.getElementById("units");
    expect(units).not.toBeNull();
    let unitsTop = 0;
    Object.defineProperty(units, "scrollTop", {
      configurable: true,
      get: () => unitsTop,
      set: (value: number) => {
        unitsTop = value;
      },
    });
    units!.scrollTop = 24;

    await userEvent.setup().click(screen.getByRole("button", { name: "Feedback", expanded: true }));
    expect(screen.queryByRole("region", { name: "Feedback" })).not.toBeInTheDocument();
    expect(screen.getByTestId("source-body")).toBe(source);
    expect(screen.getByTestId("source-body").scrollTop).toBe(40);
    expect(document.getElementById("units")).toBe(units);
    expect(document.getElementById("units")?.scrollTop).toBe(24);
    vi.unstubAllGlobals();
  });
});

const testDirectory = dirname(fileURLToPath(import.meta.url));

function walk(directory: string): string[] {
  const entries = readdirSync(directory, { withFileTypes: true });
  return entries.flatMap((entry) => {
    const path = join(directory, entry.name);
    return entry.isDirectory() ? walk(path) : [path];
  });
}

function historyAttempt(sessionId: string, disposition: string, attemptId: string) {
  return {
    attempt_id: attemptId,
    session_id: sessionId,
    session_disposition: disposition,
    mode: "typed",
    category: "correct",
    submitted: "rolling out",
    expected: "rolling out",
    explanation: "matched",
    unit_text: "rolling out",
    span_start: 23,
    span_end: 34,
    created_at: "2026-10-02T00:00:00+00:00",
  };
}

const typedItem = {
  mode: "typed",
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
  chip_unit_ids: ["unit-1"],
};

const submittedAttempt = {
  attempt_id: "attempt-submitted",
  session_open: true,
  cursor: 1,
  category: "correct",
  submitted: "rolling out",
  expected: "rolling out",
  explanation: "matched",
  chunks_used: [] as string[],
  chunks_missed: [] as string[],
  natural_alternative: null,
  learning_unit_id: "unit-1",
  span_start: 23,
  span_end: 34,
  unit_text: "rolling out",
};

function installFetch(options: {
  units: UnitRecord[];
  source?: string;
  generate?: ReturnType<typeof deferred<Response>>;
  generateResult?: Response;
  practiceGet?: ReturnType<typeof deferred<Response>>;
  practiceView?: Response;
  start?: ReturnType<typeof deferred<Response>>;
  startResult?: Response;
  latest?: unknown;
  attemptList?: unknown[];
  attemptListFailures?: number;
  finishStatus?: number;
  finishStatuses?: number[];
}): FetchCall[] {
  const calls: FetchCall[] = [];
  let units = options.units.map((unit) => ({ ...unit }));
  let attemptListFailuresLeft = options.attemptListFailures ?? 0;
  let finishStatusIndex = 0;
  const lessonBody = { ...lesson, source: options.source ?? lesson.source };
  vi.stubGlobal(
    "fetch",
    vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      const method = (init?.method ?? "GET").toUpperCase();
      const body = init?.body ? (JSON.parse(String(init.body)) as unknown) : null;
      calls.push({ url, method, body });

      if (url.includes("/api/module-registry")) {
        return jsonResponse({ modules: [] }, 500);
      }
      if (url.includes("/api/exercise-registry")) {
        return jsonResponse({
          exercises: [
            {
              exercise_type: "learner-type-from-registry",
              visibility: "learner",
              module_id: "official.exercise.gap-fill",
            },
            {
              exercise_type: "gap-fill",
              visibility: "learner",
              module_id: "learner.gap-fill",
            },
          ],
        });
      }
      if (url.includes("/learning-units") && url.includes("/accept") && method === "POST") {
        units = units.map((unit) => (unit.status === "draft" ? { ...unit, status: "accepted" } : unit));
        const accepted = units.find((unit) => unit.id === "unit-draft");
        return jsonResponse(accepted);
      }
      if (url.endsWith("/learning-units") && method === "POST") {
        const span = body as { start: number; end: number };
        const created: UnitRecord = {
          id: "unit-draft",
          lesson_id: lessonId,
          start: span.start,
          end: span.end,
          text: "draft span",
          status: "draft",
          created_at: "2026-10-01T00:00:00+00:00",
          removed_at: null,
        };
        units = [...units, created];
        return jsonResponse(created, 201);
      }
      if (url.includes("/learning-units") && method === "GET") {
        return jsonResponse({ learning_units: units });
      }
      if (url.includes("/exercises/latest") && method === "GET") {
        return jsonResponse(
          options.latest ?? {
            restorable: false,
            generation_id: null,
            accepted_unit_ids: [],
          },
        );
      }
      if (url.includes("/exercises/generate") && method === "POST") {
        if (options.generate) {
          return options.generate.promise;
        }
        return options.generateResult ?? jsonResponse({ status: "failed" }, 500);
      }
      if (url.includes("/lessons/") && url.endsWith("/attempts") && method === "GET") {
        if (attemptListFailuresLeft > 0) {
          attemptListFailuresLeft -= 1;
          return new Response("nope", { status: 500 });
        }
        return jsonResponse({ attempts: options.attemptList ?? [] });
      }
      if (url === "/api/practice-sessions" && method === "POST") {
        if (options.start) {
          return options.start.promise;
        }
        return options.startResult ?? new Response("missing", { status: 404 });
      }
      if (url.includes("/practice-sessions/") && url.endsWith("/attempts") && method === "POST") {
        return jsonResponse(submittedAttempt);
      }
      if (url.includes("/finish") && method === "POST") {
        const queued = options.finishStatuses?.[finishStatusIndex];
        if (options.finishStatuses) {
          finishStatusIndex += 1;
        }
        const status = queued ?? options.finishStatus ?? 200;
        if (status !== 200) {
          return new Response("nope", { status });
        }
        return jsonResponse({
          session_id: "session-finished",
          lesson_id: lessonId,
          open: false,
          cursor: 8,
          current: null,
        });
      }
      if (/\/api\/practice-sessions\/[^/]+$/.test(url) && method === "GET") {
        if (options.practiceGet) {
          return options.practiceGet.promise;
        }
        return options.practiceView ?? new Response("missing", { status: 404 });
      }
      if (url.includes(`/api/lessons/${lessonId}`) && method === "GET") {
        return jsonResponse(lessonBody);
      }
      return new Response("missing", { status: 404 });
    }),
  );
  return calls;
}
