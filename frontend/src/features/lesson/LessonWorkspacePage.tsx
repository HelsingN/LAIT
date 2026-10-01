import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState, type ReactNode } from "react";
import { Link, useParams } from "react-router";

import { FocusPracticeMode } from "./FocusPracticeMode.tsx";
import {
  finishPractice,
  generateExercises,
  getLesson,
  getPractice,
  listLearnerExerciseTypes,
  listLearningUnits,
  startOverPractice,
  startPractice,
  submitAttempt,
  type AttemptResult,
  type GenerationResult,
  type LearningUnit,
  type PracticeView,
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
  const [focused, setFocused] = useState(false);
  const [session, setSession] = useState<PracticeView | null>(null);
  const [feedback, setFeedback] = useState<AttemptResult | null>(null);
  const [attempts, setAttempts] = useState<AttemptResult[]>([]);
  const [feedbackUnlocked, setFeedbackUnlocked] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [submitPending, setSubmitPending] = useState(false);
  const [startError, setStartError] = useState<string | null>(null);

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

  async function handleStart() {
    setStartError(null);
    try {
      const view = await startPractice(id);
      setSession(view);
      setFeedback(null);
      setSubmitError(null);
      setFocused(true);
    } catch {
      setStartError("Could not start practice. Try again.");
    }
  }

  async function handleSubmit(answer: { text: string; submittedUnitId: string | null }) {
    if (!session?.current) {
      return;
    }
    setSubmitPending(true);
    setSubmitError(null);
    try {
      const result = await submitAttempt(session.session_id, {
        kind: session.current.mode,
        text: answer.text,
        submittedUnitId: answer.submittedUnitId,
        targetLearningUnitId: session.current.learning_unit_id,
      });
      setFeedback(result);
      setAttempts((current) => [...current, result]);
    } catch {
      setSubmitError("Could not submit. Try again.");
    } finally {
      setSubmitPending(false);
    }
  }

  async function handleContinue() {
    if (!session) {
      return;
    }
    const view = await getPractice(session.session_id);
    setSession(view);
    setFeedback(null);
    setSubmitError(null);
  }

  async function handleExit() {
    if (!session) {
      return;
    }
    await finishPractice(session.session_id);
    setFocused(false);
    setFeedbackUnlocked(true);
    setSession(null);
    setFeedback(null);
    setSubmitError(null);
    setExpansion((current) => {
      const next = { ...current, feedback: true };
      saveStageExpansion(id, next);
      return next;
    });
  }

  async function handleStartOver() {
    if (!session) {
      return;
    }
    const view = await startOverPractice(session.session_id);
    setSession(view);
    setFeedback(null);
    setSubmitError(null);
  }

  function jumpToSpan(start: number, end: number) {
    setHighlight({ start, end });
    setExpansion((current) => {
      const next = { ...current, source: true };
      saveStageExpansion(id, next);
      return next;
    });
    requestAnimationFrame(() => {
      document.getElementById("source-highlight")?.scrollIntoView({ block: "nearest" });
    });
  }

  function jumpToUnit(unit: LearningUnit) {
    jumpToSpan(unit.start, unit.end);
  }

  const learnerExerciseTypes = (exerciseTypesQuery.data?.exercises ?? []).map((row) => row.exercise_type);
  const focusItem = session?.current ?? null;

  if (focused && session) {
    return (
      <main className={styles.page}>
        <FocusPracticeMode
          item={focusItem}
          units={units.map((unit) => ({ id: unit.id, text: unit.text }))}
          learnerExerciseTypes={learnerExerciseTypes}
          pending={submitPending}
          submitError={submitError}
          feedback={feedback}
          onSubmit={(answer) => void handleSubmit(answer)}
          onContinue={() => void handleContinue()}
          onExit={() => void handleExit()}
          onStartOver={() => void handleStartOver()}
        />
      </main>
    );
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
              practiceOpen={focused}
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
          <PracticeStage enabled={practiceReady} onStart={() => void handleStart()} />
          {startError ? (
            <p className={styles.alert} role="alert">
              {startError}
            </p>
          ) : null}
        </StageSection>
        <StageSection
          label="Feedback"
          unlocked={feedbackUnlocked}
          expanded={expansion.feedback}
          onToggle={() => toggleStage("feedback")}
        >
          <FeedbackStage
            attempts={attempts}
            onJump={(attempt) => jumpToSpan(attempt.span_start, attempt.span_end)}
          />
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
