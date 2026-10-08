import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router";

import { listLessons, type Lesson } from "./lessonApi.ts";
import { CreateLessonForm } from "./CreateLessonForm.tsx";
import styles from "./LessonListPage.module.css";

function lessonTitle(title: string): string {
  return title.trim() === "" ? "Untitled Lesson" : title;
}

export function LessonListPage() {
  const lessonsQuery = useQuery({
    queryKey: ["lessons"],
    queryFn: listLessons,
  });

  return (
    <main className={styles.page}>
      <header className={styles.header}>
        <h1>Lessons</h1>
        {lessonsQuery.isPending ? <p className={styles.pending}>Loading…</p> : null}
      </header>

      {lessonsQuery.isError ? (
        <p role="alert">
          Could not load this lesson. Return to the lesson list and open it again.{" "}
          <Link to="/">Lessons</Link>
        </p>
      ) : null}

      {lessonsQuery.isSuccess && lessonsQuery.data.lessons.length === 0 ? (
        <section className={styles.empty}>
          <h2>No lessons yet</h2>
          <p>
            Paste a short English text to create your first lesson, then mark phrases to practice.
          </p>
        </section>
      ) : null}

      <CreateLessonForm />

      {lessonsQuery.isSuccess && lessonsQuery.data.lessons.length > 0 ? (
        <ul className={styles.list}>
          {lessonsQuery.data.lessons.map((lesson: Lesson) => {
            const titleText = lessonTitle(lesson.title);
            return (
              <li key={lesson.id} className={styles.row}>
                <span className={styles.rowTitle} title={titleText}>
                  {titleText}
                </span>
                <Link to={`/lessons/${lesson.id}`}>Open</Link>
              </li>
            );
          })}
        </ul>
      ) : null}
    </main>
  );
}
