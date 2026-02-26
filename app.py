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
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: #FF000F;
            color: #1a1a1a;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }

        /* ========== SSO SCREEN ========== */
        .sso-screen {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 40px 24px;
            transition: opacity 0.4s ease, transform 0.4s ease;
        }

        .sso-screen.hide {
            opacity: 0;
            transform: scale(0.96);
            pointer-events: none;
        }

        .sso-icon {
            width: 48px;
            height: 48px;
            margin-bottom: 28px;
        }

        .sso-icon svg {
            width: 48px;
            height: 48px;
            fill: rgba(255,255,255,0.85);
        }

        .sso-card {
            background: #ffffff;
            border-radius: 16px;
            padding: 44px 36px;
            max-width: 400px;
            width: 100%;
            text-align: center;
            box-shadow: 0 12px 40px rgba(0,0,0,0.15);
        }

        .app-icon {
            width: 60px;
            height: 60px;
            background: #FF000F;
            border-radius: 14px;
            margin: 0 auto 24px auto;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 12px rgba(255,0,15,0.3);
        }

        .app-icon svg {
            width: 30px;
            height: 30px;
        }

        .sso-title {
            font-size: 1.3rem;
            font-weight: 600;
            color: #1a1a1a;
            margin-bottom: 10px;
        }

        .sso-title strong {
            font-weight: 700;
            color: #FF000F;
        }

        .sso-subtitle {
            font-size: 0.84rem;
            color: #6b7280;
            margin-bottom: 32px;
            line-height: 1.6;
        }

        .sso-btn {
            width: 100%;
            padding: 14px 48px;
            font-size: 0.95rem;
            font-weight: 600;
            font-family: 'Inter', sans-serif;
            color: #ffffff;
            background: #FF000F;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            transition: background 0.15s, transform 0.1s;
        }

        .sso-btn:hover {
            background: #D4000D;
        }

        .sso-btn:active {
            transform: scale(0.985);
        }

        .sso-footer {
            margin-top: 20px;
            font-size: 0.68rem;
            color: rgba(255,255,255,0.5);
        }

        /* ========== LOADING ========== */
        .loading-screen {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: #FF000F;
            display: none;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 5;
        }

        .loading-screen.show {
            display: flex;
        }

        .spinner {
            width: 40px;
            height: 40px;
            border: 4px solid rgba(255,255,255,0.25);
            border-top: 4px solid #ffffff;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .loading-text {
            margin-top: 16px;
            font-size: 0.8rem;
            color: rgba(255,255,255,0.7);
            font-weight: 500;
        }

        /* ========== RESULT SCREEN ========== */
        .result-screen {
            display: none;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 40px 24px;
            opacity: 0;
            transform: translateY(12px);
            transition: opacity 0.5s ease, transform 0.5s ease;
        }

        .result-screen.show {
            display: flex;
            background: #ffffff;
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
        }

        .result-screen.visible {
            opacity: 1;
            transform: translateY(0);
        }

        .top-bar {
            position: fixed;
            top: 0;
            left: 0;
            height: 4px;
            background: #FF000F;
            width: 100%;
            z-index: 10;
            display: none;
        }

        .top-bar.show {
            display: block;
        }

        .result-box {
            width: 100%;
            max-width: 420px;
            background: #FF000F;
            border-radius: 14px;
            padding: 40px 32px;
            text-align: center;
            box-shadow: 0 12px 40px rgba(255, 0, 15, 0.2);
        }

        .result-label {
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            color: rgba(255,255,255,0.7);
            margin-bottom: 12px;
        }

        .result-code {
            font-size: 2.8rem;
            font-weight: 700;
            color: #ffffff;
            letter-spacing: 0.18em;
            font-variant-numeric: tabular-nums;
            margin-bottom: 20px;
        }

        .result-divider {
            width: 60%;
            margin: 0 auto 20px auto;
            height: 1px;
            background: rgba(255,255,255,0.25);
        }

        .result-meta {
            display: flex;
            flex-direction: column;
            gap: 8px;
            font-size: 0.78rem;
            color: rgba(255,255,255,0.65);
        }

        .result-meta-row {
            display: flex;
            justify-content: center;
            gap: 8px;
        }

        .result-meta-row span {
            color: #ffffff;
            font-weight: 600;
            font-family: 'Courier New', monospace;
        }

        .result-timestamp {
            margin-top: 24px;
            font-size: 0.7rem;
            color: rgba(255,255,255,0.45);
        }

        .regenerate-btn {
            margin-top: 24px;
            padding: 10px 28px;
            font-size: 0.8rem;
            font-weight: 600;
            font-family: 'Inter', sans-serif;
            color: #FF000F;
            background: #ffffff;
            border: 2px solid #FF000F;
            border-radius: 8px;
            cursor: pointer;
            transition: background 0.15s, transform 0.1s;
        }

        .regenerate-btn:hover {
            background: #fff5f5;
        }

        .regenerate-btn:active {
            transform: scale(0.97);
        }

        /* ========== ERROR ========== */
        .error-screen {
            display: none;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 40px 24px;
            text-align: center;
        }

        .error-screen.show {
            display: flex;
        }

        .error-card {
            background: #ffffff;
            border-radius: 16px;
            padding: 40px 32px;
            max-width: 400px;
            width: 100%;
            box-shadow: 0 12px 40px rgba(0,0,0,0.15);
        }

        .error-icon {
            width: 50px;
            height: 50px;
            background: #fff0f0;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 16px auto;
            font-size: 1.3rem;
            font-weight: 700;
            color: #FF000F;
        }

        .error-title {
            font-size: 1.1rem;
            font-weight: 700;
            color: #1a1a1a;
            margin-bottom: 8px;
        }

        .error-text {
            font-size: 0.82rem;
            color: #6b7280;
            line-height: 1.6;
        }

        .error-text code {
            background: #f3f4f6;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 0.75rem;
            color: #374151;
        }
    </style>
