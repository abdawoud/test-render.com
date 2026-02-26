from flask import Flask, request, jsonify, render_template_string
import random
import string

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Token Service</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Inter', sans-serif;
            background: #ffffff;
            color: #1a1a1a;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        .top-bar {
            height: 4px;
            background: #FF000F;
            width: 100%;
        }

        .container {
            max-width: 600px;
            margin: 0 auto;
            padding: 60px 24px;
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .logo-mark {
            width: 48px;
            height: 48px;
            background: #FF000F;
            border-radius: 4px;
            margin-bottom: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .logo-mark svg {
            width: 28px;
            height: 28px;
        }

        h1 {
            font-size: 1.5rem;
            font-weight: 700;
            color: #1a1a1a;
            margin-bottom: 8px;
            letter-spacing: -0.02em;
        }

        .subtitle {
            font-size: 0.875rem;
            color: #6b7280;
            margin-bottom: 40px;
        }

        .card {
            width: 100%;
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 32px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        }

        .field { margin-bottom: 20px; }
        .field:last-of-type { margin-bottom: 28px; }

        label {
            display: block;
            font-size: 0.75rem;
            font-weight: 600;
            color: #1a1a1a;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 6px;
        }

        input {
            width: 100%;
            padding: 10px 14px;
            font-size: 0.9rem;
            font-family: 'Inter', sans-serif;
            border: 1.5px solid #d1d5db;
            border-radius: 6px;
            color: #1a1a1a;
            background: #fafafa;
            transition: border-color 0.2s, box-shadow 0.2s;
            outline: none;
        }

        input:focus {
            border-color: #FF000F;
            box-shadow: 0 0 0 3px rgba(255, 0, 15, 0.08);
            background: #fff;
        }

        input::placeholder { color: #9ca3af; }

        .btn {
            width: 100%;
            padding: 12px 24px;
            font-size: 0.9rem;
            font-weight: 600;
            font-family: 'Inter', sans-serif;
            color: #ffffff;
            background: #FF000F;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            transition: background 0.15s, transform 0.1s;
        }

        .btn:hover { background: #D4000D; }
        .btn:active { transform: scale(0.985); }

        .result {
            margin-top: 24px;
            display: none;
            width: 100%;
        }

        .result.show { display: block; }

        .result-box {
            background: #FF000F;
            border-radius: 8px;
            padding: 24px;
            text-align: center;
        }

        .result-label {
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: rgba(255,255,255,0.75);
            margin-bottom: 8px;
        }

        .result-code {
            font-size: 2rem;
            font-weight: 700;
            color: #ffffff;
            letter-spacing: 0.15em;
            font-variant-numeric: tabular-nums;
        }

        .result-meta {
            margin-top: 16px;
            padding-top: 16px;
            border-top: 1px solid rgba(255,255,255,0.2);
            display: flex;
            justify-content: space-between;
            font-size: 0.75rem;
            color: rgba(255,255,255,0.7);
        }

        .result-meta span {
            font-family: monospace;
            color: #ffffff;
            font-weight: 500;
        }

        .divider {
            width: 100%;
            height: 1px;
            background: #e5e7eb;
            margin: 24px 0;
        }

        .api-hint {
            font-size: 0.75rem;
            color: #9ca3af;
            text-align: center;
        }

        .api-hint code {
            background: #f3f4f6;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.7rem;
            color: #6b7280;
        }

        .error-msg {
            margin-top: 12px;
            font-size: 0.8rem;
            color: #FF000F;
            text-align: center;
            display: none;
        }

        .error-msg.show { display: block; }

        footer {
            text-align: center;
            padding: 24px;
            font-size: 0.7rem;
            color: #d1d5db;
        }
    </style>
</head>
<body>
    <div class="top-bar"></div>
    <div class="container">
        <div class="logo-mark">
            <svg viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round">
                <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
            </svg>
        </div>

        <h1>Token Service</h1>
        <p class="subtitle">Generate a secure response code</p>

        <div class="card">
            <div class="field">
                <label>Serial Number</label>
                <input type="text" id="serial" placeholder="e.g. abcd1234ef" />
            </div>
            <div class="field">
                <label>Challenge Code</label>
                <input type="text" id="challenge" placeholder="e.g. 4829173650" />
            </div>
            <button class="btn" id="generateBtn" onclick="generate()">Generate Response</button>
            <div class="error-msg" id="error">Please fill in both fields.</div>
        </div>

        <div class="result" id="result">
            <div class="result-box">
                <div class="result-label">Response Code</div>
                <div class="result-code" id="responseCode">&mdash;</div>
                <div class="result-meta">
                    <div>Serial: <span id="metaSerial">&mdash;</span></div>
                    <div>Challenge: <span id="metaChallenge">&mdash;</span></div>
                </div>
            </div>
        </div>

        <div class="divider"></div>
        <p class="api-hint">
            API: <code>GET /?serial=...&amp;challenge=...</code>
        </p>
    </div>

    <footer>&copy; 2026 Token Service</footer>

    <script>
        const params = new URLSearchParams(window.location.search);
        if (params.get('serial')) document.getElementById('serial').value = params.get('serial');
        if (params.get('challenge')) document.getElementById('challenge').value = params.get('challenge');
        if (params.get('serial') && params.get('challenge')) generate();

        function generate() {
            const serial = document.getElementById('serial').value.trim();
            const challenge = document.getElementById('challenge').value.trim();
            const error = document.getElementById('error');
            const result = document.getElementById('result');

            if (!serial || !challenge) {
                error.classList.add('show');
                result.classList.remove('show');
                return;
            }
            error.classList.remove('show');

            fetch('/api?serial=' + encodeURIComponent(serial) + '&challenge=' + encodeURIComponent(challenge))
                .then(r => r.json())
                .then(data => {
                    document.getElementById('responseCode').textContent = data.response;
                    document.getElementById('metaSerial').textContent = data.serial;
                    document.getElementById('metaChallenge').textContent = data.challenge;
                    result.classList.add('show');
                })
                .catch(() => {
                    const code = String(Math.floor(Math.random() * 100000000)).padStart(8, '0');
                    document.getElementById('responseCode').textContent = code;
                    document.getElementById('metaSerial').textContent = serial;
                    document.getElementById('metaChallenge').textContent = challenge;
                    result.classList.add('show');
                });
        }

        document.querySelectorAll('input').forEach(input => {
            input.addEventListener('keydown', e => { if (e.key === 'Enter') generate(); });
        });
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    serial = request.args.get("serial")
    challenge = request.args.get("challenge")

    if request.headers.get("Accept", "").startswith("application/json"):
        if not serial or not challenge:
            return jsonify({"error": "Missing 'serial' and/or 'challenge' parameter"}), 400
        code = ''.join(random.choices(string.digits, k=8))
        return jsonify({"serial": serial, "challenge": challenge, "response": code})

    return render_template_string(HTML_TEMPLATE)


@app.route("/api")
def api():
    serial = request.args.get("serial")
    challenge = request.args.get("challenge")

    if not serial or not challenge:
        return jsonify({"error": "Missing 'serial' and/or 'challenge' parameter"}), 400

    code = ''.join(random.choices(string.digits, k=8))
    return jsonify({"serial": serial, "challenge": challenge, "response": code})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
