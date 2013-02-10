# This is your project's main settings file that can be committed to your
# repo. If you need to override a setting locally, use settings_local.py

import json
import os
from funfactory.settings_base import *

# Name of the top-level module where you put all your apps.
# If you did not install Playdoh with the funfactory installer script
# you may need to edit this value. See the docs about installing from a
# clone.
PROJECT_MODULE = 'project'

# Defines the views served for root URLs.
ROOT_URLCONF = '%s.urls' % PROJECT_MODULE

try:
    import dj_database_url
except ImportError:
    dj_database_url = None

if dj_database_url and os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config()
        # 'slave': {
        #     ...
        # },
    }
    if 'mysql' in DATABASES['default']['ENGINE']:
        opt = DATABASES['default'].get('OPTIONS', {})
        opt['init_command'] = 'SET storage_engine=InnoDB'
        opt['charset'] = 'utf8'
        opt['use_unicode'] = True
        DATABASES['default']['OPTIONS'] = opt
    DATABASES['default']['TEST_CHARSET'] = 'utf8'
    DATABASES['default']['TEST_COLLATION'] = 'utf8_general_ci'


if os.environ.get('MEMCACHE_URL'):
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': os.environ['MEMCACHE_URL'],
            'TIMEOUT': 500
        }
    }

INSTALLED_APPS = list(INSTALLED_APPS) + [
    # Application base, containing global templates.
    '%s.base' % PROJECT_MODULE,
    # Example code. Can (and should) be removed for actual projects.
    '%s.examples' % PROJECT_MODULE,
]

LOCALE_PATHS = (
    os.path.join(ROOT, PROJECT_MODULE, 'locale'),
)

# Because Jinja2 is the default template loader, add any non-Jinja templated
# apps here:
JINGO_EXCLUDE_APPS = [
    'admin',
    'registration',
]

# BrowserID configuration
AUTHENTICATION_BACKENDS = [
    'django_browserid.auth.BrowserIDBackend',
    'django.contrib.auth.backends.ModelBackend',
]

if os.environ.get('VCAP_APPLICATION'):
    VCAP_APP = json.loads(os.environ['VCAP_APPLICATION'])
else:
    VCAP_APP = None

# True if we running as a Stackato instance.
STACKATO = bool(VCAP_APP)

# TODO(Kumar): check for https?
SITE_URL = ('http://%s' % VCAP_APP['uris'][0] if VCAP_APP
            else 'http://127.0.0.1:8000')
LOGIN_URL = '/'
LOGIN_REDIRECT_URL = 'examples.home'
LOGIN_REDIRECT_URL_FAILURE = 'examples.home'

TEMPLATE_CONTEXT_PROCESSORS = list(TEMPLATE_CONTEXT_PROCESSORS) + [
    'django_browserid.context_processors.browserid_form',
]

# Should robots.txt deny everything or disallow a calculated list of URLs we
# don't want to be crawled?  Default is false, disallow everything.
# Also see http://www.google.com/support/webmasters/bin/answer.py?answer=93710
ENGAGE_ROBOTS = False

# Always generate a CSRF token for anonymous users.
ANON_ALWAYS = True

# Tells the extract script what files to look for L10n in and what function
# handles the extraction. The Tower library expects this.
DOMAIN_METHODS['messages'] = [
    ('%s/**.py' % PROJECT_MODULE,
        'tower.management.commands.extract.extract_tower_python'),
    ('%s/**/templates/**.html' % PROJECT_MODULE,
        'tower.management.commands.extract.extract_tower_template'),
    ('templates/**.html',
        'tower.management.commands.extract.extract_tower_template'),
]

# # Use this if you have localizable HTML files:
# DOMAIN_METHODS['lhtml'] = [
#    ('**/templates/**.lhtml',
#        'tower.management.commands.extract.extract_tower_template'),
# ]

# # Use this if you have localizable JS files:
# DOMAIN_METHODS['javascript'] = [
#    # Make sure that this won't pull in strings from external libraries you
#    # may use.
#    ('media/js/**.js', 'javascript'),
# ]

LOGGING = dict(loggers=dict(playdoh = {'level': logging.DEBUG}))

if os.environ.get('DJANGO_SECRET_KEY'):
    SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
else:
    # This must be set in settings/local.py
    SECRET_KEY = ''

if os.environ.get('DJANGO_HMAC_KEY'):
    HMAC_KEYS = {
        'stackato': os.environ['DJANGO_HMAC_KEY']
    }
    from django_sha2 import get_password_hashers
    PASSWORD_HASHERS = get_password_hashers(BASE_PASSWORD_HASHERS, HMAC_KEYS)

if STACKATO:
    # Currently, Mozilla's Stackato only has a self-signed https cert.
    # TODO: fix this when we have https support.
    SESSION_COOKIE_SECURE = False
    # TODO: remove this when we have a way to see exceptions on Stackato.
    DEBUG = TEMPLATE_DEBUG = True
