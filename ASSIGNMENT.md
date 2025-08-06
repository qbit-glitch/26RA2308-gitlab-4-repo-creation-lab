# Git Lab Assignment: Kestrel-1 Rover, Start a Repository

**Course:** 26RA2308 Git for Software Development and Collaboration
**Builds on:** Experiments 1 to 3. **Based on:** Experiment 4 (Repository Creation and Management)
**Time allowed:** 1 hour. **Marks:** 100

---

## The story

It is your fourth morning at the Kestrel-1 rover lab. **Chitra** keeps the camera detector in a loose folder on her laptop:
no history, no backup, and last week she lost an afternoon of work. You turn that folder into a proper Git repository, and
you decide what goes into it and what stays out. The lab has one rule:

> **Before you commit, look. `git status` is your eyes: run it before and after every step.**

In the next hour you create a repository (`git init`) and look inside its hidden `.git` folder, watch one file go through the
four states a file can be in (untracked, staged, committed, modified), write a `.gitignore` so that datasets and secrets never
get committed, prove that it works (`git check-ignore`, `git status --ignored`), and stop tracking a file that was committed by
mistake (`git ls-files`, `git rm --cached`). At the end you clone an existing repository and compare it with yours. Along
the way you reuse the terminal skills of Experiments 1 and 2 (`mkdir`, `cd`, `ls`, `cat`, `echo`, `touch`) and the identity
you set in Experiment 3.

## What you need

`git` and `python3` (3.9 or newer). **Your name and email must be set in Git** (Experiment 3), because every commit carries them.
Check:

```bash
git config user.name
git config user.email
```

Both must print your own details. If one prints nothing, set it first (use your real name and email, and keep the quotation marks):

```bash
git config --global user.name "Your Full Name"
git config --global user.email "your-email@example.com"
```

If your terminal does not print English messages, run `export LC_ALL=C` first, because the grader reads what Git prints. If a
long output opens in a pager (a screen with `:` or `(END)` at the bottom), press `q` to leave it.

## Start: get the lab

Clone into your **home directory** (the folder `cd ~` takes you to). This is not a numbered step and nothing is pasted for it.
The lab folder gives you this handout, the answer file and the grader. **It is not the repository you will create.**

```bash
cd ~
git clone https://github.com/qbit-glitch/26RA2308-gitlab-4-repo-creation-lab.git repo-creation-lab
cd repo-creation-lab
cp submission/outputs.template.txt submission/outputs.txt
```

Now open `submission/outputs.txt` in any editor, type your full name after `Name   :`, and save.

## Rules

1. Your own repository is a **new folder `kestrel-vision` in your home directory**, next to `repo-creation-lab`. Never create it
   inside `repo-creation-lab`: a repository inside a repository confuses Git.
2. Stay on the branch `main`. Do not use `git reset`, `git rebase` or `--force`.
3. Type the commands yourself. The grader checks that your pasted output matches what is really in your repository (your commit
   numbers and your files), so output copied from a classmate is detected.
4. Keep the folder names, file contents and commit messages exactly as written.

## How you hand in your work

1. After **each step** (numbered **1.1**, **1.2**, ...), paste what the terminal printed under the matching `--- N.M` line of
   `submission/outputs.txt`, replacing `(paste output here)`. Do not edit or delete the `=== TASK` and `--- N.M` lines. Type your
   answers after the colon of the `ANSWER-n :` lines (the line just below each `# Qn` question).
2. Fill in your registration number at the top of the file.
3. Run the automatic grader whenever you want to see where you stand. Go into the lab folder first:

   ```bash
   cd ~/repo-creation-lab
   python3 tests/grade.py
   ```

   It prints **PASS** or **FAIL** for every task, tells you exactly which check failed, and shows your score out of 100. You can
   fix a mistake and run it again as often as you like. The grader never uses the internet: it reads `submission/outputs.txt`
   and your repository `~/kestrel-vision`.
4. When you are done, show the final grader output to your instructor (it is also saved in `submission/results.txt`), and submit
   `submission/outputs.txt` as instructed.

## Time plan

