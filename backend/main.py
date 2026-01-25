import os
import psycopg2
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI(title="Browser Extension Backend")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class TokenIn(BaseModel):
    url: str
    session_id: str

@app.post("/add")
def add_token(data: TokenIn):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # 1. Check if URL exists
        cur.execute(
            "SELECT id, session_id FROM device_sessions WHERE url = %s;",
            (data.url,)
        )
        record = cur.fetchone()

        # CASE 1: URL exists
        if record:
            db_id, db_session_id = record

            # CASE 1a: Same session_id → error
            if db_session_id == data.session_id:
                raise HTTPException(
                    status_code=400,
                    detail="URL and session_id already exist"
                )

            # CASE 1b: URL exists but session_id changed → update
            cur.execute(
                "UPDATE device_sessions SET session_id = %s WHERE id = %s;",
                (data.session_id, db_id)
            )
            conn.commit()

            return {
                "message": "Session ID updated",
                "id": db_id
            }

        # CASE 2: URL does not exist → insert
        cur.execute(
            """
            INSERT INTO device_sessions (url, session_id)
            VALUES (%s, %s)
            RETURNING id;
            """,
            (data.url, data.session_id)
        )
        new_id = cur.fetchone()[0]
        conn.commit()

        return {
            "message": "New session stored",
            "id": new_id
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()
