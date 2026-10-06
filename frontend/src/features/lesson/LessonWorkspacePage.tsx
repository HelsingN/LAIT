import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useEffect, useRef, useState, type ReactNode } from "react";
import { createPortal } from "react-dom";
import { Link, useParams } from "react-router";

import { FocusPracticeMode } from "./FocusPracticeMode.tsx";
import {
  finishPractice,
  generateExercises,
  getLesson,
  getPractice,
  latestCompletedExercises,
  listLearnerExerciseTypes,
  listLearningUnits,
  listLessonAttempts,
  requestStatus,
  startOverPractice,
  startPractice,
  submitAttempt,
  type AttemptResult,
  type GenerationResult,
  type LearningUnit,
  type LessonAttempt,
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
  clearOpenPracticeSessionId,
  isPracticeOpen,
  loadOpenPracticeSessionId,
  loadStageExpansion,
  saveOpenPracticeSessionId,
  saveStageExpansion,
  type StageExpansion,
  type StageId,
} from "./stageState.ts";

const LOAD_ERROR = "Could not load this lesson. Return to the lesson list and open it again.";
const FINISH_ERROR = "Could not finish this practice. Try again.";
const HISTORY_ERROR = "Could not load practice history. Try again.";

function sameIdSet(left: string[], right: string[]): boolean {
  if (left.length !== right.length) {
    return false;
  }
  const sortedLeft = [...left].sort();
  const sortedRight = [...right].sort();
  return sortedLeft.every((id, index) => id === sortedRight[index]);
}

const WIDE_LAYOUT_QUERY = "(min-width: 960px)";
const WIDE_SHORT_QUERY = "(max-height: 693px)";
const NARROW_SHORT_QUERY = "(max-height: 837px)";

function feedbackCoversPreparation(): boolean {
  if (typeof window.matchMedia !== "function") {
    return false;
  }
  const wide = window.matchMedia(WIDE_LAYOUT_QUERY).matches;
  return window.matchMedia(wide ? WIDE_SHORT_QUERY : NARROW_SHORT_QUERY).matches;
}

function useShortFeedbackCover(): boolean {
  const [matches, setMatches] = useState(feedbackCoversPreparation);
  useEffect(() => {
    if (typeof window.matchMedia !== "function") {
      return;
    }
    const queries = [WIDE_LAYOUT_QUERY, WIDE_SHORT_QUERY, NARROW_SHORT_QUERY].map((query) =>
      window.matchMedia(query),
    );
    const onChange = () => setMatches(feedbackCoversPreparation());
    onChange();
    for (const media of queries) {
      media.addEventListener("change", onChange);
    }
    return () => {
      for (const media of queries) {
        media.removeEventListener("change", onChange);
      }
    };
  }, []);
  return matches;
}

