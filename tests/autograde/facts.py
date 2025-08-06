"""Ground truth about the student's project repository. Read-only: never changes anything and never uses the network."""
from __future__ import annotations

import os
import subprocess
from typing import List, NamedTuple, Optional, Tuple

PROJECT = "kestrel-vision"
SAMPLE = "kestrel-sample"
LAB = "repo-creation-lab"
GIT_TIMEOUT = 60
INIT_SUBJECT = "chore: initialise repository structure"
TODO_SUBJECT = "docs: note the colour filter todo"
IGNORE_SUBJECT = "chore: add gitignore for python and dataset files"
SETTINGS_SUBJECT = "chore: add camera settings"
UNTRACK_SUBJECT = "chore: stop tracking secrets.txt"
STAFF_SUBJECT = "chore: add lab assignment and grader"
README = "# Kestrel Vision\n"
DETECTOR = "print('detector placeholder')\n"
TODO_LINE = "# TODO: add colour filter\n"
GITIGNORE_LINES = ["# Python", "__pycache__/", "*.pyc", ".venv/", "# Datasets and model weights", "data/raw/", "*.csv",
                   "*.pt", "*.h5", "# Editor and OS files", ".vscode/", ".DS_Store"]
GITIGNORE = "\n".join(GITIGNORE_LINES) + "\n"
TEAM_NAMES = {"asha verma", "ben carter", "chitra rao", "course staff"}
TEAM_EMAILS = {"asha@example.com", "ben@example.com", "chitra@example.com", "staff@example.com"}
PLACEHOLDER_NAMES = {"", "your full name", "your name"}
PLACEHOLDER_EMAILS = {"", "your.email@example.com", "your-email@your-college.edu"}


class GitError(RuntimeError):
    """Raised when the project is not where the grader expects it."""


class Commit(NamedTuple):
    """A commit with the facts the grader needs."""

    sha: str
    author: str
    email: str
    subject: str
    parents: List[str]


def run_git_rc(repo: str, *args: str) -> Tuple[int, str]:
    """Run git in 'repo' and return (exit code, stdout); a git call that hangs is stopped and reported as 124."""
    env = dict(os.environ, LC_ALL="C", GIT_PAGER="cat", GIT_TERMINAL_PROMPT="0")
    try:
        proc = subprocess.run(["git", *args], cwd=repo, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              encoding="utf-8", errors="replace", timeout=GIT_TIMEOUT)
    except (subprocess.TimeoutExpired, OSError):
        return 124, ""
    return proc.returncode, proc.stdout


def run_git(repo: str, *args: str) -> str:
    """Run git in 'repo' and return stdout ('' on failure)."""
    return run_git_rc(repo, *args)[1]


FORMAT = "--format=%H%x1f%an%x1f%ae%x1f%s%x1f%P"


def _commit(line: str) -> Optional[Commit]:
    parts = line.rstrip("\n").split("\x1f")
    return Commit(parts[0], parts[1], parts[2], parts[3], parts[4].split()) if len(parts) == 5 else None


