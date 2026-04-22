import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

# Helper to reset activities before each test
@pytest.fixture(autouse=True)
def reset_activities():
    for activity in activities.values():
        # Reset to original participants
        if activity["description"].startswith("Learn strategies"):  # Chess Club
            activity["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]
        elif activity["description"].startswith("Learn programming"):  # Programming Class
            activity["participants"] = ["emma@mergington.edu", "sophia@mergington.edu"]
        elif activity["description"].startswith("Physical education"):  # Gym Class
            activity["participants"] = ["john@mergington.edu", "olivia@mergington.edu"]
    yield

def test_list_activities_returns_all():
    # Arrange
    # (client is already arranged)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data

def test_signup_success():
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert email in activities[activity]["participants"]


def test_signup_prevents_duplicates():
    # Arrange
    email = "michael@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()

def test_signup_nonexistent_activity():
    # Arrange
    email = "someone@mergington.edu"
    activity = "Nonexistent Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
