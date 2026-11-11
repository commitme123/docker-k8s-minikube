from fastapi import FastAPI
import os
import psycopg2
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

Instrumentator().instrument(app).expose(app) 


@app.get("/")
def read_root():
    return {"message": "Hello from Kubernetes!"}

@app.get("/db-check")
def check_db():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "mydb"),
            user=os.getenv("DB_USER", "myuser"),
            password=os.getenv("DB_PASSWORD", "mypassword")
        )
        conn.close()
        return {"status": "Successfully connected to the database!"}
    except Exception as e:
        return {"status": "Database connection failed", "error": str(e)}