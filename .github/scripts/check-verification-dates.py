#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path


MARKER = re.compile(
    r"^\s*<!--\s*last_verified:\s*(.*?)\s*-->\s*$",
    re.IGNORECASE,
)
SIX_MONTHS = 183
TWELVE_MONTHS = 365


def annotation(level: str, path: Path, line: int, message: str) -> None:
    print(f"::{level} file={path.as_posix()},line={line}::{message}")


def main() -> int:
    today = date.today()
    marker_count = 0
    error_count = 0

    for path in sorted(Path(".").rglob("*.md")):
        if ".git" in path.parts:
            continue

        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(),
            start=1,
        ):
            match = MARKER.match(line)
            if not match:
                continue

            marker_count += 1
            raw_date = match.group(1)

            try:
                verified = date.fromisoformat(raw_date)
            except ValueError:
                annotation(
                    "error",
                    path,
                    line_number,
                    f"last_verified must be a valid YYYY-MM-DD date, found {raw_date!r}.",
                )
                error_count += 1
                continue

            age = (today - verified).days
            if age < 0:
                annotation(
                    "error",
                    path,
                    line_number,
                    f"last_verified is {abs(age)} day(s) in the future.",
                )
                error_count += 1
            elif age > TWELVE_MONTHS:
                annotation(
                    "warning",
                    path,
                    line_number,
                    f"Source verification is {age} days old, more than twelve months.",
                )
            elif age > SIX_MONTHS:
                annotation(
                    "warning",
                    path,
                    line_number,
                    f"Source verification is {age} days old, more than six months.",
                )

    if marker_count == 0:
        print("No last_verified markers found.")
    else:
        print(f"Checked {marker_count} last_verified marker(s).")

    return 1 if error_count else 0


if __name__ == "__main__":
    sys.exit(main())
