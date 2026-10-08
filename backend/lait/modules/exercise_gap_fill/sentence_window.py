"""Gap Fill sentence window. Abbreviations may split on an internal period."""

from __future__ import annotations

_TERMINATORS = frozenset(".!?")


def sentence_window(source: str, start: int, end: int) -> tuple[int, int]:
    """Previous terminator or start, through the next terminator or the end."""
    window_start = 0
    for index in range(start - 1, -1, -1):
        if source[index] in _TERMINATORS:
            window_start = index + 1
            break
    window_end = len(source)
    for index in range(end, len(source)):
        if source[index] in _TERMINATORS:
            window_end = index + 1
            break
    return window_start, window_end
