# settings_local.py

import os
from pathlib import Path

from dotenv import load_dotenv

from .settings import *  # noqa

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

ALLOWED_HOSTS = []

# EMAIL BACKEND FOR LOCAL DEVELOPMENT
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / 'api' / 'sent_emails'
DEFAULT_FROM_EMAIL = os.getenv('EMAIL')
