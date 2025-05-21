import io
import logging
import os
from typing import Optional, Tuple, List, Union
from urllib.error import HTTPError
import time
import requests
import tempfile
from requests import RequestException
from storage3.exceptions import StorageApiError
import config, disk_to_db, sanitizer
import tenacity
import supabase
from yandex_music import Client
from .yandex_config import YANDEX_CONFIG, URL_PATTERNS, ERROR_MESSAGES