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
