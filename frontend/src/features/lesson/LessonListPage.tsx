import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState, type FormEvent } from "react";
import { Link } from "react-router";

import { createLesson, listLessons, type Lesson } from "./api.ts";
import styles from "./LessonListPage.module.css";
import { suggestTitle } from "./suggestTitle.ts";

function lessonTitle(title: string): string {
  return title.trim() === "" ? "Untitled Lesson" : title;
}

export function LessonListPage() {
  const queryClient = useQueryClient();
  const lessonsQuery = useQuery({
    queryKey: ["lessons"],
    queryFn: listLessons,
  });
  const [source, setSource] = useState("");
  const [title, setTitle] = useState("");
  const [titleTouched, setTitleTouched] = useState(false);
  const shownTitle = titleTouched ? title : suggestTitle(source);

  const createMutation = useMutation({
    mutationFn: createLesson,
    onSuccess: async () => {
      setSource("");
      setTitle("");
      setTitleTouched(false);
      await queryClient.invalidateQueries({ queryKey: ["lessons"] });
    },
  });

  function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    createMutation.mutate({
      source,
      title: titleTouched ? title : shownTitle,
    });
  }

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

      <form className={styles.form} onSubmit={onSubmit}>
        <label className={styles.field}>
          <span>Title</span>
          <input
            className={styles.titleInput}
            value={shownTitle}
            maxLength={200}
            onChange={(event) => {
              setTitleTouched(true);
              setTitle(event.target.value);
            }}
          />
        </label>
        <label className={styles.field}>
          <span>Source</span>
          <textarea
            className={styles.sourceInput}
            value={source}
            onChange={(event) => setSource(event.target.value)}
            required
          />
        </label>
        {createMutation.isError ? (
          <p role="alert">
            Could not create the lesson. Check the pasted text and try Create Lesson again.
          </p>
        ) : null}
        <button
          className={styles.primary}
          type="submit"
          disabled={createMutation.isPending || source.trim() === ""}
        >
          {createMutation.isPending ? "Creating…" : "Create Lesson"}
        </button>
      </form>

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
