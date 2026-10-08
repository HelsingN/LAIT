import type { PracticeItemView } from "../../registries/renderers/types.ts";

export const STAGE_IDS = [
  "source",
  "learning-units",
  "generate-exercises",
  "practice",
  "feedback",
] as const;

export type StageId = (typeof STAGE_IDS)[number];

export type StageExpansion = Record<StageId, boolean>;

const DEFAULT_EXPANSION: StageExpansion = {
  source: true,
  "learning-units": true,
  "generate-exercises": false,
  practice: false,
  feedback: false,
};

export function stageStorageKey(lessonId: string): string {
  return `lait.lesson-stages.${lessonId}`;
}

export function loadStageExpansion(lessonId: string): StageExpansion {
  const raw = localStorage.getItem(stageStorageKey(lessonId));
  if (!raw) {
    return { ...DEFAULT_EXPANSION };
  }
  try {
    const parsed = JSON.parse(raw) as Partial<StageExpansion>;
    return { ...DEFAULT_EXPANSION, ...parsed };
  } catch {
    return { ...DEFAULT_EXPANSION };
  }
}

export function saveStageExpansion(lessonId: string, expansion: StageExpansion): void {
  localStorage.setItem(stageStorageKey(lessonId), JSON.stringify(expansion));
}

export function revealStorageKey(sessionId: string, position: number): string {
  return `lait.practice-reveal.${sessionId}.${position}`;
}

export function attemptStorageKey(sessionId: string, position: number): string {
  return `lait.practice-attempt.${sessionId}.${position}`;
}

export function practiceSessionStorageKey(lessonId: string): string {
  return `lait.practice-session.${lessonId}`;
}

export function loadOpenPracticeSessionId(lessonId: string): string | null {
  const stored = localStorage.getItem(practiceSessionStorageKey(lessonId));
  if (!stored) {
    return null;
  }
  return stored;
}

export function saveOpenPracticeSessionId(lessonId: string, sessionId: string): void {
  localStorage.setItem(practiceSessionStorageKey(lessonId), sessionId);
}

export function clearOpenPracticeSessionId(lessonId: string): void {
  localStorage.removeItem(practiceSessionStorageKey(lessonId));
}

export function isPracticeOpen(pendingStoredSession: boolean, sessionOpen: boolean): boolean {
  if (pendingStoredSession) {
    return true;
  }
  return sessionOpen;
}

export type FeedbackBinding = {
  version: 1;
  session_id: string;
  attempt_id: string;
  item: PracticeItemView;
};

export type PendingFeedback = FeedbackBinding & { response_cursor: number };

export function pendingFeedbackKey(lessonId: string, sessionId: string): string {
  return `lait.practice-feedback.${lessonId}.${sessionId}`;
}

function record(raw: string | null): FeedbackBinding | null {
  try {
    const value = JSON.parse(raw ?? "null");
    const item = value?.item;
    if (value?.version !== 1 || typeof value.session_id !== "string" || typeof value.attempt_id !== "string" || !value.attempt_id || !item) return null;
    for (const key of ["mode", "learning_unit_id", "exercise_type", "target_text", "sentence"]) {
      if (typeof item[key] !== "string") return null;
    }
    for (const key of ["position", "start", "end"]) {
      if (!Number.isSafeInteger(item[key]) || item[key] < 0) return null;
    }
    if (item.end < item.start || !Array.isArray(item.segments) || !item.segments.every((segment: { kind?: unknown; text?: unknown } | null) => segment && typeof segment.kind === "string" && typeof segment.text === "string") || !Array.isArray(item.chip_unit_ids) || !item.chip_unit_ids.every((id: unknown) => typeof id === "string")) return null;
    return value;
  } catch {
    return null;
  }
}

export function samePracticeItem(left: PracticeItemView, right: PracticeItemView): boolean {
  return left.position === right.position && left.learning_unit_id === right.learning_unit_id && left.mode === right.mode && left.exercise_type === right.exercise_type
    && left.start === right.start && left.end === right.end && left.target_text === right.target_text && left.sentence === right.sentence
    && JSON.stringify(left.segments) === JSON.stringify(right.segments) && JSON.stringify(left.chip_unit_ids) === JSON.stringify(right.chip_unit_ids);
}

export function loadPendingFeedback(lessonId: string, sessionId: string): PendingFeedback | null {
  const parsed = record(localStorage.getItem(pendingFeedbackKey(lessonId, sessionId))) as PendingFeedback | null;
  return parsed?.session_id === sessionId && Number.isSafeInteger(parsed.response_cursor) && parsed.response_cursor >= 0 ? parsed : null;
}

export function savePendingFeedback(lessonId: string, pending: PendingFeedback): void {
  localStorage.setItem(pendingFeedbackKey(lessonId, pending.session_id), JSON.stringify(pending));
}

export function clearPendingFeedback(lessonId: string, sessionId: string): void {
  localStorage.removeItem(pendingFeedbackKey(lessonId, sessionId));
}

export function loadReveal(binding: FeedbackBinding): boolean {
  const saved = record(localStorage.getItem(revealStorageKey(binding.session_id, binding.item.position)));
  return saved !== null && saved.session_id === binding.session_id && saved.attempt_id === binding.attempt_id && samePracticeItem(saved.item, binding.item);
}

export function saveReveal(binding: FeedbackBinding): void {
  localStorage.setItem(revealStorageKey(binding.session_id, binding.item.position), JSON.stringify(binding));
}
