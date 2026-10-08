import { useState } from "react";

import {
  acceptLearningUnit,
  addLearningUnit,
  LearningUnitRequestError,
  removeLearningUnit,
  type LearningUnit,
} from "../lessonApi.ts";
import type { CodePointRange } from "../selectionOffsets.ts";
import styles from "./LearningUnitsStage.module.css";

const OVERLAP_ERROR = "That selection overlaps an existing unit. Choose a non-overlapping span.";
const FROZEN_HINT = "Learning units are locked while practice is open. Exit Practice to edit them.";
const EMPTY_SELECTION_HINT = "Select text in the source before adding a unit.";

type LearningUnitsStageProps = {
  lessonId: string;
  units: LearningUnit[];
  selection: CodePointRange | null;
  practiceOpen: boolean;
  onChanged: () => Promise<void> | void;
  onJump: (unit: LearningUnit) => void;
};

export function LearningUnitsStage({
  lessonId,
  units,
  selection,
  practiceOpen,
  onChanged,
  onJump,
}: LearningUnitsStageProps) {
  const [overlapError, setOverlapError] = useState<string | null>(null);
  const [frozenByServer, setFrozenByServer] = useState(false);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [hintSuppressed, setHintSuppressed] = useState(false);
  const locked = practiceOpen || frozenByServer;
  const needsSelection = !locked && !selection;
  const liveUnits = units.filter((unit) => unit.removed_at === null);

  async function addUnit() {
    if (!selection || locked) {
      return;
    }
    try {
      await addLearningUnit(lessonId, selection.start, selection.end);
      setOverlapError(null);
      await onChanged();
    } catch (error) {
      if (error instanceof LearningUnitRequestError && error.kind === "overlap") {
        setOverlapError(OVERLAP_ERROR);
        return;
      }
      if (error instanceof LearningUnitRequestError && error.kind === "frozen") {
        setFrozenByServer(true);
      }
    }
  }

  async function acceptUnit(unitId: string) {
    if (locked) {
      return;
    }
    try {
      await acceptLearningUnit(lessonId, unitId);
      await onChanged();
    } catch (error) {
      if (error instanceof LearningUnitRequestError && error.kind === "frozen") {
        setFrozenByServer(true);
      }
    }
  }

  async function deleteUnit(unitId: string) {
    if (locked) {
      return;
    }
    try {
      await removeLearningUnit(lessonId, unitId);
      setSelectedId((current) => (current === unitId ? null : current));
      await onChanged();
    } catch (error) {
      if (error instanceof LearningUnitRequestError && error.kind === "frozen") {
        setFrozenByServer(true);
      }
    }
  }

  function selectUnit(unit: LearningUnit) {
    setSelectedId(unit.id);
    onJump(unit);
  }

  return (
    <div className={styles.root}>
      {locked ? <p className={styles.frozen}>{FROZEN_HINT}</p> : null}
      <div
        className={hintSuppressed ? `${styles.addSlot} ${styles.addSlotSuppressed}` : styles.addSlot}
        onMouseLeave={() => setHintSuppressed(false)}
      >
        <button
          type="button"
          className={styles.primary}
          disabled={locked}
          aria-disabled={needsSelection ? true : undefined}
          aria-describedby={needsSelection ? "add-unit-hint" : undefined}
          onClick={() => void addUnit()}
          onKeyDown={(event) => {
            if (event.key === "Escape" && needsSelection) {
              setHintSuppressed(true);
              event.currentTarget.blur();
            }
          }}
        >
          Add Learning Unit
        </button>
        {needsSelection ? (
          <span id="add-unit-hint" role="tooltip" className={styles.addTooltip}>
            {EMPTY_SELECTION_HINT}
          </span>
        ) : null}
      </div>
      {overlapError ? (
        <p className={styles.error} role="alert">
          {overlapError}
        </p>
      ) : null}
      {liveUnits.length === 0 ? (
        <div className={styles.scroller}>
          <div className={styles.empty}>
            <h3>No learning units</h3>
            <p>Select a phrase in the source, then choose Add Learning Unit.</p>
          </div>
        </div>
      ) : (
        <ul id="units" className={styles.list}>
          {liveUnits.map((unit) => {
            const selected = selectedId === unit.id;
            return (
              <li key={unit.id} className={selected ? `${styles.row} ${styles.rowSelected}` : styles.row}>
                <button type="button" className={styles.phrase} onClick={() => selectUnit(unit)}>
                  {unit.text}
                </button>
                {unit.status === "draft" ? (
                  <button
                    type="button"
                    className={styles.accept}
                    disabled={locked}
                    onClick={() => void acceptUnit(unit.id)}
                  >
                    Accept
                  </button>
                ) : null}
                {selected ? (
                  <button
                    type="button"
                    className={styles.remove}
                    aria-label={`Remove ${unit.text}`}
                    disabled={locked}
                    onClick={() => void deleteUnit(unit.id)}
                  >
                    <span aria-hidden="true">×</span>
                  </button>
                ) : null}
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}
