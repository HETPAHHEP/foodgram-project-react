from settings import *


DEBUG = True

ALLOWED_HOSTS = []


STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'


MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'


# EMAIL BACKEND FOR LOCAL DEVELOPMENT
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / 'api' / 'sent_emails'
DEFAULT_FROM_EMAIL = os.getenv('EMAIL')

