import {
  attemptListForLesson,
  exerciseGenerate,
  exerciseLatestCompleted,
  exerciseRegistryListVisibleFor,
  exerciseSubmitAttempt,
  learningUnitAccept,
  learningUnitAdd,
  learningUnitList,
  learningUnitRemove,
  lessonCreate,
  lessonGet,
  lessonList,
  practiceAdvance,
  practiceFinish,
  practiceGet,
  practiceStart,
  practiceStartOver,
  type AttemptListItemResponse,
  type CurrentItemResponse,
  type ExerciseRegistryItem,
  type ExerciseRegistryResponse,
  type GenerationResponse,
  type LatestCompletedResponse,
  type LearningUnitResponse,
  type LessonResponse,
  type PracticeResponse,
  type SegmentResponse,
  type SubmitResponse,
} from "../../api/generated/index.ts";

export type Lesson = LessonResponse;

export type LessonList = {
  lessons: Lesson[];
};

export type LearningUnit = Omit<LearningUnitResponse, "removed_at"> & {
  removed_at: string | null;
};

export type LearningUnitList = {
  learning_units: LearningUnit[];
};

export type LearnerExerciseType = ExerciseRegistryItem;

export type LearnerExerciseList = ExerciseRegistryResponse;

export type GenerationResult = GenerationResponse;

export class LearningUnitRequestError extends Error {
  readonly kind: "overlap" | "frozen";

  constructor(kind: "overlap" | "frozen") {
    super(kind);
    this.name = "LearningUnitRequestError";
    this.kind = kind;
  }
}

type SdkPayload<T> = {
  data?: T;
  response?: Response;
};

async function readData<T>(pending: Promise<SdkPayload<T>>): Promise<T> {
  const result = await pending;
  if (result.data === undefined) {
    const status = result.response?.status ?? 0;
    const error = new Error(`Request failed with status ${status}`) as Error & { status: number };
    error.status = status;
    throw error;
  }
  return result.data;
}

export function requestStatus(error: unknown): number | null {
  if (typeof error === "object" && error !== null && "status" in error) {
    const status = (error as { status?: unknown }).status;
    return typeof status === "number" ? status : null;
  }
  return null;
}

function asUnit(unit: LearningUnitResponse): LearningUnit {
  return {
    ...unit,
    removed_at: unit.removed_at ?? null,
  };
}

export function listLessons(): Promise<LessonList> {
  return readData(lessonList());
}

export function createLesson(input: { source: string; title: string }): Promise<Lesson> {
  return readData(
    lessonCreate({
      body: input,
    }),
  );
}

export function getLesson(lessonId: string): Promise<Lesson> {
  return readData(
    lessonGet({
      path: { lesson_id: lessonId },
    }),
  );
}

export async function listLearningUnits(lessonId: string): Promise<LearningUnitList> {
  const body = await readData(
    learningUnitList({
      path: { lesson_id: lessonId },
    }),
  );
  return {
    learning_units: body.learning_units.map(asUnit),
  };
}

export async function addLearningUnit(
  lessonId: string,
  start: number,
  end: number,
): Promise<LearningUnit> {
  const result = await learningUnitAdd({
    path: { lesson_id: lessonId },
    body: { start, end },
  });
  if (result.response?.status === 422) {
    throw new LearningUnitRequestError("overlap");
  }
  if (result.response?.status === 409) {
    throw new LearningUnitRequestError("frozen");
  }
  if (result.data === undefined) {
    throw new Error(`Request failed with status ${result.response?.status ?? 0}`);
  }
  return asUnit(result.data);
}

export async function acceptLearningUnit(lessonId: string, unitId: string): Promise<LearningUnit> {
  const result = await learningUnitAccept({
    path: { lesson_id: lessonId, unit_id: unitId },
  });
  if (result.response?.status === 409) {
    throw new LearningUnitRequestError("frozen");
  }
  if (result.data === undefined) {
    throw new Error(`Request failed with status ${result.response?.status ?? 0}`);
  }
  return asUnit(result.data);
}

export async function removeLearningUnit(lessonId: string, unitId: string): Promise<LearningUnit> {
  const result = await learningUnitRemove({
    path: { lesson_id: lessonId, unit_id: unitId },
  });
  if (result.response?.status === 409) {
    throw new LearningUnitRequestError("frozen");
  }
  if (result.data === undefined) {
    throw new Error(`Request failed with status ${result.response?.status ?? 0}`);
  }
  return asUnit(result.data);
}

export function listLearnerExerciseTypes(): Promise<LearnerExerciseList> {
  return readData(
    exerciseRegistryListVisibleFor({
      query: { visibility: "learner" },
    }),
  );
}

export function generateExercises(lessonId: string): Promise<GenerationResult> {
  return readData(
    exerciseGenerate({
      path: { lesson_id: lessonId },
    }),
  );
}

export type LatestCompleted = LatestCompletedResponse;

export type LessonAttempt = AttemptListItemResponse & {
  pass_item_count?: number;
};

export function latestCompletedExercises(lessonId: string): Promise<LatestCompleted> {
  return readData(
    exerciseLatestCompleted({
      path: { lesson_id: lessonId },
    }),
  );
}

export function listLessonAttempts(lessonId: string): Promise<LessonAttempt[]> {
  return readData(
    attemptListForLesson({
      path: { lesson_id: lessonId },
    }),
  ).then((body) => body.attempts);
}

export type PracticeSegment = SegmentResponse;

export type PracticeItem = CurrentItemResponse;

export type PracticeView = PracticeResponse;

export type AttemptResult = SubmitResponse;

export type AttemptSubmission = {
  kind: string;
  text: string;
  submittedUnitId: string | null;
  targetLearningUnitId: string;
};

export function startPractice(lessonId: string): Promise<PracticeView> {
  return readData(
    practiceStart({
      body: { lesson_id: lessonId },
    }),
  );
}

export function getPractice(sessionId: string): Promise<PracticeView> {
  return readData(
    practiceGet({
      path: { session_id: sessionId },
    }),
  );
}

export function submitAttempt(
  sessionId: string,
  submission: AttemptSubmission,
): Promise<AttemptResult> {
  const body: {
    kind: string;
    text: string;
    target_learning_unit_id: string;
    submitted_unit_id?: string;
  } = {
    kind: submission.kind,
    text: submission.text,
    target_learning_unit_id: submission.targetLearningUnitId,
  };
  if (submission.submittedUnitId) {
    body.submitted_unit_id = submission.submittedUnitId;
  }
  return readData(
    exerciseSubmitAttempt({
      path: { session_id: sessionId },
      body,
    }),
  );
}

export function finishPractice(sessionId: string): Promise<PracticeView> {
  return readData(
    practiceFinish({
      path: { session_id: sessionId },
    }),
  );
}

export function startOverPractice(sessionId: string): Promise<PracticeView> {
  return readData(
    practiceStartOver({
      path: { session_id: sessionId },
    }),
  );
}

export function advancePractice(sessionId: string, position: number): Promise<PracticeView> {
  return readData(
    practiceAdvance({
      path: { session_id: sessionId },
      body: { position },
    }),
  );
}
