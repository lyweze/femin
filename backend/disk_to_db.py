from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def save_track_to_db(title, signed_url):

    result = supabase.table("tracks").select("track_id").eq("title", title).execute()

    if result.data:
        track_id = result.data[0]["track_id"]
        return track_id
    else:
        insert_result = supabase.table("tracks").insert({
            "title": title,
            "file_path": signed_url,
        }).execute()

        track_id = insert_result.data[0]["track_id"]

        return track_id