# -*- coding: utf-8 -*-
# Django settings for shopifyplus project.

import os.path
import posixpath
import pinax
import grappelli
import sys

PINAX_ROOT = os.path.abspath(os.path.dirname(pinax.__file__))
GRAPPELLI_ROOT = os.path.abspath(os.path.dirname(grappelli.__file__))
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

# tells Pinax to use the default theme
PINAX_THEME = "default"

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# tells Pinax to serve media through the staticfiles app.
SERVE_MEDIA = DEBUG

INTERNAL_IPS = [
    "127.0.0.1",
]

ADMINS = [
    # ("Your Name", "your_email@domain.com"),
]

MANAGERS = ADMINS

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3", # Add "postgresql_psycopg2", "postgresql", "mysql", "sqlite3" or "oracle".
        "NAME": os.path.join(PROJECT_ROOT, "dev.db"), # Or path to database file if using sqlite3.
        "USER": "",                             # Not used with sqlite3.
        "PASSWORD": "",                         # Not used with sqlite3.
        "HOST": "",                             # Set to empty string for localhost. Not used with sqlite3.
        "PORT": "",                             # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "US/Eastern"

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "site_media", "media")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = "/site_media/media/"

# Absolute path to the directory that holds static files like app media.
# Example: "/home/media/media.lawrence.com/apps/"
STATIC_ROOT = os.path.join(PROJECT_ROOT, "site_media", "static")

# URL that handles the static files like app media.
# Example: "http://media.lawrence.com"
STATIC_URL = "/site_media/static/"

# Additional directories which hold static files
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, "media"),
    # os.path.join(PROJECT_ROOT, "media", PINAX_THEME), # ship 'with' the project for now.
    # revert to the Pinax default whilst design_five is in development
    # os.path.join(PINAX_ROOT, "media", "default"),
    
    # include grappelli
    # ("admin", os.path.join(GRAPPELLI_ROOT, "media")),
]

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
# ADMIN_MEDIA_PREFIX = posixpath.join(STATIC_URL, "admin/")
ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"

# Make this unique, and don't share it with anybody.
SECRET_KEY = "d_b!f94h#ock%cao=9!@3k2y3*+a97%i2(ecv3oq^+3%&v(+f8"

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]

MIDDLEWARE_CLASSES = [
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    # "pinax.middleware.security.HideSensistiveFieldsMiddleware",
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "shopifyplus.urls"

TEMPLATE_DIRS = [
    os.path.join(PROJECT_ROOT, "templates"),
    os.path.join(PINAX_ROOT, "templates", PINAX_THEME),
]

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    
    "staticfiles.context_processors.static_url",
    
    "pinax.core.context_processors.pinax_settings",
    
    # "grappelli.context_processors.admin_template_path",
]

INSTALLED_APPS = [
    
    # Grappelli & Admin-tools
    'grappelli.dashboard',
    'grappelli',
    # 'admin_tools',
    # 'admin_tools.theming',
    # 'admin_tools.menu',
    # 'admin_tools.dashboard',
    'filebrowser',
    
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.humanize",
    "django.contrib.staticfiles",
    
    # Developer
    # "debug_toolbar",
    "django_extensions",
    
    # Pinax
    "pinax.templatetags",
    
    # External
    "taggit",
    "south",
    # "staticfiles",
    
    # Shopify Plus
    'fulfilment',
    'invoices',
    'procurement', 
    'products',
    'ordering',
    'shopifyable',
    'shops',
    # 'vendors',
    
]

CACHE_BACKEND = 'memcached://127.0.0.1:8000'

FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, "fixtures"),
]

MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
}

# Admin Tools
# ADMIN_TOOLS_INDEX_DASHBOARD = 'shopifyplus.dashboard.CustomIndexDashboard'
# ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'shopifyplus.dashboard.CustomAppIndexDashboard'

# Filebrowser
FILEBROWSER_DEBUG = False
FILEBROWSER_MEDIA_ROOT = MEDIA_ROOT
FILEBROWSER_MEDIA_URL = MEDIA_URL
FILEBROWSER_URL_FILEBROWSER_MEDIA = STATIC_URL + 'filebrowser/'
FILEBROWSER_PATH_FILEBROWSER_MEDIA = STATIC_ROOT + 'filebrowser/'
FILEBROWSER_DIRECTORY = 'files/'
FILEBROWSER_SAVE_FULL_URL = False

FILEBROWSER_VERSIONS_BASEDIR = "versions"

# Grappelli
GRAPPELLI_ADMIN_TITLE = 'Shopify Plus' 
GRAPPELLI_ADMIN_URL = '/admin'
GRAPPELLI_INDEX_DASHBOARD = 'shopifyplus.dashboard.CustomIndexDashboard'

# Shopify
SHOPIFY_API_KEY = '1a2c8995ba9a2ff76bf32fecebd23bb5'
SHOPIFY_PASSWORD = '677b21a1588ad3b31f0e0f17b6e398d2'
SHOPIFY_HOST_NAME = 'organicorigins.myshopify.com'

# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
try:
    from local_settings import *
except ImportError:
    pass
