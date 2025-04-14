import psycopg2
from backend.config import DB_NAME, DB_USER

def init_db():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER)
    return conn

from datetime import datetime, timedelta

def save_track_to_db(title, signed_url, expires_in, conn, cursor):
    now = datetime.now()
    expires_time = now + timedelta(hours=expires_in)

    cursor.execute(
        """
        SELECT track_id, url_expires
        FROM tracks
        WHERE title = %s
        """,
        (title,)
    )
    result = cursor.fetchone()

    if result:
        track_id, url_expires = result
        if url_expires and url_expires <= now:
            cursor.execute(
                """
                UPDATE tracks
                SET file_path = %s, url_expires = %s
                WHERE track_id = %s
                """,
                (signed_url, expires_time, track_id)
            )
            conn.commit()
        return track_id
    else:
        cursor.execute(
            """
            INSERT INTO tracks (title, file_path, url_expires)
            VALUES (%s, %s, %s)
            RETURNING track_id
            """,
            (title, signed_url, expires_time)
        )
        track_id = cursor.fetchone()[0]
        conn.commit()
        return track_id