"""Verification-only reproduction of WR-02. Run from the repository root.

The barrier delays one legitimate submit after its public handler reads the
current item. All writes use a newly migrated temporary database. No learner
database or production code is changed. Exit 1 means the invariant failed.
"""

import runpy
import tempfile
import threading
from pathlib import Path


def main() -> None:
    helpers = runpy.run_path("backend/tests/application/test_practice_retry.py")
    with tempfile.TemporaryDirectory(prefix="lait-verify-wr02-") as temp:
        repository, _lesson, units, view, registry = helpers["_session"](
            Path(temp), ("rolling out", "the migration")
        )
        engine = repository._practice._session_factory.kw["bind"]
        paused = threading.Event()
        release = threading.Event()
        failures: list[str] = []

        class DelayedRepository:
            def __getattr__(self, name):
                return getattr(repository, name)

            def add_attempt(self, attempt, cursor):
                paused.set()
                if not release.wait(5):
                    raise RuntimeError("probe barrier timeout")
                repository.add_attempt(attempt, cursor)

        def delayed_request() -> None:
            try:
                helpers["_submit"](
                    DelayedRepository(), registry, view.session_id,
                    "drag", "wrong", units[1].id
                )
            except BaseException as exc:
                failures.append(repr(exc))

        thread = threading.Thread(target=delayed_request)
        try:
            thread.start()
            if not paused.wait(5):
                raise RuntimeError("probe did not reach persistence")
            helpers["_submit"](
                repository, registry, view.session_id, "drag", "wrong", units[1].id
            )
            helpers["_submit"](
                repository, registry, view.session_id,
                "drag", units[0].text, units[0].id
            )
            helpers["_submit"](
                repository, registry, view.session_id,
                "drag", units[1].text, units[1].id
            )
            before = repository.get_practice_session(view.session_id).cursor
            release.set()
            thread.join(5)
            after = repository.get_practice_session(view.session_id).cursor
            if before != 2 or failures or thread.is_alive():
                raise RuntimeError(f"probe setup failed: {before=}, {failures=}")
            print(f"WR-02: cursor before delayed submit={before}, after={after}; request errors={failures}")
        finally:
            release.set()
            thread.join(6)
            engine.dispose()
    assert after >= before, (
        f"PROVEN DEFECT: delayed submit rewound durable cursor from {before} to {after}"
    )


if __name__ == "__main__":
    main()

