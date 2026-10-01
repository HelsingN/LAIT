import styles from "./FeedbackStage.module.css";

export type FeedbackAttempt = {
  attempt_id: string;
  category: string;
  explanation: string;
  unit_text: string;
  span_start: number;
  span_end: number;
};

type FeedbackStageProps = {
  attempts: FeedbackAttempt[];
  onJump: (attempt: FeedbackAttempt) => void;
};

export function FeedbackStage({ attempts, onJump }: FeedbackStageProps) {
  if (attempts.length === 0) {
    return <p className={styles.empty}>No attempts yet. Start Practice to begin.</p>;
  }

  return (
    <ul className={styles.list}>
      {attempts.map((attempt) => (
        <li key={attempt.attempt_id} className={styles.row}>
          <p className={styles.category}>{attempt.category}</p>
          <p className={styles.explanation}>{attempt.explanation}</p>
          <button type="button" className={styles.jump} onClick={() => onJump(attempt)}>
            {attempt.unit_text}
          </button>
        </li>
      ))}
    </ul>
  );
}
