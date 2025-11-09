# settings.py - Add these configurations to your Django settings

import os
from pathlib import Path
from _lib.Config import Config
import _lib.logger as lg
import logging

# read settings from config-file

# path to config file
CONFIG_PATH = "/Users/dom_mini/temp/Webserver.txt"
config = Config(CONFIG_PATH)

# settings located in external config-file

# openweather-api specfic
API_KEY = config.get_item("api_key")
URL_FORECAST = config.get_item("url_forecast").replace("{API key}", API_KEY)
URL_WEATHER = config.get_item("url_weather").replace("{API key}", API_KEY)

# Text files directory (IMPORTANT: Configure this path)
# This should be the absolute path to your directory containing text files
PROT_FILES = config.get_item("PWDprot")
# Example: TEXT_FILES_DIRECTORY = '/home/user/documents/text_files'
# Example: TEXT_FILES_DIRECTORY = 'C:\\Users\\user\\Documents\\text_files'  # Windows
# Example: TEXT_FILES_DIRECTORY = BASE_DIR / 'server_text_files'  # Relative to project
LOG_FILES = config.get_item("PWDlog")

ALLOWED_HOSTS = [config.get_item("allowed_hosts")]

# end from external config-file

# setup logging
lg.setup_logging(LOG_FILES)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'your-secret-key-here'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True



# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'upload',
    'plot',
    'landing',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'clockpi.urls'  # Replace with your project name

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Make sure templates directory exists
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'clockpi.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}



# Static files (CSS, JavaScript, Images)
STATIC_URL = 'site/public/static/'
STATIC_ROOT = BASE_DIR / 'site/public/static'

MEDIA_URL = 'site/public/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'site/public/media')



# File upload settings (still needed for other functionality)
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024   # 10MB

# Form field limits - Increase these for large text files
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000  # Default is 1000, increase for large files
DATA_UPLOAD_MAX_NUMBER_FILES = 100     # Default is 100

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = TrueUPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024   # 10MB

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