export function LessonWorkspacePage() {
  const { id = "" } = useParams();
  const queryClient = useQueryClient();
  const [expansion, setExpansion] = useState<StageExpansion>(() => ({
    ...loadStageExpansion(id),
    feedback: false,
  }));
  const [selection, setSelection] = useState<CodePointRange | null>(null);
  const [prepSlot, setPrepSlot] = useState<HTMLDivElement | null>(null);
  const shortWindow = useShortFeedbackCover();
  const [highlight, setHighlight] = useState<CodePointRange | null>(null);
  const [generation, setGeneration] = useState<GenerationResult | null>(null);
  const [practiceUnlocked, setPracticeUnlocked] = useState(false);
  const [focused, setFocused] = useState(false);
  const [session, setSession] = useState<PracticeView | null>(null);
  const [feedback, setFeedback] = useState<AttemptResult | null>(null);
  const [attempts, setAttempts] = useState<LessonAttempt[]>([]);
  const [feedbackUnlocked, setFeedbackUnlocked] = useState(false);
  const [currentPassSessionId, setCurrentPassSessionId] = useState<string | null>(null);
  const [finishError, setFinishError] = useState<string | null>(null);
  const [finishRetryId, setFinishRetryId] = useState<string | null>(null);
  const [historyError, setHistoryError] = useState<string | null>(null);
  const [historyRetryId, setHistoryRetryId] = useState<string | null>(null);
  const hydratedFor = useRef<string | null>(null);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [submitPending, setSubmitPending] = useState(false);
  const [startError, setStartError] = useState<string | null>(null);
  const [pendingStoredSession, setPendingStoredSession] = useState(
    () => loadOpenPracticeSessionId(id) !== null,
  );
  const [startPending, setStartPending] = useState(false);
  const startPendingRef = useRef(false);

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

  useEffect(() => {
    const sessionId = loadOpenPracticeSessionId(id);
    if (!sessionId) {
      setPendingStoredSession(false);
      return;
    }
    let cancelled = false;
    setPendingStoredSession(true);
    void getPractice(sessionId)
      .then((view) => {
        if (cancelled) {
          return;
        }
        if (view.open && view.current === null) {
          void closeSession(sessionId, false);
          return;
        }
        setPendingStoredSession(false);
        if (view.open) {
          setSession(view);
          setFocused(true);
          return;
        }
        clearOpenPracticeSessionId(id);
      })
      .catch(() => {
        if (cancelled) {
          return;
        }
        setPendingStoredSession(false);
        clearOpenPracticeSessionId(id);
      });
    return () => {
      cancelled = true;
    };
    // closeSession is recreated each render and only this lesson id is in scope.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  useEffect(() => {
    if (id === "" || !lessonQuery.isSuccess || !unitsQuery.isSuccess) {
      return;
    }
    if (hydratedFor.current === id) {
      return;
    }
    hydratedFor.current = id;
    const lessonId = id;
    void (async () => {
      try {
        const latest = await latestCompletedExercises(lessonId);
        if (hydratedFor.current === lessonId && latest.restorable && latest.generation_id) {
          setGeneration({
            id: latest.generation_id,
            lesson_id: lessonId,
            status: "completed",
            accepted_unit_ids: [...latest.accepted_unit_ids],
            definition_count: 0,
          });
          setPracticeUnlocked(true);
          setExpansion((current) => {
            const next = { ...current, practice: true };
            saveStageExpansion(lessonId, next);
            return next;
          });
        }
      } catch {
        // A failed read leaves Practice locked. Load never calls exercise.generate.
      }
      try {
        const listed = await listLessonAttempts(lessonId);
        if (hydratedFor.current !== lessonId || listed.length === 0) {
          return;
        }
        setAttempts(listed);
        setFeedbackUnlocked(true);
      } catch {
        // History stays closed until a later successful list.
      }
    })();
  }, [id, lessonQuery.isSuccess, unitsQuery.isSuccess]);

  const units = unitsQuery.data?.learning_units ?? [];
  const acceptedIds = units.filter((unit) => unit.status === "accepted").map((unit) => unit.id);
  const generationMatches =
    generation?.status === "completed" && sameIdSet(acceptedIds, generation.accepted_unit_ids);
  const practiceReady = practiceUnlocked && generationMatches;
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
    if (startPendingRef.current) {
      return;
    }
    startPendingRef.current = true;
    setStartPending(true);
    setStartError(null);
    try {
      const view = await startPractice(id);
      saveOpenPracticeSessionId(id, view.session_id);
      setSession(view);
      setFeedback(null);
      setSubmitError(null);
      setFocused(true);
    } catch {
      setStartError("Could not start practice. Try again.");
    } finally {
      startPendingRef.current = false;
      setStartPending(false);
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
    } catch {
      setSubmitError("Could not submit. Try again.");
    } finally {
      setSubmitPending(false);
    }
  }

  async function revealPass(sessionId: string): Promise<void> {
    setCurrentPassSessionId(sessionId);
    setFeedbackUnlocked(true);
    setExpansion((current) => {
      const next = { ...current, feedback: true };
      saveStageExpansion(id, next);
      return next;
    });
    try {
      const listed = await listLessonAttempts(id);
      setAttempts(listed);
      setHistoryError(null);
      setHistoryRetryId(null);
    } catch {
      setAttempts([]);
      setHistoryError(HISTORY_ERROR);
      setHistoryRetryId(sessionId);
    }
  }

  async function closeSession(sessionId: string, stayOnFailure: boolean): Promise<void> {
    try {
      await finishPractice(sessionId);
    } catch (error) {
      if (requestStatus(error) === 404) {
        clearOpenPracticeSessionId(id);
        setFocused(false);
        setSession(null);
        setFeedback(null);
        setSubmitError(null);
        setPendingStoredSession(false);
        setFinishError(null);
        setFinishRetryId(null);
        await revealPass(sessionId);
        return;
      }
      setFinishError(FINISH_ERROR);
      setFinishRetryId(sessionId);
      setHistoryError(null);
      setPendingStoredSession(true);
      if (!stayOnFailure) {
        setFocused(false);
        setSession(null);
      }
      return;
    }
    clearOpenPracticeSessionId(id);
    setFocused(false);
    setSession(null);
    setFeedback(null);
    setSubmitError(null);
    setPendingStoredSession(false);
    setFinishError(null);
    setFinishRetryId(null);
    await revealPass(sessionId);
  }

  async function retryFinish() {
    if (!finishRetryId) {
      return;
    }
    await closeSession(finishRetryId, focused);
  }

  async function retryHistory() {
    if (!historyRetryId) {
      return;
    }
    await revealPass(historyRetryId);
  }

  async function handleContinue() {
    if (!session) {
      return;
    }
    const view = await getPractice(session.session_id);
    if (view.open && view.current === null) {
      await closeSession(view.session_id, true);
      return;
    }
    setSession(view);
    setFeedback(null);
    setSubmitError(null);
  }

  async function handleExit() {
    if (!session) {
      return;
    }
    await closeSession(session.session_id, true);
  }

  async function handleStartOver() {
    if (!session) {
      return;
    }
    const view = await startOverPractice(session.session_id);
    saveOpenPracticeSessionId(id, view.session_id);
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
      document.getElementById("source-highlight")?.scrollIntoView?.({ block: "nearest" });
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
        {finishError ? (
          <>
            <p className={styles.alert} role="alert">
              {finishError}
            </p>
            <button type="button" onClick={() => void retryFinish()}>
              Try again
            </button>
          </>
        ) : null}
        <FocusPracticeMode
          sessionId={session.session_id}
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
    <main className={`${styles.page} ${styles.workspace}`}>
      <header className={styles.header}>
        <Link to="/">Lessons</Link>
        <h1>{lessonQuery.isSuccess ? title : "Lesson"}</h1>
        {loading ? <p className={styles.pending}>Loading…</p> : null}
        {finishError ? (
          <>
            <p className={styles.alert} role="alert">
              {finishError}
            </p>
            <button type="button" onClick={() => void retryFinish()}>
              Try again
            </button>
          </>
        ) : null}
      </header>
      <div className={styles.stageColumn} data-testid="stage-column">
        <div className={styles.prepSlot} data-testid="prep-slot" ref={setPrepSlot}>
          <section className={styles.preparation} aria-label="Preparation" inert={shortWindow && expansion.feedback && feedbackUnlocked}>
          <StageSection
            label="Source"
            pane
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
            pane
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
                practiceOpen={isPracticeOpen(pendingStoredSession, session?.open === true)}
                onChanged={refreshUnits}
                onJump={jumpToUnit}
              />
            ) : null}
          </StageSection>
          </section>
        </div>
        <div className={styles.actions}>
          <StageSection
            label="Exercises"
            allowShrink
            unlocked
            expanded={expansion["generate-exercises"]}
            onToggle={() => toggleStage("generate-exercises")}
          >
            <GenerateExercisesStage
              exerciseTypes={exerciseTypesQuery.data?.exercises ?? []}
              pending={generateMutation.isPending}
              outcome={generation}
              acceptedCount={acceptedIds.length}
              ready={generationMatches}
              onGenerate={() => generateMutation.mutate()}
            />
          </StageSection>
          <StageSection
            label="Practice"
            unlocked={practiceUnlocked}
            expanded={expansion.practice}
            onToggle={() => toggleStage("practice")}
          >
            <PracticeStage
              enabled={practiceReady}
              pending={startPending}
              onStart={() => void handleStart()}
            />
            {startError ? (
              <p className={styles.alert} role="alert">
                {startError}
              </p>
            ) : null}
          </StageSection>
          <StageSection
            label="Feedback"
            scrollable
            panelHost={shortWindow && expansion.feedback && feedbackUnlocked ? prepSlot : null}
            unlocked={feedbackUnlocked}
            expanded={expansion.feedback}
            onToggle={() => toggleStage("feedback")}
          >
            {historyError ? (
              <>
                <p className={styles.alert} role="alert">
                  {historyError}
                </p>
                <button type="button" onClick={() => void retryHistory()}>
                  Try again
                </button>
              </>
            ) : (
              <FeedbackStage
                attempts={attempts}
                currentSessionId={currentPassSessionId}
                onJump={(attempt) => jumpToSpan(attempt.span_start, attempt.span_end)}
              />
            )}
          </StageSection>
        </div>
      </div>
    </main>
  );
}

