import { useState } from "react";

import styles from "./GapFillRenderer.module.css";
import type { RendererProps, UnitLabel } from "./types.ts";

export function GapFillRenderer({
  item,
  units,
  pending,
  submitError,
  feedback,
  onSubmit,
  onContinue,
}: RendererProps) {
  const [draft, setDraft] = useState("");
  const [selectedUnitId, setSelectedUnitId] = useState<string | null>(null);
  const drag = item.mode === "drag";
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
    <div className={styles.root}>
      <p className={styles.sentence} data-testid="gap-fill-sentence">
        {item.segments.map((segment, index) =>
          segment.kind === "blank" ? (
            <span key={index} className={styles.blank} data-testid="gap-fill-blank">
              {segment.text}
            </span>
          ) : (
            <span key={index}>{segment.text}</span>
          ),
        )}
      </p>
      {drag ? (
        <div className={styles.chipBank} data-testid="chip-bank">
          {item.chip_unit_ids.map((unitId) => (
            <ChipButton
              key={unitId}
              unit={units.find((candidate) => candidate.id === unitId) ?? { id: unitId, text: unitId }}
              pressed={selectedUnitId === unitId}
              onSelect={setSelectedUnitId}
            />
          ))}
        </div>
      ) : (
        <input
          className={styles.answer}
          aria-label="Answer"
          value={draft}
          onChange={(event) => setDraft(event.target.value)}
        />
      )}
      {submitError ? (
        <p className={styles.error} role="alert">
          {submitError}
        </p>
      ) : null}
      {feedback ? <FeedbackCard feedback={feedback} /> : null}
      {feedback ? (
        <button type="button" className={styles.primary} onClick={onContinue}>
          Continue
        </button>
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
  onSelect,
}: {
  unit: UnitLabel;
  pressed: boolean;
  onSelect: (unitId: string) => void;
}) {
  return (
    <button
      type="button"
      className={styles.chip}
      aria-pressed={pressed}
      onClick={() => onSelect(unit.id)}
    >
      {unit.text}
    </button>
  );
}

function FeedbackCard({ feedback }: { feedback: RendererProps["feedback"] }) {
  if (!feedback) {
    return null;
  }
  const tone = feedback.category === "incorrect" ? styles.incorrect : styles.correct;
  return (
    <article className={styles.card} data-testid="feedback-card">
      <p className={tone}>{feedback.category}</p>
      <p>{feedback.submitted}</p>
      <p>{feedback.expected}</p>
      <p>{feedback.explanation}</p>
      {feedback.chunks_used.length > 0 ? <p>used {feedback.chunks_used.join(", ")}</p> : null}
      {feedback.chunks_missed.length > 0 ? <p>missed {feedback.chunks_missed.join(", ")}</p> : null}
      {feedback.natural_alternative != null ? <p>{feedback.natural_alternative}</p> : null}
    </article>
  );
}