| Task | Time on the clock | Topic | Suggested time | Marks |
|---|---|---|---|---|
| 1 | 09:00 | Initialise a repository | 8 min | 20 |
| 2 | 09:08 | The project and the four file states | 14 min | 25 |
| 3 | 09:22 | The .gitignore file | 10 min | 20 |
| 4 | 09:32 | Prove the rules work | 8 min | 15 |
| 5 | 09:40 | Track and untrack, and look at an existing repository | 14 min | 20 |
| | | Buffer for running the grader and fixing mistakes | 6 min | |

**Skipped a task, or running behind?** You do not lose the rest of the lab. A **catch-up box** at the start of a later task
brings your project to the state you need, in a few lines. If you skipped several tasks, run their boxes in order. You lose only
the marks of the task you skipped.

---

## Task 1: Initialise a repository (20 marks)

A repository is an ordinary folder that contains a hidden folder named `.git`. Make the folder and turn it into a repository.
`-b main` names the first branch `main`.

```bash
cd ~
mkdir kestrel-vision
cd kestrel-vision
git init -b main
```

* **1.1** Paste the output of `git init -b main`. It tells you where the `.git` folder was made.

```bash
ls -a
```

* **1.2** Paste the output. The option `-a` shows hidden files: the only thing in the folder is `.git`.

```bash
ls .git
```

* **1.3** Paste the output. This is the whole repository: the object database (`objects`), the branches and tags (`refs`), the
  hooks, the settings (`config`) and the file `HEAD`. If you delete `.git`, the folder is a plain folder again.

```bash
git status
```

* **1.4** Paste the output. Find `On branch main` and `No commits yet`.
* Then type your answer to `ANSWER-1` in the file (there is no pasted output for it): which file inside `.git` says which branch
  is checked out?

## Task 2: The project and the four file states (25 marks)

A file is always in one of four states: **untracked** (Git has never seen it), **staged** (it is in the next commit),
**committed** (it is in the history) and **modified** (a committed file was changed again). You watch one file go through all four.
Stay in `~/kestrel-vision`.

*Needs:* the repository of Task 1.

> **Catch-up box: only if you skipped Task 1.** Run these four lines, once. They do what Task 1 does. If you did Task 1, do
> **not** run them. There is nothing to paste for them, and you lose only the marks of Task 1.
>
> ```bash
> cd ~
> mkdir kestrel-vision
> cd kestrel-vision
> git init -b main
> ```

Build the project: three folders and two files.

```bash
mkdir src data docs
echo "# Kestrel Vision" > README.md
echo "print('detector placeholder')" > src/detector.py
git status
```

* **2.1** Paste the output of `git status`. The two files are **untracked**. Notice that `data/` and `docs/` are not listed: Git
  does not see empty folders.

```bash
git add README.md src/detector.py
git status
```

* **2.2** Paste the output of the second command. The files are now **staged**: `Changes to be committed`.

```bash
git commit -m "chore: initialise repository structure"
```

* **2.3** Paste the output. Both files are **committed**; the number in square brackets is the commit number.

```bash
echo "# TODO: add colour filter" >> src/detector.py
git status --short
```

* **2.4** Paste the output of `git status --short`. The file is **modified**: a space, then `M`. (`--short` prints one line per
  file.)

```bash
git commit -am "docs: note the colour filter todo"
git log --oneline
```

* **2.5** Paste the output of `git log --oneline`: two commits, newest first. (`-a` stages every change to a file Git already
  tracks; `-m` gives the message.)
* Then type your answer to `ANSWER-2` in the file: the commit number (at least 7 characters) printed in 2.3.

## Task 3: The .gitignore file (20 marks)

Some files must never be committed: caches, virtual environments, datasets and trained models. A file named `.gitignore` lists
the patterns Git must ignore. Stay in `~/kestrel-vision`.

*Needs:* the project of Task 2.

> **Catch-up box: only if you skipped Task 2.** Run these lines, once, in `~/kestrel-vision`. They do what Task 2 does. If you
> did Task 2, do **not** run them. There is nothing to paste for them, and you lose only the marks of Task 2. (If you skipped
> Task 1 as well, run its box first.)
>
> ```bash
> cd ~/kestrel-vision
> mkdir src data docs
> echo "# Kestrel Vision" > README.md
> echo "print('detector placeholder')" > src/detector.py
> git add README.md src/detector.py
> git commit -m "chore: initialise repository structure"
> echo "# TODO: add colour filter" >> src/detector.py
> git commit -am "docs: note the colour filter todo"
> ```