class Facts:
    """Everything the grader needs to know about the project the student made."""

    def __init__(self, project: str, strict: bool = True) -> None:
        self.repo = os.path.abspath(project)
        if not strict:  # --outputs-only: the pasted text is graded without the repository
            return
        if not os.path.isdir(self.repo):
            raise GitError(f"the folder {self.repo} does not exist. Create the project with the commands of Task 1, "
                           f"or run the grader with --project <folder>.")
        if run_git_rc(self.repo, "rev-parse", "--is-inside-work-tree")[0] != 0 \
                or not os.path.isdir(os.path.join(self.repo, ".git")):
            raise GitError(f"{self.repo} is not a Git repository (there is no .git folder in it). Run 'git init -b main' there.")

    # -- configuration and refs -----------------------------------------------------------
    def effective_config(self, key: str) -> str:
        """Value of a config key as Git uses it in the project, local or global ('' if unset)."""
        return run_git(self.repo, "config", "--get", key).strip()

    def head_ref(self) -> str:
        """The branch HEAD points to, e.g. 'refs/heads/main' ('' when HEAD is detached)."""
        return run_git(self.repo, "symbolic-ref", "-q", "HEAD").strip()

    def rev(self, ref: str) -> str:
        """Full SHA of 'ref' ('' if it does not name a commit)."""
        return run_git(self.repo, "rev-parse", "--verify", "-q", f"{ref}^{{commit}}").strip()

    def commit_exists(self, token: str) -> bool:
        """True if 'token' names a commit object in the project."""
        return run_git_rc(self.repo, "cat-file", "-e", f"{token}^{{commit}}")[0] == 0

    # -- the history --------------------------------------------------------------------
    def history(self) -> List[Commit]:
        """The commits of the current branch, oldest first ([] when there is none yet)."""
        code, out = run_git_rc(self.repo, "log", "--reverse", "--first-parent", FORMAT, "HEAD", "--")
        return [c for c in map(_commit, out.splitlines()) if c] if code == 0 else []

    def commit_with(self, subject: str) -> Optional[Commit]:
        """The newest commit with this subject on the current branch (None if there is none)."""
        for commit in reversed(self.history()):
            if commit.subject == subject:
                return commit
        return None

    def files_changed(self, sha: str) -> List[str]:
        """The files a commit adds, changes or removes ('--root' makes it work for the first commit too)."""
        return run_git(self.repo, "diff-tree", "--root", "--no-commit-id", "--name-only", "-r", sha).split()

    def changes(self, sha: str) -> List[Tuple[str, str]]:
        """(status letter, path) of every file a commit touches."""
        out = run_git(self.repo, "diff-tree", "--root", "--no-commit-id", "--name-status", "-r", sha).split("\n")
        return [(line.split("\t")[0], line.split("\t")[1]) for line in out if "\t" in line]

    def file_at(self, ref: str, path: str) -> Optional[str]:
        """Content of 'path' at 'ref' (None if absent)."""
        code, out = run_git_rc(self.repo, "show", f"{ref}:{path}")
        return out if code == 0 else None

    # -- the working folder --------------------------------------------------------------
    def exists(self, path: str) -> bool:
        """True if 'path' (relative to the project) exists on disk."""
        return os.path.exists(os.path.join(self.repo, path))

    def read(self, path: str) -> Optional[str]:
        """Content of a file of the working folder (None if absent or unreadable)."""
        try:
            with open(os.path.join(self.repo, path), encoding="utf-8") as handle:
                return handle.read()
        except (OSError, UnicodeDecodeError):
            return None

    def is_ignored(self, path: str) -> bool:
        """True when a path is ignored by a rule and not tracked."""
        return run_git_rc(self.repo, "check-ignore", "-q", path)[0] == 0

    def tracked(self) -> List[str]:
        """The files Git tracks now."""
        return run_git(self.repo, "ls-files").split("\n")[:-1] if run_git(self.repo, "ls-files") else []

    def untracked(self) -> List[str]:
        """The untracked files that are not ignored."""
        return [x for x in run_git(self.repo, "ls-files", "--others", "--exclude-standard").split("\n") if x]

    # -- the clone next to the project ----------------------------------------------------
    def sibling(self, name: str) -> str:
        """Path of the folder 'name' next to the project ('' when it is not there or not a repository)."""
        path = os.path.join(os.path.dirname(self.repo), name)
        return path if os.path.isdir(path) and run_git_rc(path, "rev-parse", "--git-dir")[0] == 0 else ""

    def sibling_git(self, name: str, *args: str) -> Tuple[int, str]:
        """Run git in the folder 'name' next to the project ((127, '') when it is not there)."""
        path = self.sibling(name)
        return run_git_rc(path, *args) if path else (127, "")



