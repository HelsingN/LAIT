import { useEffect, useState } from "react";

import styles from "./GapFillRenderer.module.css";
import { stripEmphasis } from "./stripEmphasis.ts";
import type { RendererProps, UnitLabel } from "./types.ts";

export function GapFillRenderer({
  item,
  units,
  pending,
  submitError,
  feedback,
  revealed = false,
  onSubmit,
  onContinue,
  onTryAgain,
  onShowAnswer,
}: RendererProps) {
  const [draft, setDraft] = useState("");
  const [selectedUnitId, setSelectedUnitId] = useState<string | null>(null);
  const [answerEditable, setAnswerEditable] = useState(false);
  const drag = item.mode === "drag";
  const graded = feedback !== null;
  const incorrect = feedback?.category === "incorrect";
  const accepted = feedback?.category === "correct" || feedback?.category === "corrected";
  const disclosed = accepted || revealed;
  const inlineAnswer = feedback ? (disclosed ? feedback.expected : feedback.submitted) : "";

  useEffect(() => {
    if (feedback !== null) {
      return;
    }
    setDraft("");
    setSelectedUnitId(null);
  }, [feedback]);
  const selected = units.find((unit) => unit.id === selectedUnitId) ?? null;
  const canSubmit = drag ? selected !== null : draft.trim() !== "";

  function submit() {
    if (!canSubmit || pending || feedback) {
      return;
    }
    if (drag && selected) {
      onSubmit({ text: selected.text, submittedUnitId: selected.id });
      return;
    }
    onSubmit({ text: draft, submittedUnitId: null });
  }

  return (
    <div className={styles.root} data-testid={feedback ? "feedback-card" : undefined}>
      <p className={styles.sentence} data-testid="gap-fill-sentence">
        {item.segments.map((segment, index) =>
          segment.kind === "blank" ? (
            <span
              key={index}
              className={[styles.blank, graded ? styles.answered : "", accepted ? styles.accepted : incorrect && !revealed ? styles.incorrect : ""].filter(Boolean).join(" ")}
              data-testid="gap-fill-blank"
            >
              {inlineAnswer}
            </span>
          ) : (
            <span key={index}>{stripEmphasis(segment.text)}</span>
          ),
        )}
      </p>
      {graded ? null : drag ? (
        <div className={styles.chipBank} data-testid="chip-bank">
          {item.chip_unit_ids.map((unitId) => (
            <ChipButton
              key={unitId}
              unit={units.find((candidate) => candidate.id === unitId) ?? { id: unitId, text: unitId }}
              pressed={selectedUnitId === unitId}
              disabled={graded}
              onSelect={setSelectedUnitId}
            />
          ))}
        </div>
      ) : (
        <>
          <label className={styles.answerLabel} htmlFor="gap-fill-answer">
            Answer
          </label>
          <p id="gap-fill-instruction" className={styles.instruction}>
            Type the missing words.
          </p>
          <input
            id="gap-fill-answer"
            className={styles.answer}
            aria-describedby="gap-fill-instruction"
            autoComplete="off"
            autoCorrect="off"
            autoCapitalize="none"
            data-1p-ignore="true"
            data-lpignore="true"
            data-form-type="other"
            readOnly={!answerEditable}
            value={draft}
            disabled={graded}
            onFocus={(event) => {
              event.currentTarget.readOnly = false;
              setAnswerEditable(true);
            }}
            onChange={(event) => setDraft(event.target.value)}
          />
        </>
      )}
      {submitError ? (
        <p className={styles.error} role="alert">
          {submitError}
        </p>
      ) : null}
      {feedback ? <p className={accepted ? styles.correct : styles.incorrect} role="status">{resultWord(feedback.category)}</p> : null}
      {feedback ? (
        <>
          {incorrect ? (
            <>
              <button type="button" className={styles.primary} onClick={() => onTryAgain?.()}>
                Try again
              </button>
              {!revealed ? <button type="button" className={styles.primary} onClick={() => onShowAnswer?.()}>
                Show answer
              </button> : null}
            </>
          ) : null}
          <button type="button" className={styles.primary} onClick={onContinue}>
            Continue
          </button>
        </>
      ) : (
        <button type="button" className={styles.primary} disabled={pending || !canSubmit} onClick={submit}>
          {pending ? "Checking…" : "Submit Answer"}
        </button>
      )}
    </div>
  );
}

function ChipButton({
  unit,
  pressed,
  disabled,
  onSelect,
}: {
  unit: UnitLabel;
  pressed: boolean;
  disabled: boolean;
  onSelect: (unitId: string) => void;
}) {
  return (
    <button
      type="button"
      className={styles.chip}
      aria-pressed={pressed}
      disabled={disabled}
      onClick={() => {
        if (disabled) {
          return;
        }
        onSelect(unit.id);
      }}
    >
      {unit.text}
    </button>
  );
}

function resultWord(category: string): string {
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
