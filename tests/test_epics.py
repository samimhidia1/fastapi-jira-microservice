import pytest
from fastapi.testclient import TestClient
from main import app
from core.database import get_db_connection, return_db_connection, initialize_connection_pool
import psycopg2.pool
import os

# Initialize connection pool at the module level
connection_pool = None

# Create a session-level fixture to initialize the database connection pool
@pytest.fixture(scope="session", autouse=True)
def initialize_connection_pool_fixture():
    global connection_pool
    try:
        print("Initializing connection pool with the following environment variables:")
        print("DB_USER:", os.getenv("DB_USER"))
        print("DB_PASSWORD:", os.getenv("DB_PASSWORD"))
        print("DB_HOST:", os.getenv("DB_HOST"))
        print("DB_PORT:", os.getenv("DB_PORT"))
        print("DB_NAME:", os.getenv("DB_NAME"))

        initialize_connection_pool()
        if connection_pool:
            print("Connection pool initialized successfully")
        else:
            print("Failed to initialize connection pool")
    except Exception as error:
        print("Error while initializing connection pool", error)

    yield

    if connection_pool:
        connection_pool.closeall()
        print("Connection pool closed successfully")

# Create a new database connection for testing
@pytest.fixture(scope="module")
def test_db():
    connection = get_db_connection()
    try:
        yield connection
    finally:
        return_db_connection(connection)

# Create a TestClient instance
client = TestClient(app)

def test_create_epic(test_db):
    response = client.post("/api/v1/epics/", json={
        "summary": "Test Epic",
        "description": "This is a test epic",
        "project_key": "TEST",
        "issuetype": "Epic",
        "custom_fields": None
    })
    print("Create Epic Response:", response.json())
    assert response.status_code == 200
    assert response.json()["id"] is not None

def test_get_epic(test_db):
    # First, create an epic to retrieve
    create_response = client.post("/api/v1/epics/", json={
        "summary": "Test Epic",
        "description": "This is a test epic",
        "project_key": "TEST",
        "issuetype": "Epic",
        "custom_fields": None
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
        "issuetype": "Epic",
        "custom_fields": None
    })
    print("Create Epic Response:", create_response.json())
    epic_id = create_response.json()["id"]

    # Now, update the epic
    response = client.put(f"/api/v1/epics/{epic_id}", json={
        "summary": "Updated Test Epic",
        "description": "This is an updated test epic",
        "project_key": "TEST",
        "issuetype": "Epic",
        "custom_fields": None
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
        "issuetype": "Epic",
        "custom_fields": None
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
