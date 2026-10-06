// @vitest-environment jsdom
import "@testing-library/jest-dom/vitest";
import { cleanup, render, screen, within } from "@testing-library/react";
import { afterEach, expect, it } from "vitest";

import { FeedbackStage, type FeedbackAttempt } from "./FeedbackStage.tsx";

const finished = "session-finished";
const earlier = "session-earlier";

function attempt(
  sessionId: string,
  attemptId: string,
  disposition: string,
  mode: string,
  unitText = "rolling out",
): FeedbackAttempt {
  return {
    attempt_id: attemptId,
    category: "correct",
    explanation: "matched",
    unit_text: unitText,
    span_start: 0,
    span_end: 5,
    session_id: sessionId,
    session_disposition: disposition,
    mode,
  };
}

afterEach(() => {
  cleanup();
});

it("keeps the finished session out of Earlier passes", () => {
  render(
    <FeedbackStage
      currentSessionId={finished}
      attempts={[
        attempt(earlier, "attempt-old", "completed", "drag", "kept earlier"),
        attempt(finished, "attempt-now", "completed", "typed"),
      ]}
      onJump={() => undefined}
    />,
  );

  const current = screen.getByRole("region", { name: "Current pass" });
  expect(within(current).getByRole("heading", { name: "Current pass" })).toBeInTheDocument();
  expect(current).toHaveTextContent("1/1");
  expect(current).toHaveTextContent("Typed");
  expect(current).toHaveTextContent("Correct");
  expect(current).not.toHaveTextContent(finished);
  expect(current).not.toHaveTextContent("typed");
  expect(current).not.toHaveTextContent("kept earlier");
  const older = screen.getByRole("region", { name: "Earlier passes" });
  expect(within(older).getByRole("heading", { name: "Earlier passes" })).toBeInTheDocument();
  expect(older).toHaveTextContent("kept earlier");
  expect(older).toHaveTextContent("Choice");
  expect(older).not.toHaveTextContent(earlier);
  expect(older).not.toHaveTextContent(finished);
});

it("uses the newest session as the current pass on a plain reload", () => {
  render(
    <FeedbackStage
      currentSessionId={null}
      attempts={[
        attempt(earlier, "attempt-old", "completed", "drag", "kept earlier"),
        attempt(finished, "attempt-now", "exited", "typed"),
      ]}
      onJump={() => undefined}
    />,
  );

  const current = screen.getByRole("region", { name: "Current pass" });
  expect(within(current).getByRole("heading", { name: "Current pass" })).toBeInTheDocument();
  expect(current).toHaveTextContent("1/1");
  expect(current).toHaveTextContent("left early");
  expect(current).not.toHaveTextContent("completed");
  expect(current).not.toHaveTextContent(finished);
  expect(current).not.toHaveTextContent("kept earlier");
  expect(screen.getByRole("region", { name: "Earlier passes" })).toHaveTextContent("kept earlier");
});

it("scores first-try corrects against the pass size and offers missed practice", () => {
  const rows: FeedbackAttempt[] = [
    ...[0, 1, 2, 3, 4, 5].map((index) => ({
      ...attempt(finished, `correct-${index}`, "completed", "typed"),
      span_start: index,
      span_end: index + 1,
      pass_item_count: 8,
    })),
    {
      ...attempt(finished, "miss", "completed", "drag"),
      category: "incorrect",
      span_start: 20,
      span_end: 21,
      pass_item_count: 8,
    },
    {
      ...attempt(finished, "fix", "completed", "drag"),
      category: "corrected",
      span_start: 20,
      span_end: 21,
      pass_item_count: 8,
    },
    {
      ...attempt(finished, "miss-2", "completed", "typed", "other"),
      category: "incorrect",
      span_start: 30,
      span_end: 31,
      pass_item_count: 8,
    },
  ];
  render(
    <FeedbackStage
      currentSessionId={finished}
      attempts={rows}
      onJump={() => undefined}
    />,
  );

  const current = screen.getByRole("region", { name: "Current pass" });
  expect(current).toHaveTextContent("6/8");
  expect(current).toHaveTextContent("Corrected");
  expect(screen.queryByRole("button", { name: "Practice missed phrases" })).not.toBeInTheDocument();
});