Write the file. The first line starts a text block that ends at the line `EOF`: everything in between goes into the file.
Type the lines exactly as shown, including the lines that start with `#` (they are comments).

```bash
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.pyc
.venv/
# Datasets and model weights
data/raw/
*.csv
*.pt
*.h5
# Editor and OS files
.vscode/
.DS_Store
EOF
git status --short
```

* **3.1** Paste the output of `git status --short`. `??` means untracked: the new file itself is not ignored.

```bash
cat .gitignore
```

* **3.2** Paste the output. It must be the 12 lines above, in the same order.

```bash
git add .gitignore
git commit -m "chore: add gitignore for python and dataset files"
```

* **3.3** Paste the output of the `git commit` command.

```bash
git log --oneline
```

* **3.4** Paste the output: three commits, newest first.

## Task 4: Prove the rules work (15 marks)

Create two files: one that the rules hide, and one that nothing hides. Stay in `~/kestrel-vision`.

*Needs:* the `.gitignore` commit of Task 3.

> **Catch-up box: only if you skipped Task 3.** Run these four lines, once, in `~/kestrel-vision`. They do what Task 3 does. If
> you did Task 3, do **not** run them. There is nothing to paste for them, and you lose only the marks of Task 3. (If you skipped
> Task 2 as well, run its box first.)
>
> ```bash
> cd ~/kestrel-vision
> cat > .gitignore << 'EOF'
> # Python
> __pycache__/
> *.pyc
> .venv/
> # Datasets and model weights
> data/raw/
> *.csv
> *.pt
> *.h5
> # Editor and OS files
> .vscode/
> .DS_Store
> EOF
> git add .gitignore
> git commit -m "chore: add gitignore for python and dataset files"
> ```

```bash
mkdir -p data/raw
touch data/raw/frames.csv
echo "scratch notes" > notes.txt
git status --short
```

* **4.1** Paste the output of `git status --short`. Only `notes.txt` is listed: Git hides `data/raw/frames.csv` because of the
  rule `data/raw/`.

```bash
git check-ignore -v data/raw/frames.csv
```

* **4.2** Paste the output. It names the rule that hides the file: the file `.gitignore`, the **line number** of the rule, the rule
  itself, and the path.

```bash
git status --ignored --short
```

* **4.3** Paste the output. `!!` marks ignored files. Git shows the folder `data/` rather than the file, because `data/` holds
  nothing but ignored files.

## Task 5: Track and untrack, and look at an existing repository (20 marks)

A `.gitignore` rule only hides files that Git does **not** track yet. Chitra committed a camera settings file with a key in it
before anybody wrote a rule for it. You see what Git tracks, stop tracking the file, and keep it on disk. Stay in
`~/kestrel-vision`.

*Needs:* the project of Task 4.

> **Catch-up box: only if you skipped Task 4.** Run these four lines, once. They do what Task 4 does. If you did Task 4, do
> **not** run them. There is nothing to paste for them, and you lose only the marks of Task 4. (If you skipped Task 3 as well,
> run its box first.)
>
> ```bash
> cd ~/kestrel-vision
> mkdir -p data/raw
> touch data/raw/frames.csv
> echo "scratch notes" > notes.txt
> ```

First the mistake: commit the settings file, and only afterwards write the rule for it. There is nothing to paste for these lines.

```bash
echo "camera_key=abc123" > src/secrets.txt
git add src/secrets.txt
git commit -m "chore: add camera settings"
echo "src/secrets.txt" >> .gitignore
```

```bash
git ls-files
```

* **5.1** Paste the output. `git ls-files` lists every file Git tracks. The secrets file is **still tracked**, although the rule is
  in `.gitignore`.

```bash
git rm --cached src/secrets.txt
```

* **5.2** Paste the output. `--cached` removes the file from Git's tracking only; it stays on disk.

```bash
git commit -am "chore: stop tracking secrets.txt"
```

* **5.3** Paste the output. Find `delete mode`: the file is deleted **from the repository**, not from your disk.

```bash
git ls-files --others --exclude-standard
```

* **5.4** Paste the output: the files that are untracked and not ignored.

```bash
git status --ignored --short
```

* **5.5** Paste the output. The secrets file now shows as ignored (`!!`), because it is no longer tracked.

Finally, look at an existing repository. The lab folder is one: clone it from your disk and compare its layout with yours.

