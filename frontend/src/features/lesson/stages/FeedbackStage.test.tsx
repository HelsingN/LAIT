// @vitest-environment jsdom
import "@testing-library/jest-dom/vitest";
import { cleanup, render, screen, within } from "@testing-library/react";
import { afterEach, expect, it } from "vitest";

import { FeedbackStage, type FeedbackAttempt } from "./FeedbackStage.tsx";

const finished = "session-finished";
const earlier = "session-earlier";

function attempt(sessionId: string, attemptId: string, disposition: string, mode: string): FeedbackAttempt {
  return {
    attempt_id: attemptId,
    category: "correct",
    explanation: "matched",
    unit_text: "rolling out",
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
        attempt(earlier, "attempt-old", "completed", "drag"),
        attempt(finished, "attempt-now", "completed", "typed"),
      ]}
      onJump={() => undefined}
    />,
  );

  const current = screen.getByRole("region", { name: "Current pass" });
  expect(current).toHaveTextContent(finished);
  expect(current).toHaveTextContent("typed");
  expect(current).not.toHaveTextContent(earlier);
  const older = screen.getByRole("region", { name: "Earlier passes" });
  expect(within(older).getByRole("heading", { name: "Earlier passes" })).toBeInTheDocument();
  expect(older).toHaveTextContent(earlier);
  expect(older).toHaveTextContent("drag");
  expect(older).not.toHaveTextContent(finished);
});

it("uses the newest session as the current pass on a plain reload", () => {
  render(
    <FeedbackStage
      currentSessionId={null}
      attempts={[
        attempt(earlier, "attempt-old", "completed", "drag"),
        attempt(finished, "attempt-now", "exited", "typed"),
      ]}
      onJump={() => undefined}
    />,
  );

  const current = screen.getByRole("region", { name: "Current pass" });
  expect(current).toHaveTextContent(finished);
  expect(current).toHaveTextContent("left early");
  expect(current).not.toHaveTextContent("completed");
  expect(current).not.toHaveTextContent(earlier);
  expect(screen.getByRole("region", { name: "Earlier passes" })).toHaveTextContent(earlier);
});
