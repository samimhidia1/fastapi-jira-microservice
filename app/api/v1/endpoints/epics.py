from fastapi import APIRouter, HTTPException
import requests
import uuid
import json
from models import schemas, models
from core.database import get_db_connection, return_db_connection

router = APIRouter()

@router.post("/api/v1/epics/", response_model=schemas.Epic)
def create_epic(epic: schemas.IssueCreate):
    print("Received request data:", epic.model_dump())
    db = get_db_connection()
    try:
        # Create the epic in the local database using raw SQL
        cursor = db.cursor()
        epic_id = str(uuid.uuid4())  # Generate a UUID for the id field
        cursor.execute("""
            INSERT INTO epics (id, summary, description, project_key, custom_fields)
            VALUES (%s, %s, %s, %s, %s)
        """, (epic_id, epic.summary, epic.description, epic.project_key, json.dumps(epic.custom_fields)))
        db.commit()

        # Fetch the created epic to return its details
        cursor.execute("SELECT * FROM epics WHERE id = %s", (epic_id,))
        db_epic = cursor.fetchone()

        # Deserialize custom_fields from JSON string to dictionary if it is valid JSON
        try:
            custom_fields = json.loads(db_epic[4])
            if not isinstance(custom_fields, dict):
                custom_fields = {}
        except (TypeError, json.JSONDecodeError):
            custom_fields = {}
        response_data = {
            "id": str(db_epic[0]),
            "summary": db_epic[1],
            "description": db_epic[2],
            "project_key": str(db_epic[3]),  # Ensure project_key is a string
            "custom_fields": custom_fields  # Ensure custom_fields is a dictionary
        }
        print("Response data:", response_data)
        return response_data
    finally:
        return_db_connection(db)

@router.get("/api/v1/epics/")
def get_epics():
    db = get_db_connection()
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM epics")
        epics = cursor.fetchall()
        result = []
        for epic in epics:
            try:
                custom_fields = json.loads(epic[4])
                if not isinstance(custom_fields, dict):
                    custom_fields = {}
            except (TypeError, json.JSONDecodeError):
                custom_fields = {}
            result.append({"id": str(epic[0]), "summary": epic[1], "description": epic[2], "project_key": epic[3], "custom_fields": custom_fields})
        return result
    finally:
        return_db_connection(db)

@router.get("/api/v1/epics/{epic_id}", response_model=schemas.Epic)
def get_epic(epic_id: str):
    db = get_db_connection()
    try:
        cursor = db.cursor()
        print(f"Executing query: SELECT * FROM epics WHERE id = {epic_id}")
        cursor.execute("SELECT * FROM epics WHERE id = %s", (epic_id,))
        db_epic = cursor.fetchone()
        print(f"Query result: {db_epic}")
        if db_epic is None:
            raise HTTPException(status_code=404, detail="Epic not found")
        try:
            custom_fields = json.loads(db_epic[4])
            if not isinstance(custom_fields, dict):
                custom_fields = {}
        except (TypeError, json.JSONDecodeError):
            custom_fields = {}
        return {"id": str(db_epic[0]), "summary": db_epic[1], "description": db_epic[2], "project_key": db_epic[3], "custom_fields": custom_fields}
    finally:
        return_db_connection(db)

@router.put("/api/v1/epics/{epic_id}", response_model=schemas.Epic)
def update_epic(epic_id: str, epic: schemas.IssueCreate):
    db = get_db_connection()
    try:
        cursor = db.cursor()
        print(f"Executing query: SELECT * FROM epics WHERE id = {epic_id}")
        cursor.execute("SELECT * FROM epics WHERE id = %s", (epic_id,))
        db_epic = cursor.fetchone()
        print(f"Query result: {db_epic}")
        if db_epic is None:
            raise HTTPException(status_code=404, detail="Epic not found")
        cursor.execute("""
            UPDATE epics
            SET summary = %s, description = %s, project_key = %s, custom_fields = %s
            WHERE id = %s
        """, (epic.summary, epic.description, epic.project_key, json.dumps(epic.custom_fields), epic_id))
        db.commit()
        cursor.execute("SELECT * FROM epics WHERE id = %s", (epic_id,))
        db_epic = cursor.fetchone()
        print(f"Updated epic: {db_epic}")
        try:
            custom_fields = json.loads(db_epic[4])
            if not isinstance(custom_fields, dict):
                custom_fields = {}
        except (TypeError, json.JSONDecodeError):
            custom_fields = {}
        return {"id": str(db_epic[0]), "summary": db_epic[1], "description": db_epic[2], "project_key": db_epic[3], "custom_fields": custom_fields}
    finally:
        return_db_connection(db)

@router.delete("/api/v1/epics/{epic_id}", response_model=schemas.Epic)
def delete_epic(epic_id: str):
    db = get_db_connection()
    try:
        cursor = db.cursor()
        print(f"Executing query: SELECT * FROM epics WHERE id = {epic_id}")
        cursor.execute("SELECT * FROM epics WHERE id = %s", (epic_id,))
        db_epic = cursor.fetchone()
        print(f"Query result: {db_epic}")
        if db_epic is None:
            raise HTTPException(status_code=404, detail="Epic not found")
        cursor.execute("DELETE FROM epics WHERE id = %s", (epic_id,))
        db.commit()
        print(f"Deleted epic: {epic_id}")
        try:
            custom_fields = json.loads(db_epic[4])
            if not isinstance(custom_fields, dict):
                custom_fields = {}
        except (TypeError, json.JSONDecodeError):
            custom_fields = {}
        return {"id": str(db_epic[0]), "summary": db_epic[1], "description": db_epic[2], "project_key": db_epic[3], "custom_fields": custom_fields}
    finally:
        return_db_connection(db)
