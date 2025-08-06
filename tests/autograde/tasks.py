"""Graders for the five tasks of the Repository Creation lab."""
from __future__ import annotations

import re
from typing import List

from .context import Ctx
from .facts import (
    DETECTOR, GITIGNORE, GITIGNORE_LINES, INIT_SUBJECT, IGNORE_SUBJECT, PLACEHOLDER_EMAILS, PLACEHOLDER_NAMES, README,
    SAMPLE, SETTINGS_SUBJECT, STAFF_SUBJECT, TEAM_EMAILS, TEAM_NAMES, TODO_LINE, TODO_SUBJECT, UNTRACK_SUBJECT, LAB,
)
from .framework import Task
from .textutil import get_answer, oneline_entries, sha_matches, strip_decoration

GIT_DIR_NAMES = {"HEAD", "config", "description", "hooks", "info", "objects", "refs"}
COMMIT_RE = r"(?m)^\[main (?:\(root-commit\) )?([0-9a-f]{7,40})\] "
STATUS_NONE = 'nothing to commit (create/copy files and use "git add" to track)'


def clean(text: str) -> str:
    """The pasted text without the '$ command' lines a student may have copied along with the output."""
    return "\n".join(ln for ln in text.split("\n") if not ln.startswith("$ "))


def lines_of(text: str) -> List[str]:
    """The non-empty lines of a pasted output, without trailing blanks and without '$ command' prompt lines."""
    return [ln.rstrip() for ln in clean(text).split("\n") if ln.strip()]


def _subjects(text: str) -> List[str]:
    return [strip_decoration(e.subject) for e in oneline_entries(text)]


def _commit_line(text: str, subject: str) -> bool:
    return re.search(COMMIT_RE + re.escape(subject) + r"$", text, re.M) is not None


def _answer(ctx: Ctx, number: int) -> str:
    return get_answer(ctx.text, number).strip("`'\" ").strip()


# -- Task 1 -----------------------------------------------------------------
def grade_task1(ctx: Ctx) -> Task:
    """Task 1: make a folder a repository and look inside .git."""
    t = Task(1, "Initialise a repository", 20, ctx.repo_mode)
    f = ctx.facts
    s11, s12, s13, s14 = ctx.step("1.1"), ctx.step("1.2"), ctx.step("1.3"), ctx.step("1.4")
    t.check(4, "1.1 init output: 'Initialized empty Git repository in .../kestrel-vision/.git/'",
            lambda: re.search(r"(?m)^Initialized empty Git repository in .*/kestrel-vision/\.git/$", s11) is not None)
    t.check(3, "1.2 ls -a: exactly '.', '..' and '.git' (a new repository is an empty folder with a hidden .git)",
            lambda: set(clean(s12).split()) == {".", "..", ".git"})
    t.check(4, "1.3 ls .git: HEAD, config, description, hooks, info, objects and refs",
            lambda: GIT_DIR_NAMES <= set(clean(s13).split()))
    t.check(2, "1.4 status: 'On branch main'", lambda: re.search(r"(?m)^On branch main$", s14) is not None)
    t.check(1, "1.4 status: 'No commits yet'", lambda: "No commits yet" in s14)
    t.check(2, "1.4 status: " + STATUS_NONE, lambda: STATUS_NONE in s14)
    t.check(2, "ANSWER-1 is HEAD (the file in .git that says which branch is checked out)",
            lambda: _answer(ctx, 1) == "HEAD")
    t.check(2, "live repo: the folder kestrel-vision next to this lab folder is a repository whose first branch is main",
            lambda: f.head_ref() == "refs/heads/main", needs_repo=True,
            why=lambda: "create it with: git init -b main (HEAD must point to refs/heads/main)")
    return t


