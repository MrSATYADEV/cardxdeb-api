import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

# -------- Keyword rules --------
POSITIVE = [
    "success", "successful", "approved", "approve",
    "live", "valid", "passed", "ok", "done",
    "completed", "added"
]

NEGATIVE = [
    "error", "failed", "declined", "invalid",
    "dead", "blocked", "denied", "timeout",
    "exception", "not allowed"
]


def detect_status(text: str) -> str:
    t = text.lower()
    for w in POSITIVE:
        if w in t:
            return "APPROVED"
    for w in NEGATIVE:
        if w in t:
            return "DECLINED"
    return "DECLINED"


# -------- Health check (for Render + UptimeRobot) --------
@app.route("/health", methods=["GET"])
def health():
    return "ok", 200


# -------- Main API endpoint --------
@app.route("/cc", methods=["GET"])
def cc():
    user_input = request.args.get("input", "").strip()

    if not user_input:
        return jsonify({
            "status": "DECLINED",
            "output": "error: no input provided"
        })

    try:
        p = subprocess.run(
            ["python3", "b3.py", user_input],
            capture_output=True,
            text=True,
            timeout=120
        )

        output = ((p.stdout or "") + (p.stderr or "")).strip()
        status = detect_status(output)

        return jsonify({
            "status": status,
            "output": output
        })

    except Exception as e:
        return jsonify({
            "status": "DECLINED",
            "output": str(e)
        })


# -------- Local testing only --------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
