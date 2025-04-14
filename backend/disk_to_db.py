# Правильный формат (Python + psycopg2)
from datetime import timedelta, datetime

import requests
import json
import pandas as pd
import psycopg2
import ssl
from backend.config import DB_NAME, DB_USER

def init_db():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER)
    return conn

def save_track_to_db(title, signed_url,expires, conn, cursor):
    expires_time = datetime.now() + timedelta(seconds=expires)
    cursor.execute(
        """
        INSERT INTO tracks (title, signed_url, expires_at)
        VALUES (%s, %s, %s)
        RETURNING track_id
        """,
        (title, signed_url, expires_time)

    )
    track_id = cursor.fetchone()[0]
    conn.commit()
    return track_id
def save_cover_to_db(track_id, signed_url, resolution, file_size, expires, conn, cursor):
    expires_time = datetime.now() + timedelta(seconds=expires)
    cursor.execute(
        """
        INSERT INTO covers (track_id, signed_url, resolution, file_size, expires_at)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING cover_id""",
        (track_id, signed_url, resolution, file_size, expires_time)

    )
    cover_id = cursor.fetchone()[0]
    conn.commit()
    return cover_id