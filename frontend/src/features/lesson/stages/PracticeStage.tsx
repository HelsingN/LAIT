import styles from "./GenerateExercisesStage.module.css";

type PracticeStageProps = {
  enabled: boolean;
  onStart: () => void;
};

export function PracticeStage({ enabled, onStart }: PracticeStageProps) {
  return (
    <button type="button" className={styles.primary} disabled={!enabled} onClick={onStart}>
      Start Practice
    </button>
  );
}
