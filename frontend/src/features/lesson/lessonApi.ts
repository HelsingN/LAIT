export type Lesson = {
  id: string;
  title: string;
  source: string;
  created_at: string;
};

export type LessonList = {
  lessons: Lesson[];
};

export type LearningUnit = {
  id: string;
  lesson_id: string;
  start: number;
  end: number;
  text: string;
  status: string;
  created_at: string;
  removed_at: string | null;
};

export type LearningUnitList = {
  learning_units: LearningUnit[];
};

export type LearnerExerciseType = {
  exercise_type: string;
  visibility: string;
  module_id: string;
};

export type LearnerExerciseList = {
  exercises: LearnerExerciseType[];
};

export type GenerationResult = {
  id: string;
  lesson_id: string;
  status: string;
  accepted_unit_ids: string[];
  definition_count: number;
};

export class LearningUnitRequestError extends Error {
  readonly kind: "overlap" | "frozen";

  constructor(kind: "overlap" | "frozen") {
    super(kind);
    this.name = "LearningUnitRequestError";
    this.kind = kind;
  }
}

async function readJson<T>(response: Response): Promise<T> {
  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }
  return (await response.json()) as T;
}

export function listLessons(): Promise<LessonList> {
  return fetch("/api/lessons").then((response) => readJson<LessonList>(response));
}

export function createLesson(input: { source: string; title: string }): Promise<Lesson> {
  return fetch("/api/lessons", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(input),
  }).then((response) => readJson<Lesson>(response));
}

export function getLesson(lessonId: string): Promise<Lesson> {
  return fetch(`/api/lessons/${encodeURIComponent(lessonId)}`).then((response) =>
    readJson<Lesson>(response),
  );
}

export function listLearningUnits(lessonId: string): Promise<LearningUnitList> {
  return fetch(`/api/lessons/${encodeURIComponent(lessonId)}/learning-units`).then((response) =>
    readJson<LearningUnitList>(response),
  );
}

export async function addLearningUnit(
  lessonId: string,
  start: number,
  end: number,
): Promise<LearningUnit> {
  const response = await fetch(`/api/lessons/${encodeURIComponent(lessonId)}/learning-units`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ start, end }),
  });
  if (response.status === 422) {
    throw new LearningUnitRequestError("overlap");
  }
  if (response.status === 409) {
    throw new LearningUnitRequestError("frozen");
  }
  return readJson<LearningUnit>(response);
}

export async function acceptLearningUnit(lessonId: string, unitId: string): Promise<LearningUnit> {
  const response = await fetch(
    `/api/lessons/${encodeURIComponent(lessonId)}/learning-units/${encodeURIComponent(unitId)}/accept`,
    { method: "POST" },
  );
  if (response.status === 409) {
    throw new LearningUnitRequestError("frozen");
  }
  return readJson<LearningUnit>(response);
}

export async function removeLearningUnit(lessonId: string, unitId: string): Promise<LearningUnit> {
  const response = await fetch(
    `/api/lessons/${encodeURIComponent(lessonId)}/learning-units/${encodeURIComponent(unitId)}/remove`,
    { method: "POST" },
  );
  if (response.status === 409) {
    throw new LearningUnitRequestError("frozen");
  }
  return readJson<LearningUnit>(response);
}

export function listLearnerExerciseTypes(): Promise<LearnerExerciseList> {
  return fetch("/api/exercise-registry?visibility=learner").then((response) =>
    readJson<LearnerExerciseList>(response),
  );
}

export function generateExercises(lessonId: string): Promise<GenerationResult> {
  return fetch(`/api/lessons/${encodeURIComponent(lessonId)}/exercises/generate`, {
    method: "POST",
  }).then((response) => readJson<GenerationResult>(response));
}
