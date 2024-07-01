from fastapi import FastAPI
from api.v1.endpoints import epics
from core.database import connection_pool, initialize_connection_pool
import psycopg2.pool
import os
from fastapi import FastAPI, Request
from fastapi.routing import APIRoute

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Jira Microservice"}

@app.get("/health")
def health_check():
    return {"status": "OK"}

async def lifespan(app: FastAPI):
    global connection_pool
    try:
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

app.router.lifespan = lifespan

# Include the router for epics
app.include_router(epics.router)
