"""Per-item chip order. The stored generation row stays in span order."""

from __future__ import annotations

import hashlib
import random


def permute_chip_ids(
    ids: tuple[str, ...],
    *,
    session_id: str,
    item_id: str,
) -> tuple[str, ...]:
    if len(ids) < 2:
        return ids
    digest = hashlib.sha256(f"{session_id}\x1f{item_id}".encode()).digest()
    rng = random.Random(int.from_bytes(digest, "big"))
    order = list(ids)
    for index in range(len(order) - 1, 0, -1):
        swap = rng.randrange(index + 1)
        order[index], order[swap] = order[swap], order[index]
    permuted = tuple(order)
    if permuted == ids:
        return ids[1:] + ids[:1]
    return permuted
