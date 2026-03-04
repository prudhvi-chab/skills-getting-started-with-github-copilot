from fastapi.testclient import TestClient

from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success():
    email = "test@example.com"
    response = client.post(f"/activities/Chess%20Club/signup?email={email}")
    assert response.status_code == 200
    assert email in activities["Chess Club"]["participants"]
    assert "Signed up" in response.json().get("message", "")


def test_signup_duplicate():
    email = "michael@mergington.edu"
    # first signup should be okay (already in initial data)
    response = client.post(f"/activities/Chess%20Club/signup?email={email}")
    assert response.status_code == 400


def test_signup_missing_activity():
    response = client.post("/activities/NoSuchActivity/signup?email=a@b.com")
    assert response.status_code == 404


def test_unregister_success():
    email = "michael@mergington.edu"
    response = client.delete(f"/activities/Chess%20Club/signup?email={email}")
    assert response.status_code == 200
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_not_registered():
    response = client.delete("/activities/Chess%20Club/signup?email=unknown@x.com")
    assert response.status_code == 400


def test_unregister_missing_activity():
    response = client.delete("/activities/Nope/signup?email=a@b.com")
    assert response.status_code == 404
