from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
import requests
import uuid
import json
from app.models import schemas, models
from app.core.database import get_db

router = APIRouter()

@router.post("/api/v1/epics/", response_model=schemas.Epic)
def create_epic(epic: schemas.IssueCreate, db: Session = Depends(get_db)):
    # Create the epic in the local database
    db_epic = models.Epic(
        id=str(uuid.uuid4()),  # Generate a UUID for the id field
        summary=epic.summary,
        description=epic.description,
        project_key=epic.project_key,
        custom_fields=json.dumps(epic.custom_fields)  # Serialize custom_fields to JSON
    )
    db.add(db_epic)
    db.commit()
    db.refresh(db_epic)

    # Commenting out the Jira API request for testing purposes
    # Prepare the data for the Jira API request
    # jira_url = "https://your-jira-instance.atlassian.net/rest/api/3/issue"
    # jira_auth = ("your-email@example.com", "your-api-token")
    # headers = {
    #     "Accept": "application/json",
    #     "Content-Type": "application/json"
    # }
    # payload = {
    #     "fields": {
    #         "summary": epic.summary,
    #         "description": epic.description,
    #         "project": {
    #             "key": epic.project_key
    #         },
    #         "issuetype": {
    #             "name": "Epic"
    #         },
    #         "customfield_10011": epic.custom_fields  # Adjust the custom field ID as needed
    #     }
    # }

    # Send the request to Jira
    # response = requests.post(jira_url, json=payload, headers=headers, auth=jira_auth)

    # Handle the response from Jira
    # if response.status_code == 201:
    #     jira_issue = response.json()
    #     return {"id": db_epic.id, "summary": db_epic.summary, "description": db_epic.description, "project_key": db_epic.project_key, "custom_fields": db_epic.custom_fields}
    # else:
    #     raise HTTPException(status_code=response.status_code, detail=response.text)

    # Return the created epic details
    return {"id": str(db_epic.id), "summary": db_epic.summary, "description": db_epic.description, "project_key": db_epic.project_key, "custom_fields": db_epic.custom_fields}

@router.get("/api/v1/epics/")
def get_epics(db: Session = Depends(get_db)):
    epics = db.query(models.Epic).all()
    return [{"id": str(epic.id), "summary": epic.summary, "description": epic.description, "project_key": epic.project_key, "custom_fields": epic.custom_fields} for epic in epics]

@router.get("/api/v1/epics/{epic_id}", response_model=schemas.Epic)
def get_epic(epic_id: str, db: Session = Depends(get_db)):
    db_epic = db.query(models.Epic).filter(models.Epic.id == epic_id).first()
    if db_epic is None:
        raise HTTPException(status_code=404, detail="Epic not found")
    return {"id": str(db_epic.id), "summary": db_epic.summary, "description": db_epic.description, "project_key": db_epic.project_key, "custom_fields": db_epic.custom_fields}

@router.put("/api/v1/epics/{epic_id}", response_model=schemas.Epic)
def update_epic(epic_id: str, epic: schemas.IssueCreate, db: Session = Depends(get_db)):
    db_epic = db.query(models.Epic).filter(models.Epic.id == epic_id).first()
    if db_epic is None:
        raise HTTPException(status_code=404, detail="Epic not found")
    db_epic.summary = epic.summary
    db_epic.description = epic.description
    db_epic.project_key = epic.project_key
    db_epic.custom_fields = json.dumps(epic.custom_fields)
    db.commit()
    db.refresh(db_epic)
    return {"id": str(db_epic.id), "summary": db_epic.summary, "description": db_epic.description, "project_key": db_epic.project_key, "custom_fields": db_epic.custom_fields}

@router.delete("/api/v1/epics/{epic_id}", response_model=schemas.Epic)
def delete_epic(epic_id: str, db: Session = Depends(get_db)):
    db_epic = db.query(models.Epic).filter(models.Epic.id == epic_id).first()
    if db_epic is None:
        raise HTTPException(status_code=404, detail="Epic not found")
    db.delete(db_epic)
    db.commit()
    return {"id": str(db_epic.id), "summary": db_epic.summary, "description": db_epic.description, "project_key": db_epic.project_key, "custom_fields": db_epic.custom_fields}
