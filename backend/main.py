import os
import psycopg2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI(title="AuthToken API")

class SessionIn(BaseModel):
    auth_token: str

def get_connection():
    return psycopg2.connect(DATABASE_URL)

@app.post("/add")
def add_session(data: SessionIn):
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO device_sessions (auth_token)
            VALUES (%s)
            """,
            (data.auth_token,)
        )

        conn.commit()
        cur.close()
        conn.close()

        return {"message": "Auth token stored successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
