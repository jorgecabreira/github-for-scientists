import csv
import json
import random
import re
import webbrowser
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

N_TRIALS = 5
MIN_BAR_LENGTH = 180
MAX_BAR_LENGTH = 240
MIN_DIFFERENCE = 10
MAX_DIFFERENCE = 25
testing_SJ
# ==================================================
# WORKSHOP TASKS — EDIT ONLY THESE EIGHT FUNCTIONS
# ==================================================

# TASK 0 (LIVE DEMO): Change the color of the bars.
def get_bar_color():
    return "black"  # TODO: try "royalblue"


# TASK 1: Ask for the participant's name.
def get_participant_id():
    return "unknown"  # TODO: replace with input(...)


# TASK 2: Ask for the experimenter's name.
def get_experimenter_id():
    return "unknown"  # TODO: replace with input(...)


# TASK 3: Generate the start timestamp automatically.
def get_session_datetime():
    return "unknown"  # TODO: use datetime.now().strftime("%Y%m%d%H%M%S%f")[:17]


# TASK 4: Complete the missing row inside the CSV writer.
def save_results(results, participant_id, experimenter_id, session_datetime):
    # The output folder and file handling are already implemented.
    Path("results").mkdir(exist_ok=True)
    safe_id = re.sub(r"[^A-Za-z0-9_-]", "_", participant_id).strip("_") or "unknown"
    filename = Path("results") / f"{safe_id}_{datetime.now():%Y%m%d_%H%M%S_%f}.csv"
    with filename.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            "participant_id", "experimenter_id", "session_datetime",
            "trial", "left_length", "right_length", "response",
            "correct", "reaction_time_ms",
        ])
        for trial in results:
            # TODO: replace pass with writer.writerow([...]) using these values:
            # participant_id, experimenter_id, session_datetime,
            # trial["trial"], trial["left_length"], trial["right_length"],
            # trial["response"], trial["correct"], trial["reaction_time_ms"]
            pass
    print(f"Results file: {filename.resolve()}")


# TASK 5: Return 'green' for correct and 'red' for incorrect responses.
def get_feedback_color(correct):
    return "black"  # TODO: use if / else


# TASK 6: Change the written instructions displayed above the choices.
def get_instructions():
    return "Which bar is longer?"  # TODO: replace the text


# TASK 7: Choose a difficulty and define the bar-length difference.
def get_difficulty():
    # TODO: Ask the experimenter to choose easy, normal, or hard.
    # TODO: Return the bar-length difference range for that choice:
    # easy: (30, 45), normal: (10, 25), hard: (3, 8)
    # For any unrecognized choice, use normal difficulty.
    return (MIN_DIFFERENCE, MAX_DIFFERENCE)


# ==================================================
# EXPERIMENT ENGINE — NO EDITS REQUIRED
# ==================================================

PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Visual Discrimination Task</title>
<style>
body { font-family: Arial, sans-serif; text-align: center; margin-top: 60px; background: #f5f5f5; }
#experiment { max-width: 850px; margin: auto; }
#stimuli { display: flex; justify-content: center; align-items: center; gap: 100px; margin-top: 70px; margin-bottom: 35px; min-height: 120px; }
.stimulus { width: 300px; }
.bar { height: 65px; background: #222; margin: auto; }
.label { margin-top: 15px; font-size: 18px; }
button { font-size: 20px; padding: 12px 35px; margin: 10px; cursor: pointer; }
#feedback { margin-top: 30px; font-size: 22px; }
#summary { font-size: 22px; line-height: 1.8; }
</style>
</head>
<body>
<div id="experiment">
<h1>Visual Discrimination Task</h1>
<p id="trialNumber"></p>
<div id="stimuli">
  <div class="stimulus"><div id="leftBar" class="bar"></div><div class="label">LEFT</div></div>
  <div class="stimulus"><div id="rightBar" class="bar"></div><div class="label">RIGHT</div></div>
</div>
<p id="question">Which bar is longer?</p>
<button id="leftButton">LEFT</button><button id="rightButton">RIGHT</button>
<div id="feedback"></div><div id="summary"></div>
</div>
<script>
let trialStart = null;
let busy = false;
const leftButton = document.getElementById("leftButton");
const rightButton = document.getElementById("rightButton");
async function loadTrial() {
  const response = await fetch("/trial");
  const data = await response.json();
  if (!response.ok) { document.getElementById("feedback").textContent = data.error; return; }
  document.getElementById("trialNumber").textContent = `Trial ${data.trial} / ${data.total_trials}`;
  document.getElementById("leftBar").style.backgroundColor = data.bar_color;
  document.getElementById("rightBar").style.backgroundColor = data.bar_color;
  document.getElementById("question").textContent = data.instructions;
  document.getElementById("leftBar").style.width = `${data.left_length}px`;
  document.getElementById("rightBar").style.width = `${data.right_length}px`;
  document.getElementById("feedback").textContent = "";
  leftButton.disabled = false;
  rightButton.disabled = false;
  busy = false;
  trialStart = performance.now();
}
async function submitResponse(choice) {
  if (busy || trialStart === null) return;
  busy = true;
  leftButton.disabled = true;
  rightButton.disabled = true;
  const reactionTime = performance.now() - trialStart;
  try {
    const response = await fetch("/response", {
      method: "POST", headers: {"Content-Type": "application/json"},
      body: JSON.stringify({response: choice, reaction_time_ms: reactionTime})
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Request failed");
    const feedback = document.getElementById("feedback");
    feedback.style.color = data.feedback_color;
    feedback.textContent = `${data.correct ? "Correct" : "Incorrect"} — ${data.reaction_time_ms} ms`;
    if (data.finished) {
      setTimeout(() => {
        document.getElementById("stimuli").style.display = "none";
        document.getElementById("question").style.display = "none";
        leftButton.style.display = "none";
        rightButton.style.display = "none";
        document.getElementById("trialNumber").textContent = "Experiment finished";
        feedback.textContent = "";
        document.getElementById("summary").textContent =
          `Correct responses: ${data.summary.n_correct} / ${data.summary.n_trials} | Mean reaction time: ${data.summary.mean_rt} ms`;
      }, 700);
    } else {
      setTimeout(loadTrial, 700);
    }
  } catch (err) {
    document.getElementById("feedback").textContent = err.message;
  }
}
leftButton.addEventListener("click", () => submitResponse("L"));
rightButton.addEventListener("click", () => submitResponse("R"));
loadTrial();
</script>
</body>
</html>"""


def create_stimulus():
    # The workshop function already selects the difference range.
    min_diff, max_diff = ExperimentHandler.difficulty
    shorter = random.randint(MIN_BAR_LENGTH, MAX_BAR_LENGTH - max_diff)
    difference = random.randint(min_diff, max_diff)
    longer = shorter + difference
    if random.choice(["L", "R"]) == "L":
        return {"left_length": longer, "right_length": shorter, "correct_response": "L"}
    return {"left_length": shorter, "right_length": longer, "correct_response": "R"}


def experiment_summary(results):
    return {
        "n_correct": sum(result["correct"] for result in results),
        "n_trials": len(results),
        "mean_rt": round(sum(r["reaction_time_ms"] for r in results) / len(results), 1),
    }


class ExperimentHandler(BaseHTTPRequestHandler):
    # This simple server is intentionally single-session, localhost-only.
    results = []
    current_trial = None
    finished = False
    participant_id = "unknown"
    experimenter_id = "unknown"
    session_datetime = "unknown"
    difficulty = (MIN_DIFFERENCE, MAX_DIFFERENCE)

    def send_json(self, data, status=200):
        message = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(message)))
        self.end_headers()
        self.wfile.write(message)

    def do_GET(self):
        cls = type(self)
        if self.path == "/":
            page = PAGE.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(page)))
            self.end_headers()
            self.wfile.write(page)
        elif self.path == "/trial":
            if cls.finished:
                self.send_json({"error": "Session finished; restart Python to begin another."}, 409)
                return
            if cls.current_trial is None:
                cls.current_trial = create_stimulus()
            self.send_json({
                "trial": len(cls.results) + 1,
                "total_trials": N_TRIALS,
                "bar_color": get_bar_color(),
                "instructions": get_instructions(),
                "left_length": cls.current_trial["left_length"],
                "right_length": cls.current_trial["right_length"],
            })
        else:
            self.send_json({"error": "Not found"}, 404)

    def do_POST(self):
        cls = type(self)
        if self.path != "/response":
            self.send_json({"error": "Not found"}, 404)
            return
        if cls.current_trial is None or cls.finished:
            self.send_json({"error": "No active trial"}, 409)
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if size > 10240 or size <= 0:
                raise ValueError("Invalid request size")
            data = json.loads(self.rfile.read(size))
            choice = data["response"]
            if choice not in ("L", "R"):
                raise ValueError("Invalid response")
            reaction_time = round(float(data["reaction_time_ms"]), 1)
            if not 0 <= reaction_time < 1000000:
                raise ValueError("Invalid reaction time")
        except (ValueError, KeyError, TypeError, json.JSONDecodeError):
            self.send_json({"error": "Invalid trial data"}, 400)
            return
        current = cls.current_trial
        cls.current_trial = None
        correct = choice == current["correct_response"]
        cls.results.append({
            "trial": len(cls.results) + 1,
            "left_length": current["left_length"],
            "right_length": current["right_length"],
            "response": choice,
            "correct": correct,
            "reaction_time_ms": reaction_time,
        })
        finished = len(cls.results) >= N_TRIALS
        reply = {
            "correct": correct,
            "reaction_time_ms": reaction_time,
            "finished": finished,
            "feedback_color": get_feedback_color(correct),
        }
        if finished:
            cls.finished = True
            reply["summary"] = experiment_summary(cls.results)
            save_results(cls.results, cls.participant_id, cls.experimenter_id, cls.session_datetime)
        self.send_json(reply)

    def log_message(self, format, *args):
        return


def run_experiment():
    ExperimentHandler.results = []
    ExperimentHandler.current_trial = None
    ExperimentHandler.finished = False
    ExperimentHandler.participant_id = get_participant_id()
    ExperimentHandler.experimenter_id = get_experimenter_id()
    ExperimentHandler.session_datetime = get_session_datetime()
    ExperimentHandler.difficulty = get_difficulty()
    server = ThreadingHTTPServer(("127.0.0.1", 0), ExperimentHandler)
    url = f"http://127.0.0.1:{server.server_address[1]}"
    print("\nVISUAL DISCRIMINATION TASK")
    print("Opening experiment in your browser:", url)
    print("After the experiment, press Ctrl+C in the terminal to stop the server.")
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nExperiment closed.")
    finally:
        server.server_close()


if __name__ == "__main__":
    run_experiment()