# -- Task 2 -----------------------------------------------------------------
def grade_task2(ctx: Ctx) -> Task:
    """Task 2: the project, and a file in each of the four states."""
    t = Task(2, "The project and the four file states", 25, ctx.repo_mode)
    f = ctx.facts
    s21, s22, s23, s24, s25 = (ctx.step(x) for x in ("2.1", "2.2", "2.3", "2.4", "2.5"))
    t.check(1, "2.1 status: 'No commits yet'", lambda: "No commits yet" in s21)
    t.check(1, "2.1 status: 'Untracked files:'", lambda: "Untracked files:" in s21)
    t.check(2, "2.1 status: README.md and src/ are listed as untracked",
            lambda: re.search(r"(?m)^\s+README\.md$", s21) is not None and re.search(r"(?m)^\s+src/$", s21) is not None)
    t.check(1, "2.1 status: data/ and docs/ are NOT listed (Git does not see empty folders)",
            lambda: "Untracked files:" in s21 and re.search(r"(?m)^\s+(data|docs)/$", s21) is None)
    t.check(2, "2.2 status: 'Changes to be committed:'", lambda: "Changes to be committed:" in s22)
    t.check(2, "2.2 status: new file README.md and new file src/detector.py are staged",
            lambda: re.search(r"new file:\s+README\.md", s22) is not None
            and re.search(r"new file:\s+src/detector\.py", s22) is not None)
    t.check(1, "2.2 status: nothing is untracked any more", lambda: "Changes to be committed:" in s22 and "Untracked files:" not in s22)
    t.check(3, "2.3 commit output: '[main (root-commit) <sha>] chore: initialise repository structure'",
            lambda: _commit_line(s23, INIT_SUBJECT) and "(root-commit)" in s23)
    t.check(1, "2.3 commit output: 2 files changed, 2 insertions(+)",
            lambda: re.search(r"\b2 files changed, 2 insertions\(\+\)", s23) is not None)
    t.check(1, "2.3 commit output: create mode for README.md and src/detector.py",
            lambda: re.search(r"create mode 100644 README\.md", s23) is not None
            and re.search(r"create mode 100644 src/detector\.py", s23) is not None)
    t.check(3, "2.4 status --short: ' M src/detector.py' (modified, not staged), and nothing else",
            lambda: [ln.strip() for ln in lines_of(s24)] == ["M src/detector.py"])
    t.check(3, "2.5 log --oneline: two commits, newest first: the todo note, then the first commit",
            lambda: _subjects(s25) == [TODO_SUBJECT, INIT_SUBJECT])
    first = re.search(COMMIT_RE, s23)
    answer = _answer(ctx, 2)
    t.check(2, "ANSWER-2 is the commit number printed in 2.3 (at least 7 characters)",
            lambda: first is not None and len(answer) >= 7 and (sha_matches(answer, first.group(1))
                                                                  or first.group(1).lower().startswith(answer.lower())))
    history = f.history() if ctx.repo_mode else []
    root = history[0] if history else None
    t.check(1, "live repo: the first commit holds exactly README.md and src/detector.py, with the contents of the handout",
            lambda: root is not None and root.subject == INIT_SUBJECT and not root.parents
            and sorted(f.files_changed(root.sha)) == ["README.md", "src/detector.py"]
            and f.file_at(root.sha, "README.md") == README and f.file_at(root.sha, "src/detector.py") == DETECTOR
            and first is not None and root.sha.startswith(first.group(1)),
            needs_repo=True, why=lambda: "the first commit must add README.md and src/detector.py only, and its number must be the one pasted in 2.3")
    name, email = f.effective_config("user.name"), f.effective_config("user.email")
    t.check(1, "live repo: the commits carry your own identity (not a placeholder, not a teammate's)",
            lambda: bool(history) and name.lower() not in PLACEHOLDER_NAMES | TEAM_NAMES and "@" in email
            and email.lower() not in PLACEHOLDER_EMAILS | TEAM_EMAILS
            and all(c.author == name and c.email == email for c in history[:2]),
            needs_repo=True, why=lambda: "set your name and email (Experiment 3) before you commit")
    return t