</head>
<body>

    <div class="top-bar" id="topBar"></div>

    <!-- ERROR -->
    <div class="error-screen" id="errorScreen">
        <div class="error-card">
            <div class="error-icon">!</div>
            <div class="error-title">Missing Parameters</div>
            <div class="error-text">
                This service requires both <code>serial</code> and <code>challenge</code> parameters.<br><br>
                Example: <code>?serial=abcd1234ef&challenge=4829173650</code>
            </div>
        </div>
    </div>

    <!-- SSO SCREEN -->
    <div class="sso-screen" id="ssoScreen">
        <div class="sso-card">
            <div class="app-icon">
                <svg viewBox="0 0 24 24" fill="white">
                <path d="M12 1C8.676 1 6 3.676 6 7v2H4a1 1 0 00-1 1v11a1 1 0 001 1h16a1 1 0 001-1V10a1 1 0 00-1-1h-2V7c0-3.324-2.676-6-6-6zm-4 8V7c0-2.206 1.794-4 4-4s4 1.794 4 4v2H8zm5 6.722V18a1 1 0 11-2 0v-2.278a1.993 1.993 0 01-1-1.722 2 2 0 114 0c0 .738-.404 1.376-1 1.722z"/>
            </svg>
            </div>

            <div class="sso-title">Single sign-on to <strong>AssetManager</strong></div>
            <div class="sso-subtitle">Authenticate your account by logging into AssetManager's single sign-on provider.</div>

            <button class="sso-btn" onclick="authenticate()">Continue</button>
        </div>
    </div>

    <!-- LOADING -->
    <div class="loading-screen" id="loadingScreen">
        <div class="spinner"></div>
        <div class="loading-text">Authenticating...</div>
    </div>

    <!-- RESULT -->
    <div class="result-screen" id="resultScreen">
        <div class="result-box">
            <div class="result-label">Response Code</div>
            <div class="result-code" id="responseCode">&mdash;</div>
            <div class="result-divider"></div>
            <div class="result-meta">
                <div class="result-meta-row">
                    Serial: <span id="metaSerial">&mdash;</span>
                </div>
                <div class="result-meta-row">
                    Challenge: <span id="metaChallenge">&mdash;</span>
                </div>
            </div>
            <div class="result-timestamp" id="timestamp"></div>
        </div>
    </div>

    <script>
        const params = new URLSearchParams(window.location.search);
        const serial = params.get('serial');
        const challenge = params.get('challenge');

        if (!serial || !challenge) {
            document.getElementById('ssoScreen').style.display = 'none';
            document.getElementById('errorScreen').classList.add('show');
        }

        function authenticate() {
            document.getElementById('ssoScreen').classList.add('hide');

            setTimeout(() => {
                document.getElementById('ssoScreen').style.display = 'none';
                document.getElementById('loadingScreen').classList.add('show');
            }, 400);

            setTimeout(() => {
                fetchCode(() => {
                    document.getElementById('loadingScreen').classList.remove('show');
                    document.getElementById('topBar').classList.add('show');
                    const resultScreen = document.getElementById('resultScreen');
                    resultScreen.classList.add('show');
                    requestAnimationFrame(() => {
                        requestAnimationFrame(() => {
                            resultScreen.classList.add('visible');
                        });
                    });
                });
            }, 1500);
        }

        function fetchCode(callback) {
            fetch('/api?serial=' + encodeURIComponent(serial) + '&challenge=' + encodeURIComponent(challenge))
                .then(r => r.json())
                .then(data => {
                    showResult(data);
                    callback();
                })
                .catch(() => {
                    const code = String(Math.floor(Math.random() * 100000000)).padStart(8, '0');
                    showResult({ serial: serial, challenge: challenge, response: code });
                    callback();
                });
        }

        function showResult(data) {
            document.getElementById('responseCode').textContent = data.response;
            document.getElementById('metaSerial').textContent = data.serial;
            document.getElementById('metaChallenge').textContent = data.challenge;
            document.getElementById('timestamp').textContent = new Date().toLocaleString();
        }

        function regenerate() {
            fetchCode(() => {});
        }
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