```bash
cd ..
git clone repo-creation-lab kestrel-sample
```

* **5.6** Paste the output of `git clone`. Then look around: `ls -a kestrel-sample` and `ls -a kestrel-vision` show the same
  pattern, a `.git` folder next to the project's own files.

```bash
git -C kestrel-sample log --oneline -5
```

* **5.7** Paste the output. The option `-C <folder>` runs Git as if you had gone into that folder: this is the history of the
  clone, one line per commit.
* Then type your answer to `ANSWER-3` in the file: you add a file that is **already tracked** to `.gitignore`. Does Git stop
  tracking it? Answer `yes` or `no`.

## Finish

```bash
cd ~/repo-creation-lab
python3 tests/grade.py
```

You want to see `PASS` for all five tasks and `TOTAL: 100/100`. Anything marked `FAIL` is listed with the reason; fix it and run
the grader again.

## Marks

| Task | Marks | How it is checked |
|---|---|---|
| 1 | 20 | the init message, `ls -a`, `ls .git` and `git status` are pasted; one answer; `kestrel-vision` is really a repository on branch `main` |
| 2 | 25 | the two `git status` outputs, the commit, the short status and the log are pasted; one answer; the first commit really holds the two files with the given contents, and your commits carry your identity |
| 3 | 20 | the short status, the file, the commit and the log are pasted; the `.gitignore` commit really holds the exact 12 lines |
| 4 | 15 | the three status and check outputs are pasted; the ignored file and the untracked note are really there |
| 5 | 20 | `ls-files`, `rm --cached`, the commit, the status and the clone are pasted; one answer; the secrets file is really untracked but still on disk, and `kestrel-sample` is really a clone |

A task shows **PASS** only when every check in it passes, and you earn marks for each check that passes even if the task as a
whole fails.

## If something goes wrong

* **You skipped a task and a later one fails.** Run the catch-up box at the start of the task after the one you skipped (in
  order, if you skipped several), then carry on.
* **`Author identity unknown` / `Please tell me who you are` when you commit.** Your name and email are not set: run the two
  `git config --global` lines in "What you need", then run the `git commit` again.
* **A commit prints `Your name and email address were configured automatically based on your username and hostname`.** Your
  name and email were **not** set, so Git made up an identity, and the grader will not accept it. Run the two `git config --global`
  lines in "What you need", delete the folder (`cd ~`, then `rm -rf kestrel-vision`, only that folder) and start again with Task 1.
* **`fatal: not a git repository`.** You are not inside `~/kestrel-vision`: run `cd ~/kestrel-vision`. If `git status` works in the
  wrong folder, you created the project inside another repository: go to `~`, and start again with Task 1.
* **`git init` says `Reinitialized existing Git repository`.** The folder was already a repository. That is harmless: carry on.
* **Step 1.4 says `On branch master`.** You left out `-b main`. Delete the folder (`cd ~`, then `rm -rf kestrel-vision` if you are sure
  it is the new empty one) and start Task 1 again, or run `git branch -m main` in it.
* **Step 2.1 lists `data/` and `docs/` too.** You put a file in them. Leave them empty: the point is that Git does not track empty
  folders.
* **A heredoc (the `cat > .gitignore << 'EOF'` block) seems to hang, or the prompt shows `>`.** Git is not involved: the shell is
  still waiting for the line `EOF`. Type `EOF` alone on a line and press `Enter`. If the file is wrong, type the block again: it
  replaces the file.
* **Step 4.1 lists `data/` or the `.csv` file.** `.gitignore` is missing a line or was not saved: compare `cat .gitignore` with
  Task 3, fix it and make a new commit.
* **Step 5.1 does not list `src/secrets.txt`.** You ran `git rm --cached` already, or never committed the file: run the four lines
  of "First the mistake" again, but only if `ls src` does not show `secrets.txt`.
* **`error: pathspec 'src/secrets.txt' did not match any files known to git`.** The file is not tracked: see the line above.
* **An editor opened and asked for a commit message.** You left out `-m "..."`. Save and exit (nano: `Ctrl+O`, `Enter`, `Ctrl+X`; vim:
  `Esc`, then `:wq` and `Enter`). Then fix the message with `git commit --amend -m "<the message from the step>"`.
* **`tests/grade.py` says it cannot find the project.** The project must be `~/kestrel-vision`, next to `repo-creation-lab`.
