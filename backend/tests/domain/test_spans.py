"""Disjoint source spans. Overlap is strict; touching edges are allowed."""

from __future__ import annotations


def test_overlapping_spans_are_rejected_by_predicate() -> None:
    from lait.domain.span import Span, overlaps

    # "responsible for rolling out" overlaps "rolling out".
    existing = Span(start=5, end=31)
    incoming = Span(start=21, end=32)
    assert overlaps(existing, incoming) is True
    assert overlaps(incoming, existing) is True
    assert overlaps(Span(start=0, end=4), Span(start=0, end=4)) is True


def test_touching_edges_do_not_overlap() -> None:
    from lait.domain.span import Span, overlaps

    left = Span(start=0, end=16)
    right = Span(start=16, end=27)
    assert overlaps(left, right) is False
    assert overlaps(right, left) is False
    assert overlaps(Span(start=0, end=3), Span(start=5, end=8)) is False
