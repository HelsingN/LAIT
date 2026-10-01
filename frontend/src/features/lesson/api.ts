export type Lesson = {
  id: string;
  title: string;
  source: string;
  created_at: string;
};

export type LessonList = {
  lessons: Lesson[];
};

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
