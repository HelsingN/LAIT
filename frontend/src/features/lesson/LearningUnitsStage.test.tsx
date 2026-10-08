// @vitest-environment jsdom
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import "@testing-library/jest-dom/vitest";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { useState } from "react";
import { afterEach, expect, it, vi } from "vitest";

import type { LearningUnit } from "./lessonApi.ts";
import type { CodePointRange } from "./selectionOffsets.ts";
import { LearningUnitsStage } from "./stages/LearningUnitsStage.tsx";
import { SourceStage } from "./stages/SourceStage.tsx";

const draft: LearningUnit = {
  id: "unit-draft",
  lesson_id: "lesson-1",
  start: 0,
  end: 3,
  text: "out",
  status: "draft",
  created_at: "2026-10-01T00:00:00+00:00",
  removed_at: null,
};

function renderStage(props: Partial<Parameters<typeof LearningUnitsStage>[0]> = {}) {
  return render(
    <LearningUnitsStage
      lessonId="lesson-1"
      units={[]}
      selection={null}
      practiceOpen={false}
      onChanged={() => {}}
      onJump={() => {}}
      {...props}
    />,
  );
}

afterEach(() => {
  cleanup();
  vi.unstubAllGlobals();
});

it("shows the empty learning units copy", () => {
  renderStage();
  expect(screen.getByRole("heading", { name: "No learning units" })).toBeInTheDocument();
  expect(
    screen.getByText("Select a phrase in the source, then choose Add Learning Unit."),
  ).toBeInTheDocument();
});

