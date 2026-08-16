from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_student_can_apply():
    response = client.post(
        "/applications",
        json={"student_id": 101, "job_id": 1},
    )
    assert response.status_code == 201
    assert response.json()["meets_skill_threshold"] is True


def test_company_can_shortlist_eligible_candidate():
    response = client.post(
        "/applications",
        json={"student_id": 101, "job_id": 1},
    )
    assert response.status_code == 201

    application_id = response.json()["id"]
    shortlist = client.post(
        "/companies/shortlist",
        json={"application_id": application_id},
    )
    assert shortlist.status_code == 200
    assert shortlist.json()["status"] == "shortlisted"
