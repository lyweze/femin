from supabase import create_client, Client
import config

supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)

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

def save_cover_to_db(solo_track_id, public_cover_url):
    result = supabase.table("covers").select("cover_id").eq("track_id", solo_track_id).execute()

    if result.data:
        cover_id = result.data[0]["cover_id"]
        return cover_id
    else:
        insert_result = supabase.table("covers").insert({
            "track_id": solo_track_id,
            "image_path": public_cover_url,
        }).execute()
        cover_id = insert_result.data[0]["cover_id"]
        return cover_id
