// @vitest-environment jsdom
import "@testing-library/jest-dom/vitest";
import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { PracticeStage } from "./PracticeStage.tsx";

afterEach(() => {
  cleanup();
});

describe("Practice stage", () => {
  it("disables Start Practice while the start request is pending", () => {
    const onStart = vi.fn();
    const view = render(<PracticeStage enabled pending onStart={onStart} />);
    const button = screen.getByRole("button", { name: "Start Practice" });
    expect(button).toBeDisabled();
    button.click();
    expect(onStart).not.toHaveBeenCalled();

    view.rerender(<PracticeStage enabled pending={false} onStart={onStart} />);
    expect(screen.getByRole("button", { name: "Start Practice" })).toBeEnabled();
  });

  it("stays disabled when practice is not enabled", () => {
    render(<PracticeStage enabled={false} pending={false} onStart={() => undefined} />);
    expect(screen.getByRole("button", { name: "Start Practice" })).toBeDisabled();
  });
});
