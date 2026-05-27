import pytest
from App import app, check_password, check_breach


# ── Pytest fixture: creates a test client for the Flask app ──────────────────
# This is the Python equivalent of supertest in Node.js.
# Every test function that has "client" as a parameter gets this automatically.

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ── Unit tests: check_password() ─────────────────────────────────────────────

class TestCheckPassword:

    def test_weak_password_has_low_score(self):
        result = check_password("abc")
        assert result["score"] < 3
        assert result["strong"] is False

    def test_strong_password_has_high_score(self):
        result = check_password("Secure#Pass99")
        assert result["score"] >= 4
        assert result["strong"] is True

    def test_weak_password_returns_feedback(self):
        result = check_password("abc")
        assert len(result["feedback"]) > 0

    def test_returns_a_label_string(self):
        result = check_password("abc")
        assert isinstance(result["label"], str)

    def test_raises_on_empty_string(self):
        with pytest.raises(ValueError):
            check_password("")

    def test_raises_on_non_string(self):
        with pytest.raises(ValueError):
            check_password(12345)

    def test_all_rules_pass_for_strong_password(self):
        result = check_password("Secure#Pass99")
        assert result["feedback"] == []


# ── Unit tests: check_breach() ────────────────────────────────────────────────

class TestCheckBreach:

    def test_detects_known_breached_email(self):
        result = check_breach("test@example.com")
        assert result["breached"] is True
        assert result["details"]["severity"] == "HIGH"

    def test_returns_not_breached_for_safe_email(self):
        result = check_breach("safe@clean.com")
        assert result["breached"] is False

    def test_is_case_insensitive(self):
        result = check_breach("TEST@EXAMPLE.COM")
        assert result["breached"] is True

    def test_raises_on_invalid_email(self):
        with pytest.raises(ValueError):
            check_breach("notanemail")

    def test_raises_on_empty_string(self):
        with pytest.raises(ValueError):
            check_breach("")


# ── Integration tests: API endpoints ─────────────────────────────────────────

class TestHealthEndpoint:

    def test_returns_200_with_up_status(self, client):
        res = client.get("/health")
        assert res.status_code == 200
        assert res.get_json()["status"] == "UP"


class TestPasswordEndpoint:

    def test_returns_result_for_valid_password(self, client):
        res = client.post("/api/password/check",
                          json={"password": "Secure#Pass99"})
        assert res.status_code == 200
        body = res.get_json()
        assert body["success"] is True
        assert "score" in body["result"]
        assert "label" in body["result"]

    def test_returns_400_when_password_missing(self, client):
        res = client.post("/api/password/check", json={})
        assert res.status_code == 400

    def test_flags_weak_password(self, client):
        res = client.post("/api/password/check", json={"password": "abc"})
        assert res.status_code == 200
        assert res.get_json()["result"]["strong"] is False


class TestBreachEndpoint:

    def test_detects_breached_email(self, client):
        res = client.post("/api/breach/check",
                          json={"email": "admin@test.com"})
        assert res.status_code == 200
        assert res.get_json()["result"]["breached"] is True

    def test_returns_not_breached_for_safe_email(self, client):
        res = client.post("/api/breach/check",
                          json={"email": "nobody@safe.com"})
        assert res.get_json()["result"]["breached"] is False

    def test_returns_400_when_email_missing(self, client):
        res = client.post("/api/breach/check", json={})
        assert res.status_code == 400


class TestNotFound:

    def test_unknown_route_returns_404(self, client):
        res = client.get("/api/doesnotexist")
        assert res.status_code == 404