function StageSection({
  label,
  unlocked,
  expanded,
  onToggle,
  pane = false,
  scrollable = false,
  allowShrink = false,
  panelHost = null,
  children,
}: {
  label: string;
  unlocked: boolean;
  expanded: boolean;
  onToggle: () => void;
  pane?: boolean;
  scrollable?: boolean;
  allowShrink?: boolean;
  panelHost?: HTMLElement | null;
  children: ReactNode;
}) {
  const open = unlocked && expanded;
  const panelId = `stage-panel-${label.toLowerCase().replaceAll(" ", "-")}`;
  const panelClass = scrollable && panelHost ? styles.feedbackCover : scrollable ? styles.feedbackPanel : pane ? styles.panePanel : styles.stagePanel;
  const sectionClass = [
    pane
      ? styles.pane
      : scrollable && open && !panelHost
        ? styles.feedbackStage
        : open
          ? styles.stageOpen
          : undefined,
    allowShrink ? styles.allowShrink : undefined,
  ]
    .filter(Boolean)
    .join(" ");
  const panel = open ? (
    <div id={panelId} role="region" aria-label={label} className={panelClass}>
      {children}
    </div>
  ) : null;
  return (
    <div className={sectionClass || undefined}>
      <h2>
        <button
          type="button"
          className={styles.stageToggle}
          aria-label={label}
          aria-expanded={open}
          aria-controls={panelId}
          disabled={!unlocked}
          onClick={onToggle}
        >
          <span className={styles.chevron} aria-hidden="true">
            {open ? "▾" : "▸"}
          </span>
          {label}
        </button>
      </h2>
      {panelHost && panel ? createPortal(panel, panelHost) : panel}
    </div>
  );
}
