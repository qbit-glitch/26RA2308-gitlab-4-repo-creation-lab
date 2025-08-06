"""Detects pasted output that does not belong to the project being graded."""
from __future__ import annotations

import re
from typing import List, Set

from .context import Ctx
from .facts import SAMPLE
from .textutil import line_shas

BRACKET_SHA_RE = re.compile(r"\[[^\]]*? ([0-9a-f]{7,40})\]")
PROJECT_STEPS = ("2.3", "2.5", "3.3", "3.4", "5.3")  # commit numbers printed inside the project


def integrity_warnings(ctx: Ctx) -> List[str]:
    """Return human-readable warnings; an empty list means the pasted text matches this project."""
    if not ctx.repo_mode:
        return []
    facts = ctx.facts
    foreign: Set[str] = set()
    for step_id in PROJECT_STEPS:
        text = ctx.step(step_id)
        for token in line_shas(text) + BRACKET_SHA_RE.findall(text):
            if not facts.commit_exists(token):
                foreign.add(token)
    if facts.sibling(SAMPLE):  # the commits printed in 5.7 must exist in the clone they came from
        for token in line_shas(ctx.step("5.7")):
            if facts.sibling_git(SAMPLE, "cat-file", "-e", f"{token}^{{commit}}")[0] != 0:
                foreign.add(token)
    warnings: List[str] = []
    if foreign:
        shown = ", ".join(sorted(foreign)[:6])
        warnings.append(f"{len(foreign)} commit SHA(s) in the pasted text do not exist in your repositories "
                        f"(e.g. {shown}); the outputs were not produced here")
    return warnings
