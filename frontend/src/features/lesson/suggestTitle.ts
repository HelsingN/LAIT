const UNTITLED_LESSON = "Untitled Lesson";
const MAX_TITLE_LENGTH = 200;
const heading = /^\s{0,3}#{1,6}\s+/;

function isAlphanumeric(character: string): boolean {
  return /[\p{L}\p{N}]/u.test(character);
}

export function suggestTitle(source: string): string {
  for (const rawLine of source.split(/\r?\n/)) {
    const candidate = rawLine.trim().replace(heading, "").trim();
    if ([...candidate].some(isAlphanumeric)) {
      return candidate.slice(0, MAX_TITLE_LENGTH);
    }
  }
  return UNTITLED_LESSON;
}

export { UNTITLED_LESSON };
