# GitHub Workshop: Collaborative Visual Discrimination Experiment

Work in pairs to improve a real, running Python experiment using Git and GitHub. **No extra Python packages** are needed.

## Start the program

```bash
python experiment.py
```

Use `python3 experiment.py` if necessary. Answer any questions in the terminal, then use the task in your browser. Stop with **Ctrl+C** after the five trials. Restart Python for a new session. Use fictional participant names; exported `results/` files are excluded from Git.

## Eight tiny edits: one demo and seven participant exercises

**Edit only the functions in the WORKSHOP TASKS section at the top of `experiment.py`.** All browser/server integration is provided. Every task can be accomplished by modifying a few lines.

| Task | Goal | What to change |
|---|---|---|
| **0 — Instructor demo (A)** | Change the bars to blue | In `get_bar_color()`, return `"royalblue"` instead of `"black"`. |
| **1** | Ask for participant name | In `get_participant_id()`, use `input("Participant name: ")`. |
| **2** | Ask for experimenter name | In `get_experimenter_id()`, use `input("Experimenter name: ")`. |
| **3** | Record session start time | In `get_session_datetime()`, return `datetime.now().strftime("%Y%m%d%H%M%S%f")[:17]`. This produces `YYYYMMDDHHMMSSmmm`. |
| **4** | Save the data in CSV | Replace `pass` with `writer.writerow([...])` using the nine values listed in the comment, in the header order. File creation is provided. |
| **5** | Show red/green feedback | Make `get_feedback_color(correct)` return `"green"` if correct, otherwise `"red"`. |
| **6 (D)** | Change experiment instructions | In `get_instructions()`, return a new instruction string, such as `"Select the longer bar."`. |
| **7 (F)** | Choose difficulty | In `get_difficulty()`, ask the experimenter for a difficulty using `input(...)`, then use `if` / `elif` / `else` to return the corresponding range. |

The starter version does not ask for difficulty yet. **Complete the function itself** so it returns `(30, 45)` for easy, `(3, 8)` for hard, and `(10, 25)` for normal or an unrecognized choice. The experiment engine uses the returned pair without any difficulty rules of its own.

## GitHub workflow for pairs

Use a separate local clone per person and create a **new branch for each change**.

```bash
git clone <repository-url>
cd <repository-folder>
git switch -c task-1-participant
# Edit the assigned function.
git status
git add experiment.py
git commit -m "Ask for participant name"
git push -u origin task-1-participant
```

Open a pull request on GitHub; your partner reviews and merges it. Before starting another task:

```bash
git switch main
git pull origin main
git switch -c task-3-timestamp
```

Suggested division: A completes Tasks 1, 3, 5, 7; B completes Tasks 2, 4, 6. Both partners should review PRs and run the final program.

**Important:** The instructor's Task 0 change should be committed to `main` before participants create their task branches.
