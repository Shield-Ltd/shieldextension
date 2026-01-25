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
    session_name: str
    session_id: str

@app.post("/add")
def add_token(data: TokenIn):
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # 1. Check if URL exists
        cur.execute(
            """
            SELECT id, session_id, session_name
            FROM device_sessions
            WHERE url = %s;
            """,
            (data.url,)
        )
        record = cur.fetchone()

        # CASE 1: URL exists
        if record:
            db_id, db_session_id, db_session_name = record

            # CASE 1a: Same session_id and session_name → error
            if db_session_id == data.session_id and db_session_name == data.session_name:
                raise HTTPException(
                    status_code=400,
                    detail="URL and session_id already exist"
                )

            # CASE 1b: URL exists but session changed → update
            cur.execute(
                """
                UPDATE device_sessions
                SET session_id = %s,
                    session_name = %s
                WHERE id = %s;
                """,
                (data.session_id, data.session_name, db_id)
            )
            conn.commit()

            return {
                "message": "Session updated",
                "id": db_id
            }

        # CASE 2: URL does not exist → insert
        cur.execute(
            """
            INSERT INTO device_sessions (url, session_name, session_id)
            VALUES (%s, %s, %s)
            RETURNING id;
            """,
            (data.url, data.session_name, data.session_id)
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
