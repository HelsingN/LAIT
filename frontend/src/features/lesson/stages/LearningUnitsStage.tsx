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
  const locked = practiceOpen || frozenByServer;
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
      await onChanged();
    } catch (error) {
      if (error instanceof LearningUnitRequestError && error.kind === "frozen") {
        setFrozenByServer(true);
      }
    }
  }

  return (
    <div>
      {locked ? <p className={styles.frozen}>{FROZEN_HINT}</p> : null}
      {liveUnits.length === 0 ? (
        <div className={styles.empty}>
          <h3>No learning units</h3>
          <p>Select a phrase in the source, then choose Add Learning Unit.</p>
        </div>
      ) : (
        <ul className={styles.list}>
          {liveUnits.map((unit) => (
            <li key={unit.id} className={styles.row}>
              <p className={styles.unitText}>{unit.text}</p>
              <span className={styles.badge}>{unit.status}</span>
              <button type="button" className={styles.jump} onClick={() => onJump(unit)} disabled={locked}>
                {unit.text}
              </button>
              <div className={styles.actions}>
                {unit.status === "draft" ? (
                  <button
                    type="button"
                    className={styles.primary}
                    disabled={locked}
                    onClick={() => void acceptUnit(unit.id)}
                  >
                    Accept
                  </button>
                ) : null}
                <button
                  type="button"
                  className={styles.destructive}
                  disabled={locked}
                  onClick={() => void deleteUnit(unit.id)}
                >
                  Delete
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
      {overlapError ? (
        <p className={styles.error} role="alert">
          {overlapError}
        </p>
      ) : null}
      {!locked && !selection ? <p className={styles.hint}>{EMPTY_SELECTION_HINT}</p> : null}
      <button type="button" className={styles.primary} disabled={locked || !selection} onClick={() => void addUnit()}>
        Add Learning Unit
      </button>
    </div>
  );
}
