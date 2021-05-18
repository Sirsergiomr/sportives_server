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

STRIPE_API_KEY_PUBLIC = "pk_test_51IYyXyKhOFEV5aAVYobT4WsyQVt451tfr0SG3YQZl80H7G2tIxZUBQImXTgMb73RC6e4CgpdfbDt1vokfjjrqGe000j1XBaPdc"
STRIPE_SECRET_KEY = "sk_test_51IYyXyKhOFEV5aAVeyZV8HbhiM2orC9iwPzlosC7uXw10p92qGBuFguLIcddbvQgALjxJGLfsqVisZYpc7zc6Q0v00YMhpTn64"
STRIPE_API_KEY  = "sk_test_51IYyXyKhOFEV5aAVeyZV8HbhiM2orC9iwPzlosC7uXw10p92qGBuFguLIcddbvQgALjxJGLfsqVisZYpc7zc6Q0v00YMhpTn64"