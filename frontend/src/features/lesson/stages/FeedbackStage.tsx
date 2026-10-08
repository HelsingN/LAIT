import styles from "./FeedbackStage.module.css";

export type FeedbackAttempt = {
  attempt_id: string;
  category: string;
  explanation: string;
  unit_text: string;
  span_start: number;
  span_end: number;
  session_id: string;
  session_disposition: string;
  mode: string;
  pass_item_count?: number;
};

type FeedbackStageProps = {
  attempts: FeedbackAttempt[];
  currentSessionId: string | null;
  onJump: (attempt: FeedbackAttempt) => void;
};

function modeLabel(mode: string): string {
  if (mode === "drag") {
    return "Choice";
  }
  if (mode === "typed") {
    return "Typed";
  }
  return mode;
}

function categoryLabel(category: string): string {
  if (category === "correct") {
    return "Correct";
  }
  if (category === "incorrect") {
    return "Incorrect";
  }
  if (category === "corrected") {
    return "Corrected";
  }
  return category;
}

function itemKey(attempt: FeedbackAttempt): string {
  return `${attempt.mode}:${attempt.span_start}:${attempt.span_end}`;
}

function scoreLabel(attempts: FeedbackAttempt[]): string {
  const first = new Map<string, string>();
  for (const attempt of attempts) {
    const key = itemKey(attempt);
    if (!first.has(key)) {
      first.set(key, attempt.category);
    }
  }
  const correct = [...first.values()].filter((category) => category === "correct").length;
  const declared = attempts.find((attempt) => attempt.pass_item_count !== undefined)?.pass_item_count;
  const denominator = declared !== undefined && declared > 0 ? declared : first.size;
  return `${correct}/${denominator}`;
}

function passLabel(disposition: string): string {
  if (disposition === "exited") {
    return "left early";
  }
  if (disposition === "completed") {
    return "completed";
  }
  if (disposition === "abandoned") {
    return "abandoned";
  }
  return "open";
}

function sessionOrder(attempts: FeedbackAttempt[]): string[] {
  const sessionIds: string[] = [];
  for (const attempt of attempts) {
    if (!sessionIds.includes(attempt.session_id)) {
      sessionIds.push(attempt.session_id);
    }
  }
  return sessionIds;
}

export function FeedbackStage({ attempts, currentSessionId, onJump }: FeedbackStageProps) {
  if (attempts.length === 0) {
    return <p className={styles.empty}>No attempts yet. Start Practice to begin.</p>;
  }

  const sessionIds = sessionOrder(attempts);
  const newest = sessionIds[sessionIds.length - 1] ?? null;
  const current =
    currentSessionId !== null && sessionIds.includes(currentSessionId) ? currentSessionId : newest;
  const currentAttempts = attempts.filter((attempt) => attempt.session_id === current);
  const earlierIds = sessionIds.filter((sessionId) => sessionId !== current);

  return (
    <div>
      <section aria-label="Current pass">
        <h3>Current pass</h3>
        <p>{scoreLabel(currentAttempts)}</p>
        <p>{passLabel(currentAttempts[0]?.session_disposition ?? "")}</p>
        <AttemptRows attempts={currentAttempts} onJump={onJump} />
      </section>
      {earlierIds.length > 0 ? (
        <section aria-label="Earlier passes">
          <h3>Earlier passes</h3>
          {earlierIds.map((sessionId) => {
            const rows = attempts.filter((attempt) => attempt.session_id === sessionId);
            return (
              <div key={sessionId}>
                <p>{passLabel(rows[0]?.session_disposition ?? "")}</p>
                <AttemptRows attempts={rows} onJump={onJump} />
              </div>
            );
          })}
        </section>
      ) : null}
    </div>
  );
}

function AttemptRows({
  attempts,
  onJump,
}: {
  attempts: FeedbackAttempt[];
  onJump: (attempt: FeedbackAttempt) => void;
}) {
  return (
    <ul className={styles.list}>
      {attempts.map((attempt) => (
        <li key={attempt.attempt_id} className={styles.row}>
          <p className={styles.category}>{modeLabel(attempt.mode)}</p>
          <p className={styles.category}>{categoryLabel(attempt.category)}</p>
          <p className={styles.explanation}>{attempt.explanation}</p>
          <button type="button" className={styles.jump} onClick={() => onJump(attempt)}>
            {attempt.unit_text}
          </button>
        </li>
      ))}
    </ul>
  );
}
