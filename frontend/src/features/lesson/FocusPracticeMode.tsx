import { useState, type ComponentType } from "react";

import { rendererFor, type RendererProps } from "../../registries/renderers/registry.ts";
import type { PracticeItemView, RendererFeedback, UnitLabel } from "../../registries/renderers/types.ts";
import styles from "./FocusPracticeMode.module.css";

const FROZEN_HINT = "Learning units are locked while practice is open. Exit Practice to edit them.";
const START_OVER_CONFIRMATION =
  "Start over: Abandon this practice run and start a new session on the same units? Submitted answers stay saved.";

type FocusPracticeModeProps = {
  sessionId: string;
  item: PracticeItemView | null;
  units: UnitLabel[];
  learnerExerciseTypes: string[];
  pending: boolean;
  submitError: string | null;
  feedback: RendererFeedback | null;
  onSubmit: RendererProps["onSubmit"];
  onContinue: () => void;
  onExit: () => void;
  onStartOver: () => void;
};

export function FocusPracticeMode({
  sessionId,
  item,
  units,
  learnerExerciseTypes,
  pending,
  submitError,
  feedback,
  onSubmit,
  onContinue,
  onExit,
  onStartOver,
}: FocusPracticeModeProps) {
  const [confirming, setConfirming] = useState(false);
  const Renderer = item ? learnerRenderer(item.exercise_type, learnerExerciseTypes) : undefined;

  return (
    <section className={styles.shell} aria-label="Focus Practice">
      <p className={styles.hint}>{FROZEN_HINT}</p>
      {Renderer && item ? (
        <Renderer
          key={`${sessionId}:${item.exercise_type}:${item.position}:${item.mode}:${item.learning_unit_id}`}
          item={item}
          units={units}
          pending={pending}
          submitError={submitError}
          feedback={feedback}
          onSubmit={onSubmit}
          onContinue={onContinue}
        />
      ) : null}
      <div className={styles.nav}>
        <button type="button" className={styles.secondary} onClick={onExit}>
          Exit Practice
        </button>
        <button type="button" className={styles.secondary} onClick={() => setConfirming(true)}>
          Start Over
        </button>
      </div>
      {confirming ? (
        <div className={styles.confirm} role="alertdialog" aria-label="Start Over">
          <p>{START_OVER_CONFIRMATION}</p>
          <button
            type="button"
            className={styles.secondary}
            onClick={() => {
              setConfirming(false);
              onStartOver();
            }}
          >
            Start Over
          </button>
        </div>
      ) : null}
    </section>
  );
}

function learnerRenderer(
  exerciseType: string,
  learnerExerciseTypes: string[],
): ComponentType<RendererProps> | undefined {
  if (!learnerExerciseTypes.includes(exerciseType)) {
    return undefined;
  }
  return rendererFor(exerciseType);
}
