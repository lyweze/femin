SELECT t.track_id, t.title, t.file_path AS mp3_url,
       c.image_path AS cover_url
FROM tracks t
LEFT JOIN covers c ON t.track_id = c.track_id;