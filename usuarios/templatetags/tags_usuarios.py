# -*- coding: utf-8 -*-

from django.shortcuts import render, render_to_response
from django import template
import datetime

from configuracion import local_settings

register = template.Library()


@register.simple_tag(name='get_id_usuario')
def get_id_usuario_por_djangouser(user):

    u=user.pk
    id = u.pk
    return id

@register.simple_tag(name='get_usuario')
def get_usuario_por_djangouser(user):

    u=user

    return u


@register.simple_tag(name='get_public_key_stripe')
def get_public_key_stripe():
    return local_settings.STRIPE_API_KEY_PUBLIC


# @register.simple_tag(name='get_tipo_usuario')
# def get_tipo_usuario_por_djangouser(user):
#
#     u=Usuario.objects.get(usuario=user)
#     tipo = u.tipo
#     return tipo

@register.simple_tag(name='get_nombre_archivo')
def get_nombre_archivo(url):

    u = url.split('/')[-1]

    return u

@register.simple_tag(name='get_tipo_archivo')
def get_tipo_archivo(url):

    u = url.split('/')[-1]
    exten = u.split('.')[-1]
    return exten

@register.simple_tag(name='get_url_server_mensajes')
def get_url_server_mensajes(url):

    cortes = url.find("/mensajes")+1
    urlfinal = url[0:cortes]
    return urlfinal

@register.simple_tag(name='get_url_server')
def get_url_server(url):

    cortes = url.find("/")+1
    urlfinal = url[0:cortes]
    return urlfinal

@register.filter(name='get_grupos_dia')
def get_grupos_dia(grupos,dia):
    grupos_dia = grupos.filter(dia_semana=dia).order_by('hora_inicio')
    return grupos_dia

@register.filter(name='get_clase_grupo_activo')
def get_clase_grupo_activo(grupo):
    clase = "panel-success"
    if grupo.caducidad < datetime.date.today():
        clase = "panel-danger"

    return clase


