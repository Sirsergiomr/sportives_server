from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from ckeditor_uploader import views as vistas_ckeditor
from django.contrib.auth import views as auth_views

import usuarios

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^usuarios/', include('usuarios.urls')),

    url(r'^api/v1/usuarios/', include('usuarios.urls_api_v1')),

    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^upload/', login_required(vistas_ckeditor.upload), name='ckeditor_upload'),
    url(r'^browse/', login_required(vistas_ckeditor.browse), name='ckeditor_browse'),
]