it("does not call the API when Add Learning Unit has no selection", async () => {
  const fetchMock = vi.fn();
  vi.stubGlobal("fetch", fetchMock);
  const user = userEvent.setup();
  renderStage();
  const add = screen.getByRole("button", { name: "Add Learning Unit" });
  expect(add).toHaveAttribute("aria-describedby", "add-unit-hint");
  expect(add).toHaveAttribute("aria-disabled", "true");
  expect(add).toBeEnabled();
  fireEvent.click(add);
  add.focus();
  const tooltip = screen.getByRole("tooltip");
  expect(tooltip).toHaveTextContent("Select text in the source before adding a unit.");
  expect(add.compareDocumentPosition(tooltip) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
  await user.keyboard("{Enter}");
  expect(fetchMock).not.toHaveBeenCalled();
  expect(screen.getByRole("tooltip")).toBeInTheDocument();
  await user.keyboard("{Escape}");
  expect(add).not.toHaveFocus();
  const css = readFileSync(
    join(dirname(fileURLToPath(import.meta.url)), "stages", "LearningUnitsStage.module.css"),
    "utf8",
  );
  expect(css).toMatch(/\.addTooltip\s*\{[^}]*position:\s*absolute/s);
  expect(css).toMatch(/:focus-within \.addTooltip/);
  expect(css).not.toMatch(/\.hint\s*\{/);
});

it("hides the selection tooltip once text is selected", () => {
  renderStage({ selection: { start: 0, end: 4 } });
  const add = screen.getByRole("button", { name: "Add Learning Unit" });
  expect(add).toBeEnabled();
  expect(add).not.toHaveAttribute("aria-disabled");
  expect(screen.queryByRole("tooltip")).not.toBeInTheDocument();
  expect(screen.queryByText("Select text in the source before adding a unit.")).not.toBeInTheDocument();
});

it("renders the overlap error and keeps the existing unit", async () => {
  vi.stubGlobal(
    "fetch",
    vi.fn(async () => new Response(JSON.stringify({ detail: "" }), { status: 422 })),
  );
  const user = userEvent.setup();
  renderStage({
    units: [draft],
    selection: { start: 1, end: 4 },
  });
  await user.click(screen.getByRole("button", { name: "Add Learning Unit" }));
  expect(
    await screen.findByText("That selection overlaps an existing unit. Choose a non-overlapping span."),
  ).toBeInTheDocument();
  expect(screen.getAllByText("out").length).toBeGreaterThan(0);
});

it("disables unit controls and shows the frozen hint while practice is open", async () => {
  const user = userEvent.setup();
  renderStage({ units: [draft], practiceOpen: true, selection: { start: 0, end: 3 } });
  expect(
    screen.getByText("Learning units are locked while practice is open. Exit Practice to edit them."),
  ).toBeInTheDocument();
  expect(screen.getByRole("button", { name: "Add Learning Unit" })).toBeDisabled();
  expect(screen.getByRole("button", { name: "Accept" })).toBeDisabled();
  expect(screen.queryByRole("button", { name: "Remove out" })).not.toBeInTheDocument();
  await user.click(screen.getByRole("button", { name: "out" }));
  expect(screen.getByRole("button", { name: "Remove out" })).toBeDisabled();
});

it("shows one phrase, Accept on a draft, and Remove only after selection", async () => {
  const user = userEvent.setup();
  const accepted: LearningUnit = {
    ...draft,
    id: "unit-accepted",
    text: "rolling out",
    status: "accepted",
  };
  renderStage({ units: [accepted, draft] });

  expect(screen.getAllByText("rolling out")).toHaveLength(1);
  expect(screen.getAllByText("out")).toHaveLength(1);
  expect(screen.queryByText("accepted")).not.toBeInTheDocument();
  expect(screen.queryByText("draft")).not.toBeInTheDocument();
  expect(screen.getByRole("button", { name: "Accept" })).toBeEnabled();
  expect(screen.queryByRole("button", { name: "Remove rolling out" })).not.toBeInTheDocument();

  const units = document.getElementById("units");
  expect(units).not.toBeNull();
  expect(units?.contains(screen.getByRole("button", { name: "Add Learning Unit" }))).toBe(false);

  const row = screen.getByRole("button", { name: "rolling out" });
  row.focus();
  await user.keyboard("{Enter}");
  const remove = screen.getByRole("button", { name: "Remove rolling out" });
  expect(remove.querySelector("[aria-hidden='true']")).toHaveTextContent("×");
  expect(remove).not.toHaveTextContent("rolling out");

  screen.getByRole("button", { name: "out" }).focus();
  await user.keyboard(" ");
  expect(screen.getByRole("button", { name: "Remove out" })).toBeInTheDocument();
  expect(screen.queryByRole("button", { name: "Remove rolling out" })).not.toBeInTheDocument();
});

it("converts a selection after an emoji to Unicode code points", async () => {
  const calls: { start: number; end: number; keys: string[] }[] = [];
  vi.stubGlobal(
    "fetch",
    vi.fn(async (_input: RequestInfo | URL, init?: RequestInit) => {
      const body = JSON.parse(String(init?.body)) as { start: number; end: number };
      calls.push({ start: body.start, end: body.end, keys: Object.keys(body) });
      return new Response(
        JSON.stringify({
          id: "unit-emoji",
          lesson_id: "lesson-1",
          start: body.start,
          end: body.end,
          text: "out",
          status: "draft",
          created_at: "2026-10-01T00:00:00+00:00",
          removed_at: null,
        }),
        { status: 201, headers: { "content-type": "application/json" } },
      );
    }),
  );

  function Harness() {
    const [selection, setSelection] = useState<CodePointRange | null>(null);
    return (
      <>
        <SourceStage source="👍out" highlight={null} onSelectionChange={setSelection} />
        <LearningUnitsStage
          lessonId="lesson-1"
          units={[]}
          selection={selection}
          practiceOpen={false}
          onChanged={() => {}}
          onJump={() => {}}
        />
      </>
    );
  }

  const user = userEvent.setup();
  render(<Harness />);
  const sourceBody = screen.getByTestId("source-body");
  const textNode = sourceBody.firstChild;
  if (!textNode || textNode.textContent !== "👍out") {
    throw new Error("emoji fixture was not rendered as one text node");
  }
  expect(textNode.textContent.length).toBe(5);

  const range = document.createRange();
  range.setStart(textNode, 2);
  range.setEnd(textNode, 5);
  const selection = window.getSelection();
  selection?.removeAllRanges();
  selection?.addRange(range);
  fireEvent.mouseUp(sourceBody);

  await user.click(screen.getByRole("button", { name: "Add Learning Unit" }));

  expect(calls).toEqual([{ start: 1, end: 4, keys: ["start", "end"] }]);
  expect(calls[0]).not.toMatchObject({ start: 2, end: 5 });
});
