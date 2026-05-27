import os
import re
from flask import Flask, jsonify, request

app = Flask(__name__)

# ── Password strength checker ─────────────────────────────────────────────────
# Each rule adds 1 point to the score (max score = 5).
# This mirrors the Node.js version so the logic is easy to follow.

STRENGTH_LABELS = ["Very Weak", "Weak", "Fair", "Strong", "Very Strong"]


def check_password(password: str) -> dict:
    """
    Analyse a password and return a structured strength report.
    Raises ValueError if input is invalid.
    """
    if not password or not isinstance(password, str):
        raise ValueError("Password must be a non-empty string")

    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Use at least 8 characters")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add an uppercase letter")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add a lowercase letter")

    if re.search(r"[0-9]", password):
        score += 1
    else:
        feedback.append("Add a number")

    if re.search(r"[^A-Za-z0-9]", password):
        score += 1
    else:
        feedback.append("Add a special character")

    label = STRENGTH_LABELS[score - 1] if score > 0 else "Very Weak"

    return {
        "score": score,
        "label": label,
        "feedback": feedback,
        "strong": score >= 4,
    }


# ── Breach checker ────────────────────────────────────────────────────────────
# Simulated breach database (in a real system this would call HaveIBeenPwned).

BREACHED = {
    "test@example.com": {"source": "ExampleBreach2022", "severity": "HIGH"},
    "admin@test.com":   {"source": "AdminLeak2023",     "severity": "CRITICAL"},
    "user@leaked.com":  {"source": "LeakedDB2021",      "severity": "MEDIUM"},
}


def check_breach(email: str) -> dict:
    """
    Check whether an email appears in known breach records.
    Raises ValueError for invalid input.
    """
    if not email or "@" not in email:
        raise ValueError("Invalid email format")

    normalised = email.lower().strip()
    details = BREACHED.get(normalised)

    if details:
        return {
            "email": normalised,
            "breached": True,
            "details": details,
            "message": "Email found in a known breach!",
        }

    return {
        "email": normalised,
        "breached": False,
        "details": None,
        "message": "No breach records found.",
    }


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return jsonify({
        "status": "UP",
        "version": os.getenv("APP_VERSION", "1.0.0"),
    })


@app.post("/api/password/check")
def password_check():
    data = request.get_json(silent=True) or {}
    password = data.get("password")

    if not password:
        return jsonify({"error": "Password is required"}), 400

    try:
        result = check_password(password)
        return jsonify({"success": True, "result": result})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.post("/api/breach/check")
def breach_check():
    data = request.get_json(silent=True) or {}
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required"}), 400

    try:
        result = check_breach(email)
        return jsonify({"success": True, "result": result})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


# 404 handler
@app.errorhandler(404)
def not_found(e):
    return jsonify({"success": False, "message": "Endpoint not found"}), 404


if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    app.run(host="0.0.0.0", port=port)