# -- Task 3 -----------------------------------------------------------------
def grade_task3(ctx: Ctx) -> Task:
    """Task 3: write .gitignore and commit it."""
    t = Task(3, "The .gitignore file", 20, ctx.repo_mode)
    f = ctx.facts
    s31, s32, s33, s34 = (ctx.step(x) for x in ("3.1", "3.2", "3.3", "3.4"))
    t.check(3, "3.1 status --short: '?? .gitignore' (the new file is untracked), and nothing else",
            lambda: lines_of(s31) == ["?? .gitignore"])
    t.check(4, "3.2 cat: the 12 lines of the handout, in order", lambda: lines_of(s32) == GITIGNORE_LINES)
    t.check(3, "3.3 commit output: '[main <sha>] chore: add gitignore for python and dataset files'",
            lambda: _commit_line(s33, IGNORE_SUBJECT))
    t.check(1, "3.3 commit output: 1 file changed, 12 insertions(+)",
            lambda: re.search(r"\b1 file changed, 12 insertions\(\+\)", s33) is not None)
    t.check(1, "3.3 commit output: create mode 100644 .gitignore", lambda: "create mode 100644 .gitignore" in s33)
    t.check(3, "3.4 log --oneline: three commits, newest first: the gitignore, the todo note, the first commit",
            lambda: _subjects(s34) == [IGNORE_SUBJECT, TODO_SUBJECT, INIT_SUBJECT])
    history = f.history() if ctx.repo_mode else []
    commit = f.commit_with(IGNORE_SUBJECT) if ctx.repo_mode else None
    printed = re.search(COMMIT_RE, s33)
    t.check(3, "live repo: the commit 'chore: add gitignore for python and dataset files' adds only .gitignore, with the handout's content",
            lambda: commit is not None and f.changes(commit.sha) == [("A", ".gitignore")]
            and f.file_at(commit.sha, ".gitignore") == GITIGNORE and printed is not None
            and commit.sha.startswith(printed.group(1)), needs_repo=True,
            why=lambda: "the commit must add .gitignore (and nothing else) with exactly the 12 lines of the handout")
    t.check(2, "live repo: the history starts with the first commit, the todo note and then the gitignore commit",
            lambda: [c.subject for c in history[:3]] == [INIT_SUBJECT, TODO_SUBJECT, IGNORE_SUBJECT], needs_repo=True)
    return t


# -- Task 4 -----------------------------------------------------------------
def grade_task4(ctx: Ctx) -> Task:
    """Task 4: prove that the ignore rules work."""
    t = Task(4, "Prove the rules work", 15, ctx.repo_mode)
    f = ctx.facts
    s41, s42, s43 = ctx.step("4.1"), ctx.step("4.2"), ctx.step("4.3")
    t.check(4, "4.1 status --short: only '?? notes.txt' (the file in data/raw is hidden by the rules)",
            lambda: lines_of(s41) == ["?? notes.txt"])
    rule = re.search(r"(?m)^\.gitignore:(\d+):data/raw/\s+data/raw/frames\.csv$", s42)
    t.check(3, "4.2 check-ignore -v: '.gitignore:<line>:data/raw/   data/raw/frames.csv' (the rule that hides the file)",
            lambda: rule is not None)
    t.check(2, "4.2 the rule is on line 6 of .gitignore, where 'data/raw/' is in the handout's file",
            lambda: rule is not None and rule.group(1) == str(GITIGNORE_LINES.index("data/raw/") + 1))
    t.check(4, "4.3 status --ignored --short: '?? notes.txt' and '!! data/' (ignored files are marked !!; data/ holds nothing else)",
            lambda: set(lines_of(s43)) == {"?? notes.txt", "!! data/"})
    t.check(2, "live repo: data/raw/frames.csv exists and is ignored, notes.txt exists and is untracked",
            lambda: f.exists("data/raw/frames.csv") and f.is_ignored("data/raw/frames.csv") and f.exists("notes.txt")
            and "notes.txt" in f.untracked(), needs_repo=True,
            why=lambda: "create data/raw/frames.csv and notes.txt as in the handout, and do not add notes.txt")
    return t


