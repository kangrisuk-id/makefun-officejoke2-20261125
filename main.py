#!/usr/bin/env python3
"""One-Line Office Joke Laugh-Off — entry program.

Writes the single winning one-line office joke to entry.txt in the
output directory the harness names (MAKEFUN_OUTPUT_DIR), so the
sealed gate can read it. Pure standard library; no third-party code.
"""

import os
import sys

# The winning line, picked from 40 candidates by a knockout tournament
# scored against the judge's five published criteria (see candidates.md).
JOKE = "We replaced the suggestion box with a shredder to cut out the middleman."


def output_candidates():
    """Yield the directories to try, best first, each only once."""
    seen = set()
    named = os.environ.get("MAKEFUN_OUTPUT_DIR")
    for directory in (named, "/output", os.path.dirname(os.path.abspath(__file__))):
        if directory and directory not in seen:
            seen.add(directory)
            yield directory


def checked_joke():
    """Return the joke only if it passes the gate: 1-200 characters of
    UTF-8 text, not only white space, on a single line."""
    if not (1 <= len(JOKE) <= 200):
        raise ValueError("joke length %d outside the 1-200 gate" % len(JOKE))
    if not JOKE.strip() or "\n" in JOKE:
        raise ValueError("joke must be one non-blank line")
    return JOKE


def main():
    joke = checked_joke()
    failures = []
    for directory in output_candidates():
        path = os.path.join(directory, "entry.txt")
        try:
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(joke)
        except OSError as exc:
            failures.append("%s: %s" % (path, exc))
            continue
        return 0
    for failure in failures:
        print("could not write entry: " + failure, file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
