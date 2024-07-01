import psycopg2
from psycopg2 import pool
import os

# Database connection parameters
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "fastapi_jira")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")

# Initialize connection pool
connection_pool = None

# Function to initialize the connection pool
def initialize_connection_pool():
    global connection_pool
    try:
        connection_pool = psycopg2.pool.SimpleConnectionPool(
            1, 20,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME
        )
        if connection_pool:
            print("Connection pool created successfully")
        else:
            print("Failed to create connection pool")
    except Exception as error:
        print("Error while initializing connection pool", error)
        raise

# Function to get a connection from the pool
def get_db_connection():
    global connection_pool
    try:
        if connection_pool:
            connection = connection_pool.getconn()
            if connection:
                print("Successfully received a connection from the connection pool")
                return connection
        else:
            raise Exception("Connection pool is not initialized")
    except Exception as error:
        print("Error while getting a connection from the connection pool", error)
        raise

# Function to return a connection to the pool
def return_db_connection(connection):
    global connection_pool
    try:
        if connection_pool:
            connection_pool.putconn(connection)
            print("Successfully returned a connection to the connection pool")
        else:
            raise Exception("Connection pool is not initialized")
    except Exception as error:
        print("Error while returning a connection to the connection pool", error)
        raise
