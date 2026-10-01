import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState, type ReactNode } from "react";
import { Link, useParams } from "react-router";

import {
  generateExercises,
  getLesson,
  listLearnerExerciseTypes,
  listLearningUnits,
  type GenerationResult,
  type LearningUnit,
} from "./lessonApi.ts";
import styles from "./LessonWorkspacePage.module.css";
import { type CodePointRange } from "./selectionOffsets.ts";
import { FeedbackStage } from "./stages/FeedbackStage.tsx";
import { GenerateExercisesStage } from "./stages/GenerateExercisesStage.tsx";
import { LearningUnitsStage } from "./stages/LearningUnitsStage.tsx";
import { PracticeStage } from "./stages/PracticeStage.tsx";
import { SourceStage } from "./stages/SourceStage.tsx";
import {
  loadStageExpansion,
  saveStageExpansion,
  type StageExpansion,
  type StageId,
} from "./stageState.ts";

const LOAD_ERROR = "Could not load this lesson. Return to the lesson list and open it again.";

function sameIdSet(left: string[], right: string[]): boolean {
  if (left.length !== right.length) {
    return false;
  }
  const sortedLeft = [...left].sort();
  const sortedRight = [...right].sort();
  return sortedLeft.every((id, index) => id === sortedRight[index]);
}

export function LessonWorkspacePage() {
  const { id = "" } = useParams();
  const queryClient = useQueryClient();
  const [expansion, setExpansion] = useState<StageExpansion>(() => loadStageExpansion(id));
  const [selection, setSelection] = useState<CodePointRange | null>(null);
  const [highlight, setHighlight] = useState<CodePointRange | null>(null);
  const [generation, setGeneration] = useState<GenerationResult | null>(null);
  const [practiceUnlocked, setPracticeUnlocked] = useState(false);

  const lessonQuery = useQuery({
    queryKey: ["lesson", id],
    queryFn: () => getLesson(id),
    enabled: id !== "",
  });
  const unitsQuery = useQuery({
    queryKey: ["learning-units", id],
    queryFn: () => listLearningUnits(id),
    enabled: id !== "" && lessonQuery.isSuccess,
  });
  const exerciseTypesQuery = useQuery({
    queryKey: ["learner-exercise-types"],
    queryFn: listLearnerExerciseTypes,
  });
  const generateMutation = useMutation({
    mutationFn: () => generateExercises(id),
    onSuccess: (result) => {
      setGeneration(result);
      if (result.status === "completed") {
        setPracticeUnlocked(true);
        setExpansion((current) => {
          const next = { ...current, practice: true };
          saveStageExpansion(id, next);
          return next;
        });
      }
    },
  });

  const units = unitsQuery.data?.learning_units ?? [];
  const acceptedIds = units.filter((unit) => unit.status === "accepted").map((unit) => unit.id);
  const practiceReady =
    practiceUnlocked &&
    generation?.status === "completed" &&
    sameIdSet(acceptedIds, generation.accepted_unit_ids);
  const loading = lessonQuery.isPending || (lessonQuery.isSuccess && unitsQuery.isPending);
  const title =
    lessonQuery.data && lessonQuery.data.title.trim() !== "" ? lessonQuery.data.title : "Untitled Lesson";

  function toggleStage(stageId: StageId) {
    setExpansion((current) => {
      const next = { ...current, [stageId]: !current[stageId] };
      saveStageExpansion(id, next);
      return next;
    });
  }

  async function refreshUnits() {
    setSelection(null);
    await queryClient.invalidateQueries({ queryKey: ["learning-units", id] });
  }

  function jumpToUnit(unit: LearningUnit) {
    setHighlight({ start: unit.start, end: unit.end });
    setExpansion((current) => {
      const next = { ...current, source: true };
      saveStageExpansion(id, next);
      return next;
    });
    requestAnimationFrame(() => {
      document.getElementById("source-highlight")?.scrollIntoView({ block: "nearest" });
    });
  }

  return (
    <main className={styles.page}>
      <header className={styles.header}>
        <Link to="/">Lessons</Link>
        <h1>{lessonQuery.isSuccess ? title : "Lesson"}</h1>
        {loading ? <p className={styles.pending}>Loading…</p> : null}
      </header>
      <div className={styles.stageColumn} data-testid="stage-column">
        <StageSection
          label="Source"
          unlocked
          expanded={expansion.source}
          onToggle={() => toggleStage("source")}
        >
          {lessonQuery.isSuccess ? (
            <SourceStage
              source={lessonQuery.data.source}
              highlight={highlight}
              onSelectionChange={setSelection}
            />
          ) : null}
        </StageSection>
        <StageSection
          label="Learning Units"
          unlocked
          expanded={expansion["learning-units"]}
          onToggle={() => toggleStage("learning-units")}
        >
          {loading ? <p className={styles.pending}>Loading…</p> : null}
          {lessonQuery.isError ? (
            <p className={styles.alert} role="alert">
              {LOAD_ERROR} <Link to="/">Lessons</Link>
            </p>
          ) : null}
          {lessonQuery.isSuccess ? (
            <LearningUnitsStage
              lessonId={id}
              units={units}
              selection={selection}
              practiceOpen={false}
              onChanged={refreshUnits}
              onJump={jumpToUnit}
            />
          ) : null}
        </StageSection>
        <StageSection
          label="Generate Exercises"
          unlocked
          expanded={expansion["generate-exercises"]}
          onToggle={() => toggleStage("generate-exercises")}
        >
          <GenerateExercisesStage
            exerciseTypes={exerciseTypesQuery.data?.exercises ?? []}
            pending={generateMutation.isPending}
            outcome={generation}
            acceptedCount={acceptedIds.length}
            onGenerate={() => generateMutation.mutate()}
          />
        </StageSection>
        <StageSection
          label="Practice"
          unlocked={practiceUnlocked}
          expanded={expansion.practice}
          onToggle={() => toggleStage("practice")}
        >
          <PracticeStage enabled={practiceReady} />
        </StageSection>
        <StageSection label="Feedback" unlocked={false} expanded={expansion.feedback} onToggle={() => toggleStage("feedback")}>
          <FeedbackStage />
        </StageSection>
      </div>
    </main>
  );
}

function StageSection({
  label,
  unlocked,
  expanded,
  onToggle,
  children,
}: {
  label: string;
  unlocked: boolean;
  expanded: boolean;
  onToggle: () => void;
  children: ReactNode;
}) {
  const open = unlocked && expanded;
  const panelId = `stage-panel-${label.toLowerCase().replaceAll(" ", "-")}`;
  return (
    <div className={open ? styles.stageOpen : undefined}>
      <h2>
        <button
          type="button"
          className={styles.stageToggle}
          aria-expanded={open}
          aria-controls={panelId}
          disabled={!unlocked}
          onClick={onToggle}
        >
          {label}
        </button>
      </h2>
      {open ? (
        <div id={panelId} role="region" aria-label={label} className={styles.stagePanel}>
          {children}
        </div>
      ) : null}
    </div>
  );
}