# -- Task 5 -----------------------------------------------------------------
def grade_task5(ctx: Ctx) -> Task:
    """Task 5: what Git tracks, stopping tracking a file, and looking at an existing repository."""
    t = Task(5, "Track and untrack, and look at an existing repository", 20, ctx.repo_mode)
    f = ctx.facts
    s = {k: ctx.step(k) for k in ("5.1", "5.2", "5.3", "5.4", "5.5", "5.6", "5.7")}
    t.check(3, "5.1 ls-files: .gitignore, README.md, src/detector.py and src/secrets.txt (the secrets file is still tracked)",
            lambda: lines_of(s["5.1"]) == [".gitignore", "README.md", "src/detector.py", "src/secrets.txt"])
    t.check(2, "5.2 rm --cached: \"rm 'src/secrets.txt'\"", lambda: lines_of(s["5.2"]) == ["rm 'src/secrets.txt'"])
    t.check(1, "5.3 commit output: '[main <sha>] chore: stop tracking secrets.txt'", lambda: _commit_line(s["5.3"], UNTRACK_SUBJECT))
    t.check(1, "5.3 commit output: delete mode 100644 src/secrets.txt", lambda: "delete mode 100644 src/secrets.txt" in s["5.3"])
    t.check(1, "5.3 commit output: 2 files changed (the .gitignore line and the removed file)",
            lambda: re.search(r"\b2 files changed, 1 insertion\(\+\), 1 deletion\(-\)", s["5.3"]) is not None)
    t.check(2, "5.4 ls-files --others --exclude-standard: only notes.txt", lambda: lines_of(s["5.4"]) == ["notes.txt"])
    t.check(3, "5.5 status --ignored --short: '?? notes.txt', '!! data/' and '!! src/secrets.txt'",
            lambda: set(lines_of(s["5.5"])) == {"?? notes.txt", "!! data/", "!! src/secrets.txt"})
    t.check(1, "5.6 clone output: \"Cloning into 'kestrel-sample'...\"", lambda: "Cloning into 'kestrel-sample'" in s["5.6"])
    t.check(1, "5.7 log -5 of the clone: five commits, the newest is 'chore: add lab assignment and grader'",
            lambda: len(oneline_entries(s["5.7"])) == 5 and _subjects(s["5.7"])[:1] == [STAFF_SUBJECT])
    t.check(2, "ANSWER-3 is no (a file that is already tracked stays tracked when you add it to .gitignore)",
            lambda: _answer(ctx, 3).lower() in ("no", "no.", "nope"))
    printed = re.search(COMMIT_RE, s["5.3"])
    settings = f.commit_with(SETTINGS_SUBJECT) if ctx.repo_mode else None
    untrack = f.commit_with(UNTRACK_SUBJECT) if ctx.repo_mode else None
    t.check(2, "live repo: src/secrets.txt is still on disk and ignored, is no longer in the newest commit, and was committed before",
            lambda: f.exists("src/secrets.txt") and f.is_ignored("src/secrets.txt") and untrack is not None
            and settings is not None and f.file_at("HEAD", "src/secrets.txt") is None
            and f.file_at(settings.sha, "src/secrets.txt") is not None and f.changes(untrack.sha)
            and ("D", "src/secrets.txt") in f.changes(untrack.sha) and printed is not None
            and untrack.sha.startswith(printed.group(1)), needs_repo=True,
            why=lambda: "expected: commit 'chore: add camera settings', then git rm --cached and 'chore: stop tracking secrets.txt'")
    code, url = f.sibling_git(SAMPLE, "config", "--get", "remote.origin.url")
    t.check(1, "live repo: the folder kestrel-sample next to the project is a clone of the lab folder",
            lambda: code == 0 and url.strip().rstrip("/").endswith("/" + LAB), needs_repo=True,
            why=lambda: "expected a clone made with: git clone repo-creation-lab kestrel-sample")
    return t
