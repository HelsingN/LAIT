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
  source: false,
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
