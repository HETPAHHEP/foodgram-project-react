# settings_local.py

import os
from dotenv import load_dotenv
from .settings import *

load_dotenv()


DEBUG = True

ALLOWED_HOSTS = []

# EMAIL BACKEND FOR LOCAL DEVELOPMENT
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / 'api' / 'sent_emails'
DEFAULT_FROM_EMAIL = os.getenv('EMAIL')
