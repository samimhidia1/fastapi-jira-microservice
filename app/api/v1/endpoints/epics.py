from fastapi import APIRouter
import requests
import uuid
import json
from models import schemas, models
from core.database import get_db_connection, return_db_connection

router = APIRouter()

@router.post("/api/v1/epics/", response_model=schemas.Epic)
def create_epic(epic: schemas.IssueCreate):
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

        # Deserialize custom_fields from JSON string to dictionary
        custom_fields = json.loads(db_epic[4])
        return {"id": str(db_epic[0]), "summary": db_epic[1], "description": db_epic[2], "project_key": db_epic[3], "custom_fields": custom_fields}
    finally:
        return_db_connection(db)

@router.get("/api/v1/epics/")
def get_epics():
    db = get_db_connection()
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM epics")
        epics = cursor.fetchall()
        return [{"id": str(epic[0]), "summary": epic[1], "description": epic[2], "project_key": epic[3], "custom_fields": epic[4]} for epic in epics]
    finally:
        return_db_connection(db)

@router.get("/api/v1/epics/{epic_id}", response_model=schemas.Epic)
def get_epic(epic_id: str):
    db = get_db_connection()
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM epics WHERE id = %s", (epic_id,))
        db_epic = cursor.fetchone()
        if db_epic is None:
            raise HTTPException(status_code=404, detail="Epic not found")
        return {"id": str(db_epic[0]), "summary": db_epic[1], "description": db_epic[2], "project_key": db_epic[3], "custom_fields": db_epic[4]}
    finally:
        return_db_connection(db)

@router.put("/api/v1/epics/{epic_id}", response_model=schemas.Epic)
def update_epic(epic_id: str, epic: schemas.IssueCreate):
    db = get_db_connection()
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM epics WHERE id = %s", (epic_id,))
        db_epic = cursor.fetchone()
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
        return {"id": str(db_epic[0]), "summary": db_epic[1], "description": db_epic[2], "project_key": db_epic[3], "custom_fields": db_epic[4]}
    finally:
        return_db_connection(db)

@router.delete("/api/v1/epics/{epic_id}", response_model=schemas.Epic)
def delete_epic(epic_id: str):
    db = get_db_connection()
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM epics WHERE id = %s", (epic_id,))
        db_epic = cursor.fetchone()
        if db_epic is None:
            raise HTTPException(status_code=404, detail="Epic not found")
        cursor.execute("DELETE FROM epics WHERE id = %s", (epic_id,))
        db.commit()
        return {"id": str(db_epic[0]), "summary": db_epic[1], "description": db_epic[2], "project_key": db_epic[3], "custom_fields": db_epic[4]}
    finally:
        return_db_connection(db)
