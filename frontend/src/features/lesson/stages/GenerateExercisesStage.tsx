import type { GenerationResult, LearnerExerciseType } from "../lessonApi.ts";
import styles from "./GenerateExercisesStage.module.css";

const NO_ACCEPTED =
  "No accepted units to practice. Accept at least one draft unit, then generate again.";
const GENERIC_FAILURE =
  "Exercise generation failed. Check your accepted units and try Generate Exercises again.";

type GenerateExercisesStageProps = {
  exerciseTypes: LearnerExerciseType[];
  pending: boolean;
  outcome: GenerationResult | null;
  acceptedCount: number;
  ready: boolean;
  onGenerate: () => void;
};

export function GenerateExercisesStage({
  exerciseTypes,
  pending,
  outcome,
  acceptedCount,
  ready,
  onGenerate,
}: GenerateExercisesStageProps) {
  const failureCopy =
    outcome?.status === "failed" ? (acceptedCount === 0 ? NO_ACCEPTED : GENERIC_FAILURE) : null;
  const showGenerate = pending || !ready;

  return (
    <div className={styles.panel}>
      {exerciseTypes.length > 0 ? (
        <ul className={styles.types}>
          {exerciseTypes.map((exercise) => (
            <li key={exercise.exercise_type}>{exercise.exercise_type}</li>
          ))}
        </ul>
      ) : null}
      {showGenerate ? (
        <button type="button" className={styles.primary} disabled={pending} onClick={onGenerate}>
          {pending ? "Generating…" : "Generate Exercises"}
        </button>
      ) : null}
      {ready ? <p className={styles.ready}>Exercises are ready.</p> : null}
      {failureCopy ? (
        <p className={styles.status} role="alert">
          {failureCopy}
        </p>
      ) : null}
    </div>
  );
}
