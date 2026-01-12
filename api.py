from flask import Flask, request, jsonify
from b3 import run_b3

app = Flask(__name__)

# ---------------- HEALTH CHECK ----------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "cardxdeb-api"
    })


# ---------------- MAIN ENDPOINT ----------------
@app.route("/cc", methods=["GET"])
def cc():
    card_input = request.args.get("input")

    if not card_input:
        return jsonify({
            "status": "ERROR",
            "message": "input parameter missing"
        }), 400

    try:
        result = run_b3(card_input)
        return jsonify(result)

    except Exception as e:
        return jsonify({
            "status": "ERROR",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
