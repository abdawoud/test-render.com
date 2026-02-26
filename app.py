from flask import Flask, request, jsonify
import random
import string

app = Flask(__name__)

@app.route("/")
def index():
    serial = request.args.get("serial")
    challenge = request.args.get("challenge")

    if not serial or not challenge:
        return jsonify({"error": "Missing 'serial' and/or 'challenge' parameter"}), 400

    response_code = ''.join(random.choices(string.digits, k=8))

    return jsonify({
        "serial": serial,
        "challenge": challenge,
        "response": response_code
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
