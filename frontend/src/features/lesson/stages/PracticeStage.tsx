import styles from "./GenerateExercisesStage.module.css";

type PracticeStageProps = {
  enabled: boolean;
};

export function PracticeStage({ enabled }: PracticeStageProps) {
  return (
    <button type="button" className={styles.primary} disabled={!enabled}>
      Start Practice
    </button>
  );
}
