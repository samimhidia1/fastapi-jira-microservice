from fastapi import FastAPI
from api.v1.endpoints import epics

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Jira Microservice"}

# Include the router for epics
app.include_router(epics.router)
