import { useQuery } from "@tanstack/react-query";
import { Link, useParams } from "react-router";

import { getLesson } from "./api.ts";
import styles from "./LessonWorkspacePage.module.css";

export function LessonWorkspacePage() {
  const { id = "" } = useParams();
  const lessonQuery = useQuery({
    queryKey: ["lesson", id],
    queryFn: () => getLesson(id),
    enabled: id !== "",
  });

  if (lessonQuery.isPending) {
    return (
      <main className={styles.page}>
        <p>Loading…</p>
      </main>
    );
  }

  if (lessonQuery.isError || !lessonQuery.data) {
    return (
      <main className={styles.page}>
        <p role="alert">
          Could not load this lesson. Return to the lesson list and open it again.
        </p>
        <Link to="/">Lessons</Link>
      </main>
    );
  }

  const lesson = lessonQuery.data;
  const title = lesson.title.trim() === "" ? "Untitled Lesson" : lesson.title;

  return (
    <main className={styles.page}>
      <p>
        <Link to="/">Lessons</Link>
      </p>
      <h1>{title}</h1>
      <pre className={styles.source}>{lesson.source}</pre>
    </main>
  );
}
