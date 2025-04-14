DELETE FROM covers
WHERE cover_id = (SELECT MIN(cover_id) FROM covers);

DELETE FROM tracks
WHERE track_id = (SELECT MIN(track_id) FROM tracks);

ALTER SEQUENCE covers_cover_id_seq RESTART WITH 1;
ALTER sequence tracks_track_id_seq RESTART WITH 1;