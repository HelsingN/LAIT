// @vitest-environment jsdom
import "@testing-library/jest-dom/vitest";
import { cleanup, render, screen } from "@testing-library/react";
import { createElement } from "react";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { afterEach, expect, it } from "vitest";

import { FocusPracticeMode } from "../../features/lesson/FocusPracticeMode.tsx";
import { rendererFor } from "./registry.ts";
import type { PracticeItemView, RendererProps } from "./types.ts";

const testDirectory = dirname(fileURLToPath(import.meta.url));

function item(exerciseType: string): PracticeItemView {
  return {
    mode: "typed",
    learning_unit_id: "unit-1",
    exercise_type: exerciseType,
    position: 0,
    start: 0,
    end: 4,
    target_text: "proof",
    sentence: "proof <script>alert(1)</script>",
    segments: [{ kind: "text", text: "proof <script>alert(1)</script>" }],
    chip_unit_ids: [],
  };
}

function rendererProps(exerciseType: string): RendererProps {
  return {
    item: item(exerciseType),
    units: [],
    pending: false,
    submitError: null,
    feedback: null,
    onSubmit: () => undefined,
    onContinue: () => undefined,
  };
}

afterEach(() => {
  cleanup();
});

it("mounts the proof renderer by exercise_type", () => {
  const Renderer = rendererFor("proof");
  expect(Renderer).toBeTypeOf("function");
  render(createElement(Renderer as NonNullable<typeof Renderer>, rendererProps("proof")));
  const mounted = screen.getByTestId("proof-renderer");
  expect(mounted).toHaveTextContent("proof <script>alert(1)</script>");
  expect(mounted.querySelector("script")).toBeNull();
  expect(rendererFor("gap-fill")).not.toBe(Renderer);
});

it("learner focus practice never selects the proof renderer", () => {
  const focusSource = readFileSync(join(testDirectory, "../../features/lesson/FocusPracticeMode.tsx"), "utf8");
  const workspaceSource = readFileSync(
    join(testDirectory, "../../features/lesson/LessonWorkspacePage.tsx"),
    "utf8",
  );
  expect(focusSource).not.toContain("ProofRenderer");
  expect(focusSource).not.toContain("proof");
  expect(workspaceSource).not.toContain("ProofRenderer");
  expect(workspaceSource).not.toContain('"proof"');

  render(
    createElement(FocusPracticeMode, {
      ...rendererProps("proof"),
      learnerExerciseTypes: ["gap-fill"],
      onExit: () => undefined,
      onStartOver: () => undefined,
    }),
  );
  expect(screen.queryByTestId("proof-renderer")).not.toBeInTheDocument();
  expect(screen.getByRole("button", { name: "Exit Practice" })).toBeInTheDocument();
});
