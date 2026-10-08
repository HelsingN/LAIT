import { selectedCodePointRange, type CodePointRange } from "../selectionOffsets.ts";
import styles from "./SourceStage.module.css";

type SourceStageProps = {
  source: string;
  highlight: CodePointRange | null;
  onSelectionChange: (range: CodePointRange | null) => void;
};

function sliceByCodePoints(source: string, start: number, end: number) {
  const characters = [...source];
  return {
    before: characters.slice(0, start).join(""),
    middle: characters.slice(start, end).join(""),
    after: characters.slice(end).join(""),
  };
}

export function SourceStage({ source, highlight, onSelectionChange }: SourceStageProps) {
  function publishSelection(root: HTMLElement) {
    onSelectionChange(selectedCodePointRange(root, source));
  }

  const highlighted =
    highlight && highlight.end > highlight.start ? sliceByCodePoints(source, highlight.start, highlight.end) : null;

  return (
    <div
      className={styles.sourceBody}
      data-testid="source-body"
      onMouseUp={(event) => publishSelection(event.currentTarget)}
      onKeyUp={(event) => publishSelection(event.currentTarget)}
    >
      {highlighted ? (
        <>
          {highlighted.before}
          <mark id="source-highlight" className={styles.highlight}>
            {highlighted.middle}
          </mark>
          {highlighted.after}
        </>
      ) : (
        source
      )}
    </div>
  );
}
