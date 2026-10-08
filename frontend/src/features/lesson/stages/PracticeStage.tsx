import styles from "./GenerateExercisesStage.module.css";

type PracticeStageProps = {
  enabled: boolean;
  pending: boolean;
  onStart: () => void;
};

export function PracticeStage({ enabled, pending, onStart }: PracticeStageProps) {
  return (
    <button
      type="button"
      className={styles.primary}
      disabled={!enabled || pending}
      onClick={onStart}
    >
      Start Practice
    </button>
  );
}
