#!/usr/bin/env python3
"""Fortune in a Pot — make.fun entry (Account A / overtheraa).

Writes one original, kind and funny fortune for a houseplant to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output). Deterministic, no network,
no model calls, standard library only.
"""

import os
import string
import sys

# The fortune: a prediction for the plant on the windowsill, warm about the
# plant and its keeper, with a small joke that lands (the plant was listening).
LINE = (
    "Soon you will outgrow this pot, and your keeper will finally "
    "admit you were listening all along."
)

MAX_CHARS = 120


def build_line() -> str:
    """Return the fortune line."""
    return LINE


def validate(line: str) -> str:
    """Check the line against the competition gate and return it unchanged.

    Gate: UTF-8 text of 1 to 120 characters, not only white space, a single
    line, printable characters only, and ending with terminal punctuation.
    """
    if not isinstance(line, str):
        raise ValueError("fortune must be a string")
    if not line.strip():
        raise ValueError("fortune must not be blank")
    if line != line.strip():
        raise ValueError("fortune must not start or end with white space")
    if "\n" in line or "\r" in line:
        raise ValueError("fortune must be a single line")
    if len(line) > MAX_CHARS:
        raise ValueError(f"fortune is {len(line)} chars, over the 120 limit")
    if len(line) < 1:
        raise ValueError("fortune must be at least 1 character")
    if not all(ch in string.printable for ch in line):
        raise ValueError("fortune must contain only printable characters")
    if line[-1] not in ".!?":
        raise ValueError("fortune must end with terminal punctuation")
    line.encode("utf-8")
    return line


def write_entry(line: str, out_dir: str | None = None) -> str:
    """Validate the line and write it to <out_dir>/entry.txt."""
    line = validate(line)
    out_dir = out_dir or os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(line + "\n")
    return path


def main() -> int:
    path = write_entry(build_line())
    print(f"wrote {path} ({len(build_line())} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
