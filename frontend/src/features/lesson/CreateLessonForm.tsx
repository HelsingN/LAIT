import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useState, type FormEvent } from "react";

import { createLesson } from "./lessonApi.ts";
import styles from "./LessonListPage.module.css";
import { suggestTitle } from "./suggestTitle.ts";

export function CreateLessonForm() {
  const queryClient = useQueryClient();
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
      <button className={styles.primary} type="submit" disabled={createMutation.isPending || source.trim() === ""}>
        {createMutation.isPending ? "Creating…" : "Create Lesson"}
      </button>
    </form>
  );
}
