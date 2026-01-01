def test_get_activities_returns_seed_data(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert "Basketball" in payload
    assert payload["Basketball"]["participants"]  # seed not empty


def test_signup_adds_participant(client):
    email = "new.student@mergington.edu"

    response = client.post(
        "/activities/Basketball/signup",
        params={"email": email},
    )

    assert response.status_code == 200
    assert email in response.json()["message"]

    refreshed = client.get("/activities").json()
    assert email in refreshed["Basketball"]["participants"]


def test_signup_rejects_duplicate_student(client):
    # james@mergington.edu is already in Basketball in seed data
    response = client.post(
        "/activities/Tennis Club/signup",
        params={"email": "james@mergington.edu"},
    )

    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_unregister_removes_participant(client):
    email = "michael@mergington.edu"

    delete_response = client.delete(f"/activities/Chess Club/participants/{email}")
    assert delete_response.status_code == 200

    refreshed = client.get("/activities").json()
    assert email not in refreshed["Chess Club"]["participants"]
