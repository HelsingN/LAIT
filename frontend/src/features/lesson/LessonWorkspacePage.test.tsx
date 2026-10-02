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
  return ["Source", "Learning Units", "Generate Exercises", "Practice", "Feedback"].filter(
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
      "Generate Exercises",
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
      "Generate Exercises",
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
      "Generate Exercises",
      "Practice",
      "Feedback",
    ]);
    const workspaceCss = readFileSync(join(testDirectory, "LessonWorkspacePage.module.css"), "utf8");
    expect(workspaceCss).toMatch(/\.stageColumn\s*\{[^}]*overflow-y:\s*auto/s);
    expect(column.className).not.toBe("");
  });

  it("source-panel-body-scrolls", async () => {
    const user = userEvent.setup();
    installFetch({ units: [], source: "hello <script>alert(1)</script>" });
    renderWorkspace();

    await screen.findByRole("heading", { name: "Rolling out" });
    await user.click(screen.getByRole("button", { name: "Source", expanded: false }));
    const sourceBody = await screen.findByTestId("source-body");
    const sourceCss = readFileSync(join(testDirectory, "stages", "SourceStage.module.css"), "utf8");
    expect(sourceCss).toMatch(/\.sourceBody\s*\{[^}]*overflow-y:\s*auto/s);
    expect(sourceCss).toMatch(/overflow-wrap:\s*anywhere/);
    expect(sourceBody.querySelector("script")).toBeNull();
    expect(sourceBody).toHaveTextContent("hello <script>alert(1)</script>");
  });

  it("shows learner exercise types from list_visible_for and never describe", async () => {
    const calls = installFetch({ units: [] });
    renderWorkspace();
    await userEvent.setup().click(
      await screen.findByRole("button", { name: "Generate Exercises", expanded: false }),
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
    await user.click(screen.getByRole("button", { name: "Generate Exercises", expanded: false }));
    await user.click(within(screen.getByRole("region", { name: "Generate Exercises" })).getByRole("button", { name: "Generate Exercises" }));

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
      within(screen.getByRole("region", { name: "Generate Exercises" })).getByRole("button", {
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
    await user.click(screen.getByRole("button", { name: "Generate Exercises", expanded: false }));
    await user.click(
      within(screen.getByRole("region", { name: "Generate Exercises" })).getByRole("button", {
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

    await user.click(screen.getByRole("button", { name: "Generate Exercises", expanded: false }));
    await user.click(
      within(screen.getByRole("region", { name: "Generate Exercises" })).getByRole("button", {
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

    expect(await screen.findByText("completed")).toBeInTheDocument();
    const start = screen.getByRole("button", { name: "Start Practice" });
    expect(start).toBeEnabled();
    expect(screen.queryByRole("button", { name: "Submit Answer" })).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Exit Practice" })).not.toBeInTheDocument();

    await user.click(screen.getByRole("button", { name: "Source", expanded: false }));
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
      expect(screen.getByText("draft")).toBeInTheDocument();
    });
    expect(screen.getByRole("button", { name: "Start Practice" })).toBeEnabled();

    await user.click(screen.getByRole("button", { name: "Accept" }));
    await waitFor(() => {
      expect(screen.getByRole("button", { name: "Start Practice" })).toBeDisabled();
    });
  });

  it("remembers stage expansion per lesson id", async () => {
    const user = userEvent.setup();
    installFetch({ units: [] });
    const view = renderWorkspace();
    await screen.findByRole("heading", { name: "Rolling out" });

    expect(screen.getByRole("button", { name: "Learning Units", expanded: true })).toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: "Source", expanded: false }));
    await user.click(screen.getByRole("button", { name: "Learning Units", expanded: true }));

    const stored = JSON.parse(localStorage.getItem(`lait.lesson-stages.${lessonId}`) ?? "{}") as {
      source: boolean;
      "learning-units": boolean;
    };
    expect(stored.source).toBe(true);
    expect(stored["learning-units"]).toBe(false);

    view.unmount();
    renderWorkspace();
    expect(await screen.findByRole("button", { name: "Source", expanded: true })).toBeInTheDocument();
    expect(screen.getByRole("button", { name: "Learning Units", expanded: false })).toBeInTheDocument();
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
        current: null,
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
    await user.click(screen.getByRole("button", { name: "Generate Exercises", expanded: false }));
    await user.click(
      within(screen.getByRole("region", { name: "Generate Exercises" })).getByRole("button", {
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
    await user.click(screen.getByRole("button", { name: "Generate Exercises", expanded: false }));
    await user.click(
      within(screen.getByRole("region", { name: "Generate Exercises" })).getByRole("button", {
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
});

const testDirectory = dirname(fileURLToPath(import.meta.url));

function walk(directory: string): string[] {
  const entries = readdirSync(directory, { withFileTypes: true });
  return entries.flatMap((entry) => {
    const path = join(directory, entry.name);
    return entry.isDirectory() ? walk(path) : [path];
  });
}

function installFetch(options: {
  units: UnitRecord[];
  source?: string;
  generate?: ReturnType<typeof deferred<Response>>;
  generateResult?: Response;
  practiceGet?: ReturnType<typeof deferred<Response>>;
  start?: ReturnType<typeof deferred<Response>>;
}): FetchCall[] {
  const calls: FetchCall[] = [];
  let units = options.units.map((unit) => ({ ...unit }));
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
      if (url.includes("/exercises/generate") && method === "POST") {
        if (options.generate) {
          return options.generate.promise;
        }
        return options.generateResult ?? jsonResponse({ status: "failed" }, 500);
      }
      if (url === "/api/practice-sessions" && method === "POST") {
        if (options.start) {
          return options.start.promise;
        }
        return new Response("missing", { status: 404 });
      }
      if (/\/api\/practice-sessions\/[^/]+$/.test(url) && method === "GET") {
        if (options.practiceGet) {
          return options.practiceGet.promise;
        }
        return new Response("missing", { status: 404 });
      }
      if (url.includes(`/api/lessons/${lessonId}`) && method === "GET") {
        return jsonResponse(lessonBody);
      }
      return new Response("missing", { status: 404 });
    }),
  );
  return calls;
}
