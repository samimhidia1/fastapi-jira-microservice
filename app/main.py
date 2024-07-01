from fastapi import FastAPI
from api.v1.endpoints import epics
from core.database import connection_pool
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

@app.on_event("startup")
async def startup_event():
    global connection_pool
    try:
        connection_pool = psycopg2.pool.SimpleConnectionPool(
            1, 20,
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME")
        )
        if connection_pool:
            print("Connection pool initialized successfully")
        else:
            print("Failed to initialize connection pool")
    except Exception as error:
        print("Error while initializing connection pool", error)

@app.on_event("shutdown")
async def shutdown_event():
    global connection_pool
    if connection_pool:
        connection_pool.closeall()
        print("Connection pool closed successfully")

# Include the router for epics
app.include_router(epics.router)
