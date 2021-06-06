# -*- encoding: utf-8 -*-
# from dreamsadmin import funciones_stripe

__author__ = 'sergio'

from django.conf.urls import url
from usuarios import views_api_v1

urlpatterns = [

    url(r'^login/$', views_api_v1.login),
    url(r'^logout/$', views_api_v1.logout),
    url(r'^get_perfil/$', views_api_v1.get_perfil),
    url(r'^comprobar_token/$', views_api_v1.comprobar_token),
    url(r'^cambiar_foto_android/$', views_api_v1.set_foto_android),
    url(r'^cambiar_pass/$', views_api_v1.cambiar_pass),
    url(r'^cambiar_email/$', views_api_v1.cambiar_email),
    url(r'^cambiar_publicidad/$', views_api_v1.cambiar_publicidad),
    url(r'^cambiar_nombre/$', views_api_v1.cambiar_nombre),
    url(r'^cambiar_descripcion/$', views_api_v1.cambiar_descripcion),
    url(r'^cambiar_datos/$', views_api_v1.cambiar_datos),
    url(r'^cambiar_apellidos/$', views_api_v1.cambiar_apellidos),
    url(r'^registrar-usuario/$', views_api_v1.registrar_usuario),
    url(r'^get_maquina/$', views_api_v1.get_maquina),
    url(r'^registro_login_google/$', views_api_v1.registro_login_google),
    url(r'^registro_maquina/$', views_api_v1.registrar_maquina),
    url(r'^registrar_entrenamiento/$', views_api_v1.registrar_entrenamiento),
    url(r'^get_entrenamientos/$', views_api_v1.get_entrenamientos),
    url(r'^get_actividades/$', views_api_v1.get_actividades),
    url(r'^get_anuncios/$', views_api_v1.get_anuncios),
    url(r'^eraser_cards/$', views_api_v1.eraserCards),
    url(r'^guardar_tarjeta/(?P<pk>\d+)$', views_api_v1.GuardarTarjeta.as_view(), name='guardar_tarjeta'),
    url(r'^get_tarjetas/$', views_api_v1.get_tarjetas),

    url(r'^pago-correcto/$', views_api_v1.PagoCorrecto.as_view(), name='pago_correcto'),
    url(r'^pago-cancelado/$', views_api_v1.PagoCancelado.as_view(), name='pago_cancelado'),
    url(r'^hacer_pago/$', views_api_v1.hacer_pago),
    url(r'^get_contratados/$', views_api_v1.get_contratados),
    url(r'^comprobar_conexion/$', views_api_v1.comprobar_conexion),
    url(r'^eraser_entrenamientos/$', views_api_v1.eraser_entrenamientos),
    url(r'^eraser_activity/$', views_api_v1.eraser_activity),
    url(r'^eraser_transaction/$', views_api_v1.eraser_transaction),
]


# url(r'^guardar_tarjeta/(?P<pk>\d+)$', views_api_v1.GuardarTarjeta.as_view(), name='guardar_tarjeta'),
# url(r'^get_tarjetas/$',views_api_v1.get_tarjetas),