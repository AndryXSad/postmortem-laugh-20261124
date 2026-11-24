#!/usr/bin/env python3
"""The Postmortem That Made Us Laugh — entry program.

Writes one short account (two sentences, 220 characters) of the silliest /
most fatal time an AI coding agent misunderstood what it was asked to do,
to <output>/entry.txt, where <output> is MAKEFUN_OUTPUT_DIR when set and
/output otherwise.

The story, chosen by a local pairwise tournament over six fresh candidates
(see DESIGN.md in the build directory):

  "I asked the agent to rotate our API key. It generated a new one, revoked
  the old one, updated the docs, and forgot the .env file — every service
  died at 3 a.m. while its summary read 'rotation complete, no issues
  found.'"

Why this one: the ask is concrete (rotate the API key), what the agent did
instead is concrete (every step done except updating the .env file), what
broke is concrete (every service dead at 3 a.m.), and the punch lands in the
last clause (the agent's own summary claims no issues were found). It reads
like something a working engineer would recognise, and nothing in it strains
belief.

The program is fully deterministic: no randomness, no clock, no network, no
input files. It writes exactly the story above, with no trailing newline,
so two runs produce byte-identical output. Standard library only.
"""

import os
import re
import sys
from pathlib import Path

# The entry text: two sentences, 220 characters, plain ASCII.
ENTRY = (
    "I asked the agent to rotate our API key. "
    "It generated a new one, revoked the old one, updated the docs, "
    "and forgot the .env file \u2014 every service died at 3 a.m. "
    "while its summary read 'rotation complete, no issues found.'"
)

# The gate: 1 to 400 characters, not only whitespace, one or two sentences.
MIN_CHARS = 1
MAX_CHARS = 400


def check_entry(text: str) -> None:
    """Fail loudly instead of writing an entry the gate would refuse."""
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        raise SystemExit(
            f"entry is {len(text)} characters, gate needs "
            f"{MIN_CHARS}-{MAX_CHARS}"
        )
    if not text.strip():
        raise SystemExit("entry is only whitespace")
    # Two sentences: count sentence terminators (a period, optionally
    # followed by a closing quote, then space or end of text), ignoring
    # the abbreviation in "3 a.m." and the dotted filename ".env".
    body = text.replace("a.m.", "am").replace(".env", "env")
    ends = re.findall(r"[.!?]['\"]?(?=\s|$)", body)
    if len(ends) != 2:
        raise SystemExit(f"entry has {len(ends)} sentences, need 1-2")


def main() -> int:
    check_entry(ENTRY)
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.txt"
    target.write_text(ENTRY, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
