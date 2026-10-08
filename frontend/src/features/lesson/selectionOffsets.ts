export type CodePointRange = {
  start: number;
  end: number;
};

export function utf16OffsetToCodePoint(source: string, utf16Offset: number): number {
  if (utf16Offset <= 0) {
    return 0;
  }
  let remaining = utf16Offset;
  let codePoints = 0;
  for (const character of source) {
    if (remaining <= 0) {
      break;
    }
    remaining -= character.length;
    codePoints += 1;
  }
  return codePoints;
}

export function selectedCodePointRange(root: HTMLElement, source: string): CodePointRange | null {
  const selection = window.getSelection();
  if (!selection || selection.rangeCount === 0 || selection.isCollapsed) {
    return null;
  }
  const range = selection.getRangeAt(0);
  if (!root.contains(range.startContainer) || !root.contains(range.endContainer)) {
    return null;
  }
  const startUtf16 = utf16OffsetInRoot(root, range.startContainer, range.startOffset);
  const endUtf16 = utf16OffsetInRoot(root, range.endContainer, range.endOffset);
  const start = Math.min(startUtf16, endUtf16);
  const end = Math.max(startUtf16, endUtf16);
  if (start === end) {
    return null;
  }
  return {
    start: utf16OffsetToCodePoint(source, start),
    end: utf16OffsetToCodePoint(source, end),
  };
}

function utf16OffsetInRoot(root: HTMLElement, container: Node, offset: number): number {
  if (container === root) {
    let utf16 = 0;
    for (let index = 0; index < offset && index < root.childNodes.length; index += 1) {
      utf16 += root.childNodes[index]?.textContent?.length ?? 0;
    }
    return utf16;
  }
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
  let utf16 = 0;
  let current = walker.nextNode();
  while (current) {
    if (current === container) {
      return utf16 + offset;
    }
    utf16 += current.textContent?.length ?? 0;
    current = walker.nextNode();
  }
  return utf16;
}
