"""
Django settings for proyectolimpio project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '_eg)$l@t9%y1uz&1a7e)$)-s*vxlcw430xo@4ndxy&4p(%5092'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'dal',
    'dal_select2',

    'sslserver',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',
    'ckeditor_uploader',
    'bootstrapform',

    'usuarios',
    'datetimewidget',




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

ROOT_URLCONF = 'configuracion.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
                 os.path.join(BASE_DIR, 'web/templates')]
        ,
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

WSGI_APPLICATION = 'configuracion.wsgi.application'


"""
para poder instalar con apache hay que descomentar static root y comentar
los staticfiles_dirs hacer python manage.py collectstatic y dejar comoe staba
"""
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# os.path.join(BASE_DIR, "static"),
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# crear las utilidades en un blog (negrita,color...)
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js'
CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_IMAGE_BACKEND = "pillow"

CKEDITOR_CONFIGS = {
    'default': {
        'allowedContent': True,
        'skin': 'office2013',
        # 'skin': 'office2013',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},

            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', '-', 'Undo', 'Redo', '-']},
            {'name': 'editing', 'items': ['Replace' 'SelectAll']},
            {'name': 'tools', 'items': ['Maximize']},
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert',
             'items': ['Image', 'Table', 'HorizontalRule', 'Youtube']},
            {'name': 'styles', 'items': ['Styles', 'Format', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},

            # '/',   put this to force next toolbar on new line
            {'name': 'yourcustomtools', 'items': [
                # put the name of your editor.ui.addButton here

            ]},
        ],
        'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
        # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
        # 'height': 291,
        'width': '100%',
        # 'filebrowserWindowHeight': 725,
        # 'filebrowserWindowWidth': 940,
        # 'toolbarCanCollapse': True,
        # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
        'tabSpaces': 4,
        'extraPlugins': ','.join(
            [
                # your extra plugins here
                'div',
                'autolink',
                'autoembed',
                'embedsemantic',
                'autogrow',
                'youtube',
                # 'devtools',
                'widget',
                'lineutils',
                'clipboard',
                'dialog',
                'dialogui',
                'elementspath'
            ]),
    }
}

DREAMS_ADMIN_CUSTOM_MENU = [
    {'label': 'Correos',
     'tipo': 'seccion',
     'items': [{'label': 'Enviar correo todos',
                'tipo': 'url_django',
                'url': 'enviar_correo_todos',
                },
                {'label': 'Enviar correo criadores',
                'tipo': 'url_django',
                'url': 'enviar_correo_criadores',
                },
                {'label': 'Enviar correo un destinatario',
                'tipo': 'url_django',
                'url': 'enviar_correo_destinarario',
                }
               ]
     }
]

# DREAMS_ADMIN_STAFF_MENU = [
#     {'label': 'Correos',
#      'tipo': 'seccion',
#      'items': [{'label': 'Enviar correo todos',
#                 'tipo': 'url_django',
#                 'url': 'enviar_correo_todos',
#                 },
#                {'label': 'Enviar correo criadores',
#                 'tipo': 'url_django',
#                 'url': 'enviar_correo_criadores',
#                 },
#                {'label': 'Enviar correo un destinatario',
#                 'tipo': 'url_django',
#                 'url': 'enviar_correo_destinarario',
#                 }
#                ]
#      }
# ]


LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/login/'

DEFAULT_FROM_EMAIL = 'App Sortives Titans <info@sportivestitans.com>'
SERVER_EMAIL = DEFAULT_FROM_EMAIL
EMAIL_USE_TLS = True
EMAIL_HOST = 'ssl0.ovh.net'
EMAIL_HOST_USER = 'info@sportivestitans.com'
EMAIL_HOST_PASSWORD = 'sportivestitans27078'
EMAIL_PORT = 587

# EMAIL_BACKEND = 'django_dkim.backends.smtp.EmailBackend'
# DKIM_SELECTOR = 'com'
# DKIM_DOMAIN = 'waucan.com'
# DKIM_PRIVATE_KEY = '''-----BEGIN RSA PRIVATE KEY-----
# MIICXgIBAAKBgQDDGY7uakkb7XgsZG3wCrNR8KnAKvwZwbMAe5Oqo74J+Wo71Dzv
# fwgUzk4UTJevS7JMZoqwMJAXll8aS2Fdj0fVvWPf4wpWtYI1UJsmQrBGKSS83d6H
# QDoaP1vKMhzuoYzUlyjeNCYo433+/gobDhnMsl3mUVUPr9lSa9a2L4V9HQIDAQAB
# AoGAetZpvsTeuR3ADztAWOVz2ACN8Hdf+RuTB5fG9qZX7dHCyF6t6yDxRqBKWs+K
# pY0keqQJaDt7Tc6YnGafrBedYuM1+TSNBNVMlqdqMc/Wol3Y2Lh2vBrydCDK7+9n
# R4EdHK6QdvBP47T8fZX/IpUnJkV38qr3JA148ExvBMyQ+qUCQQD+Jy29u85YSzvv
# /XaXhq05AEKBMHCn8RL1uONZyD1AmQSyNyxFeFWrEhT0I2TV7rDeOOVwiFlJoCyf
# APWAdbP3AkEAxISEqpgpHeFwPFKoluptCoCeKfvELnbuox+64wgVzVjBD/M319e/
# AIJIXOUwLYxy0AelDtKpgN0cde0HbovqiwJBAIfG3oTyhHZfGxJHUsf4xyognWbv
# PgA6pmpn7+3TMAYGuZ+MIjaq5vmRm2giUIiKECtoMgtAjJLs42m+1WlfeFkCQQCn
# ExtPhkn+s3meb5ARroDCGxNdEkV6U3cTjJhxCKCwkrKhAuEJSs2Ce0FWaSwKrYu3
# Paig741Yl6Poxno5DA99AkEA8J9zkkFqN9ahweOUzM4QNRdv+M9Z3AeZXKdJCxQF
# yQgnRxw85UX3JQAZR8noPmgAoeIQSeKwW3klT/7MPEs8gw==
# -----END RSA PRIVATE KEY-----'''
# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE ='Europe/Madrid'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media/')
MEDIA_URL = '/media/'

MEDIA_IMAGE = MEDIA_ROOT + 'imagenes/'
MEDIA_IMAGE_URL = MEDIA_URL + 'imagenes/'

try:
    from configuracion import local_settings
except ImportError:
    print ("""
    -------------------------------------------------------------------------
    You need to create a local_settings.py file which needs to contain at least
    database connection information.
    -------------------------------------------------------------------------
    """)
    import sys

    sys.exit(1)
else:
    # Import any symbols that begin with A-Z. Append to lists any symbols that
    # begin with "EXTRA_".
    import re

    for attr in dir(local_settings):
        match = re.search('^EXTRA_(\w+)', attr)
        if match:
            name = match.group(1)
            value = getattr(local_settings, attr)
            try:
                globals()[name] += value
            except KeyError:
                globals()[name] = value
        elif re.search('^[A-Z]', attr):
            globals()[attr] = getattr(local_settings, attr)