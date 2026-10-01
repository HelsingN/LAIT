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
  onGenerate: () => void;
};

export function GenerateExercisesStage({
  exerciseTypes,
  pending,
  outcome,
  acceptedCount,
  onGenerate,
}: GenerateExercisesStageProps) {
  const failureCopy =
    outcome?.status === "failed" ? (acceptedCount === 0 ? NO_ACCEPTED : GENERIC_FAILURE) : null;

  return (
    <div className={styles.panel}>
      {exerciseTypes.length > 0 ? (
        <ul className={styles.types}>
          {exerciseTypes.map((exercise) => (
            <li key={exercise.exercise_type}>{exercise.exercise_type}</li>
          ))}
        </ul>
      ) : null}
      <button type="button" className={styles.primary} disabled={pending} onClick={onGenerate}>
        {pending ? "Generating…" : "Generate Exercises"}
      </button>
      {outcome?.status === "completed" ? <p className={styles.status}>completed</p> : null}
      {failureCopy ? (
        <p className={styles.status} role="alert">
          {failureCopy}
        </p>
      ) : null}
    </div>
  );
}
