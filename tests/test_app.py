import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Helper to reset activities for isolation (optional, can be improved)
def reset_activities():
    for activity in app.activities.values():
        activity["participants"] = []

# AAA: Arrange-Act-Assert pattern

def test_get_activities():
    # Arrange
    # (client is already set up)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Soccer Team" in data


def test_signup_success():
    # Arrange
    activity = "Soccer Team"
    email = "newstudent@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity}"
    # Confirm participant added
    get_resp = client.get("/activities")
    assert email in get_resp.json()[activity]["participants"]


def test_signup_duplicate():
    # Arrange
    activity = "Soccer Team"
    email = "liam@mergington.edu"  # already present
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_unregister_success():
    # Arrange
    activity = "Soccer Team"
    email = "liam@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 200
    assert "Removed" in response.json()["message"]
    # Confirm participant removed
    get_resp = client.get("/activities")
    assert email not in get_resp.json()[activity]["participants"]


def test_unregister_not_found():
    # Arrange
    activity = "Soccer Team"
    email = "notfound@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]


def test_signup_activity_not_found():
    # Arrange
    activity = "Nonexistent Club"
    email = "student@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_activity_not_found():
    # Arrange
    activity = "Nonexistent Club"
    email = "student@mergington.edu"
    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
