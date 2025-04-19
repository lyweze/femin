from supabase import create_client, Client
import config

supabase: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)

def save_track_to_db(title, signed_url, playlist_id=None):

    result = supabase.table("tracks").select("track_id").eq("title", title).execute()

    if result.data:
        track_id = result.data[0]["track_id"]
        return track_id

    insert_data = {
        "title": title,
        "file_path": signed_url
    }
    if playlist_id is not None:
        insert_data["playlist_id"] = playlist_id

    insert_result = supabase.table("tracks").insert(insert_data).execute()
    if not insert_result.data:
        raise ValueError("Failed to insert track into database")

    return insert_result.data[0]["track_id"]


def save_playlist_to_db(title):
    result = supabase.table("playlists").select("playlist_id").eq("title", title).execute()
    if result.data:
        return result.data[0]["playlist_id"]
    insert_result = supabase.table("playlists").insert({
        "title": title,
    }).execute()
    return insert_result.data[0]["playlist_id"]

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
