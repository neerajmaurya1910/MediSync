# Learning Sapling by building MediSync

The idea: build MediSync as a **stack of small commits**, one per step, and learn one
new Sapling skill at each milestone. Run every command from inside the `medisync` folder.

Cheat sheet you will use all the time:
```bash
sl             # smartlog: where am I?
sl status      # what changed?
sl diff        # exact changes not yet committed
sl web         # visual smartlog in the browser (great for screenshots)
```

---

## Milestone 0: Look at what you copied in
```bash
sl status                 # new files show as ?, edited README/.gitignore show as M
sl diff README.md .gitignore
```
The old `.gitkeep` placeholders are no longer needed:
```bash
sl rm docs/.gitkeep server/.gitkeep client/.gitkeep shared/.gitkeep
```
(If one of them doesn't exist, skip that one.)

**Skill: reading changes** (`status`, `diff`).

---

## Milestone 1: Commit in small pieces (a stack)
Instead of one giant commit, commit one part at a time by naming the paths:
```bash
sl add shared/
sl commit -m "Add shared data models and triage scoring" shared/ 

sl add tests/__init__.py tests/test_triage.py
sl commit -m "Add triage tests" tests/__init__.py tests/test_triage.py

sl add server/__init__.py server/store.py tests/test_store.py
sl commit -m "Add versioned patient store" server/__init__.py server/store.py tests/test_store.py

sl add server/app.py tests/test_api.py
sl commit -m "Add HTTP API server" server/app.py tests/test_api.py

sl add client/
sl commit -m "Add device CLI with offline cache" client/

sl add docs/
sl commit -m "Add README, docs and gitignore"
```
The last commit has no paths, so it takes everything still left (README, .gitignore,
docs, and the removed `.gitkeep` files).

Look at your stack:
```bash
sl          # a chain of 6 commits, @ marks where you are
```
Run the tests before pushing: `python3 -m unittest discover -v`

**Skill: stacked commits and partial commits by path.**

---

## Milestone 2: Push your first stack
```bash
sl push --to main
```
Open GitHub and check the commits page: you should see 6 separate commits.

**Skill: pushing.** Take an `sl` / `sl web` screenshot for your report.

---

## Milestone 3: Move around the stack
```bash
sl prev       # go to the parent commit (your files change to that moment!)
sl prev
sl next       # come back up
sl goto main  # jump back to the top
```
Use `sl` after each move and watch `@`.

**Skill: navigating history.**

---

## Milestone 4: Fix a mistake in an old commit
Only rewrite commits you have **not pushed**. Once pushed, make a new commit instead,
so practise this on the Milestone 5 commits before you push them.
```bash
# edit a file in VS Code, e.g. improve a docstring
sl diff
sl amend                 # fold the change into the current commit
```
If commits above look detached in `sl`, run `sl restack`.

Other useful fixes:
```bash
sl metaedit              # rewrite the commit message
sl absorb                # after editing several files, auto-fold each change into the right earlier commit
sl undo                  # reverse your last Sapling action
sl uncommit              # un-commit but keep your file edits
sl revert <file>         # throw away unsaved edits to a file
```
**Skill: rewriting history safely** (Sapling's biggest strength over plain Git).

---

## Milestone 5: Add a feature as a new stack
Feature idea: a `discharge` command that removes a patient from the queue.
```bash
sl goto main
# 1) add a "status" field to Patient in shared/models.py
sl commit -m "Add status field to Patient"
# 2) handle discharge in server/store.py + a test
sl commit -m "Store: support discharging a patient"
# 3) add a CLI command in client/cli.py
sl commit -m "CLI: add discharge command"
sl push --to main
```
Other feature ideas: SQLite storage, editing a patient's vitals, a web dashboard.

**Skill: feature work as small reviewable commits.**

Combine or split when needed:
```bash
sl fold --from .^    # merge current commit with its parent
sl split             # split one big commit into smaller ones (interactive)
sl hide <commit>     # remove a commit you don't want
```

---

## Milestone 6: Working with teammates
Start every session:
```bash
sl status
sl pull
sl goto main
```
If you have local commits and your teammate pushed too:
```bash
sl pull
sl rebase -d main     # place your commits on top of theirs
sl push --to main
```
For a conflict: fix the file in VS Code, then `sl resolve --mark <file>` and `sl rebase --continue`.

Useful investigation commands:
```bash
sl blame shared/triage.py      # who wrote each line
sl log shared/triage.py        # history of one file
sl show <commit>               # what one commit changed
```

---

## Habits checklist
- [ ] `sl pull` before starting work
- [ ] One idea per commit, clear message
- [ ] Tests pass (`python3 -m unittest discover`) before `sl push`
- [ ] Screenshot `sl` / `sl web` after each milestone for your report

## Evidence to collect for your report
1. `sl` smartlog showing the 6-commit stack (Milestone 1)
2. `sl web` screenshot
3. GitHub commits page (Milestone 2)
4. Before/after `sl` around an `sl amend` (Milestone 4)
5. `sl paths` output and the `.sl` folder in VS Code
