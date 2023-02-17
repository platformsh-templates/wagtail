from .base import *

DEBUG = False

try:
    from .local import *
except ImportError:
    pass

#################################################################################
import os
import sys
import json
import base64

# Platform.sh-specific configuration

# This variable should always match the primary database relationship name,
#   configured in .platform.app.yaml.
PLATFORMSH_DB_RELATIONSHIP="database"

# Helper function for decoding base64-encoded JSON variables.
def decode(variable):
    """Decodes a Platform.sh environment variable.
    Args:
        variable (string):
            Base64-encoded JSON (the content of an environment variable).
    Returns:
        An dict (if representing a JSON object), or a scalar type.
    Raises:
        JSON decoding error.
    """
    try:
        if sys.version_info[1] > 5:
            return json.loads(base64.b64decode(variable))
        else:
            return json.loads(base64.b64decode(variable).decode('utf-8'))
    except json.decoder.JSONDecodeError:
        print('Error decoding JSON, code %d', json.decoder.JSONDecodeError)

python -c 'import os, json, base64; routes = json.loads(base64.b64decode(os.getenv("PLATFORM_ROUTES")).decode("utf-8")); print(routes); primary_route = [e for e in routes if e["primary"] == True]; print(primary_route)'

primary_route = [e for e in routes if e['primary'] == True]; print(primary_route)

# Import some Platform.sh settings from the environment.
if (os.getenv('PLATFORM_APPLICATION_NAME') is not None):

    DEBUG = False

    ALLOWED_HOSTS = [
        'localhost',
        '127.0.0.1',
        '.platformsh.site',
    ]

    if (os.getenv('PLATFORM_APP_DIR') is not None):
        STATIC_ROOT = os.path.join(os.getenv('PLATFORM_APP_DIR'), 'static')
    if (os.getenv('PLATFORM_PROJECT_ENTROPY') is not None):
        SECRET_KEY = os.getenv('PLATFORM_PROJECT_ENTROPY')
    
    if (os.getenv('PLATFORM_ENVIRONMENT') is not None):
        # Database service configuration, post-build only.
        platformRelationships = decode(os.getenv('PLATFORM_RELATIONSHIPS'))
        db_settings = platformRelationships[PLATFORMSH_DB_RELATIONSHIP][0]
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': db_settings['path'],
                'USER': db_settings['username'],
                'PASSWORD': db_settings['password'],
                'HOST': db_settings['host'],
                'PORT': db_settings['port'],
            },
            'sqlite': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
            }
        }
        # Routes configuration, post-build only.
        routes = decode(os.getenv('PLATFORM_ROUTES'))
        primaryRoute = [route for route in routes.keys() if routes[route]["primary"] == True][0][:-1]
        WAGTAILADMIN_BASE_URL = primaryRoute
        BASE_URL = primaryRoute
