# Yandex Music sync configuration
YANDEX_CONFIG = {
    "cover_size": "1000x1000",  # Size for high quality covers
    "retry_attempts": 5,
    "retry_wait": 3,
    "rate_limit": 30,
    "rate_period": 60,
    "buckets": {"covers": "covers", "tracks": "tracks"},
    "file_options": {"mp3": {"content-type": "audio/mp3"}},
}

# URL validation patterns
URL_PATTERNS = {
    "yandex": [
        "https://music.yandex.ru/",
        "http://music.yandex.ru/",
        "https://music.yandex.com/",
        "http://music.yandex.com/",
    ]
}

# Error messages
ERROR_MESSAGES = {
    "invalid_url": "Invalid Yandex Music URL. URL must start with music.yandex.ru/ or music.yandex.com/",
    "empty_url": "URL cannot be empty",
    "track_not_found": "URL is not managed to be a track",
    "download_failed": "Failed to download track",
    "upload_failed": "Failed to upload track to storage",
    "cover_download_failed": "Failed to download cover",
    "cover_upload_failed": "Failed to upload cover to storage",
}
