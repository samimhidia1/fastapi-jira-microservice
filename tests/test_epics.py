import pytest
from fastapi.testclient import TestClient
from main import app
from core.database import SessionLocal, Base, engine
from models import schemas

# Create a new database session for testing
@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

# Create a TestClient instance
client = TestClient(app)

def test_create_epic(test_db):
    response = client.post("/api/v1/epics/", json={
        "summary": "Test Epic",
        "description": "This is a test epic",
        "project_key": "TEST",
        "issuetype": "Epic"
    })
    print("Create Epic Response:", response.json())
    assert response.status_code == 200
    assert response.json()["id"] is not None
    assert response.json()["summary"] == "Test Epic"

def test_get_epic(test_db):
    # First, create an epic to retrieve
    create_response = client.post("/api/v1/epics/", json={
        "summary": "Test Epic",
        "description": "This is a test epic",
        "project_key": "TEST",
        "issuetype": "Epic"
    })
    print("Create Epic Response:", create_response.json())
    epic_id = create_response.json()["id"]

    # Now, retrieve the epic by ID
    response = client.get(f"/api/v1/epics/{epic_id}")
    print("Get Epic Response:", response.json())
    assert response.status_code == 200
    assert response.json()["summary"] == "Test Epic"

def test_update_epic(test_db):
    # First, create an epic to update
    create_response = client.post("/api/v1/epics/", json={
        "summary": "Test Epic",
        "description": "This is a test epic",
        "project_key": "TEST",
        "issuetype": "Epic"
    })
    print("Create Epic Response:", create_response.json())
    epic_id = create_response.json()["id"]

    # Now, update the epic
    response = client.put(f"/api/v1/epics/{epic_id}", json={
        "summary": "Updated Test Epic",
        "description": "This is an updated test epic",
        "project_key": "TEST",
        "issuetype": "Epic"
    })
    print("Update Epic Response:", response.json())
    assert response.status_code == 200
    assert response.json()["summary"] == "Updated Test Epic"

def test_delete_epic(test_db):
    # First, create an epic to delete
    create_response = client.post("/api/v1/epics/", json={
        "summary": "Test Epic",
        "description": "This is a test epic",
        "project_key": "TEST",
        "issuetype": "Epic"
    })
    print("Create Epic Response:", create_response.json())
    epic_id = create_response.json()["id"]

    # Now, delete the epic
    response = client.delete(f"/api/v1/epics/{epic_id}")
    print("Delete Epic Response:", response.json())
    assert response.status_code == 200

    # Verify the epic has been deleted
    get_response = client.get(f"/api/v1/epics/{epic_id}")
    print("Get Deleted Epic Response:", get_response.json())
    assert get_response.status_code == 404
