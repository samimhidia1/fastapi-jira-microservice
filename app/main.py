from fastapi import FastAPI
from api.v1.endpoints import epics
from core.database import connection_pool

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Jira Microservice"}

@app.get("/health")
def health_check():
    return {"status": "OK"}

@app.on_event("startup")
async def startup_event():
    if connection_pool:
        print("Connection pool initialized successfully")
    else:
        print("Failed to initialize connection pool")

# Include the router for epics
app.include_router(epics.router)
