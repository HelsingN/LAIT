"""Emit a node-test TAP summary so RED evidence can name the failing test."""

from __future__ import annotations

import sys

from _pytest.reports import TestReport


def _test_name(report: TestReport) -> str:
    return report.nodeid.split("::")[-1]


def pytest_terminal_summary(terminalreporter, exitstatus, config) -> None:
    del exitstatus, config
    passed = list(terminalreporter.stats.get("passed", []))
    failed = list(terminalreporter.stats.get("failed", []))
    errors = list(terminalreporter.stats.get("error", []))
    failing = failed + errors
    lines: list[str] = []
    index = 1
    for report in failing:
        lines.append(f"not ok {index} - {_test_name(report)}")
        index += 1
    for report in passed:
        lines.append(f"ok {index} - {_test_name(report)}")
        index += 1
    total = len(failing) + len(passed)
    lines.append(f"# tests {total}")
    lines.append(f"# pass {len(passed)}")
    lines.append(f"# fail {len(failing)}")
    sys.stdout.write("\n".join(lines) + "\n")
    sys.stdout.flush()
