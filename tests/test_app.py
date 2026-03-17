import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_activities():
    # Reset the in-memory activities before each test
    for name, details in activities.items():
        if name == "Chess Club":
            details["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]
        elif name == "Programming Class":
            details["participants"] = ["emma@mergington.edu", "sophia@mergington.edu"]
        elif name == "Gym Class":
            details["participants"] = ["john@mergington.edu", "olivia@mergington.edu"]
        elif name == "Basketball Team":
            details["participants"] = ["james@mergington.edu"]
        elif name == "Tennis Club":
            details["participants"] = ["sarah@mergington.edu", "lucas@mergington.edu"]
        elif name == "Art Studio":
            details["participants"] = ["ava@mergington.edu"]
        elif name == "Music Band":
            details["participants"] = ["noah@mergington.edu", "isabella@mergington.edu"]
        elif name == "Debate Team":
            details["participants"] = ["ethan@mergington.edu"]
        elif name == "Science Club":
            details["participants"] = ["mia@mergington.edu", "alexander@mergington.edu"]


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_for_activity():
    response = client.post("/activities/Chess Club/signup?email=test@mergington.edu")
    assert response.status_code == 200
    assert "Signed up test@mergington.edu for Chess Club" in response.json()["message"]
    # Check participant added
    assert "test@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_duplicate():
    # Already signed up
    response = client.post("/activities/Chess Club/signup?email=michael@mergington.edu")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_nonexistent_activity():
    response = client.post("/activities/Nonexistent/signup?email=someone@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_participant():
    # Remove existing participant
    response = client.delete("/activities/Chess Club/unregister?email=michael@mergington.edu")
    assert response.status_code == 200
    assert "Unregistered michael@mergington.edu from Chess Club" in response.json()["message"]
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_not_registered():
    response = client.delete("/activities/Chess Club/unregister?email=notfound@mergington.edu")
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]


def test_unregister_nonexistent_activity():
    response = client.delete("/activities/Nonexistent/unregister?email=someone@mergington.edu")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
