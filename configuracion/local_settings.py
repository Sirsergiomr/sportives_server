# -*-coding: utf-8 -*-

# import settings

import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

EXTRA_MIDDLEWARE_CLASSES = ()

EXTRA_INSTALLED_APPS = ()

DATABASES = {
    'default':{
        'ENGINE':'django.db.backends.sqlite3',
        'NAME': BASE_DIR+'/dbsqlite',
        'USER': '',
        'PASSWORD':'',
        'HOST':'',
        'PORT':'',
    }
}