import io
import logging
import os
from urllib.error import HTTPError
import time
import requests
import tempfile
from requests import RequestException
from storage3.exceptions import StorageApiError
import config, disk_to_db, sanitizer
import tenacity
from supabase import Client, create_client
from yandex_music import Client

logging.basicConfig(level=logging.INFO, format='%(asctime)s -- %(levelname)s -- %(message)s')
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    print("Starting Yandex Sync")