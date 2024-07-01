from fastapi import FastAPI
from core.database import engine
from models import models
from api.v1.endpoints import epics

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Jira Microservice"}

# Include the router for epics
app.include_router(epics.router)
