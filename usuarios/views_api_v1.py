# -*- encoding: utf-8 -*-
import base64
import imghdr
import os
import threading
import qrcode

import stripe
from django.contrib.gis.geometry import json_regex
from django.db.models import Sum
from django.http.response import JsonResponse
from django.template.loader import get_template
import requests
from django.urls.base import reverse
from django.utils.crypto import get_random_string
from django.views.generic.edit import CreateView

# import notificaciones
from configuracion import local_settings
from configuracion import settings
# from dreamsadmin import funciones_stripe
from notificaciones import notificaciones
from usuarios import funciones_stripe
from utilidades.contrasena import contrasena_generator
from django.core.mail import EmailMessage

__author__ = 'brian'

import django.contrib.auth as auth
import django.http as http
from annoying.functions import get_object_or_None

from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import get_object_or_404, render
import json
import datetime

from utilidades import Token
from usuarios.models import Tokenregister, DatosExtraUser, Validacion, Maquina, Actividad, Entrenamiento, Anuncio

from django.contrib.auth.models import User
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


'''
definicion para conseguir el usuario de django a partir del token
'''

def get_userdjango_by_token(token):
    user_token = get_object_or_None(Tokenregister, token=token)

    if user_token is not None:
        return user_token.user
    else:
        return None


'''
definicion para conseguir el usuario de django a partir del id de usuario
'''


def get_userdjango_by_id(userdjango_id):
    userdjango = get_object_or_None(User, pk=userdjango_id)
    return userdjango


'''
definicion para conseguir el usuario de django a partir del id de usuario
'''


def get_userdjango_by_id2(userdjango_id):
    userdjango = get_object_or_None(User, pk=userdjango_id)
    return userdjango


'''
definicion para comprobar el usuario
'''


def comprobar_usuario(token, usuario_id):
    userdjango = get_userdjango_by_id(usuario_id)
    user_token = get_userdjango_by_token(token)

    if (user_token is not None) and (userdjango is not None):
        if user_token == userdjango:
            return True
        else:
            return False


'''
definicion para comprobar el usuario
'''


def comprobar_usuario2(token, userdjango_id):
    userdjango = get_userdjango_by_id2(userdjango_id)
    user_token = get_userdjango_by_token(token)

    if (user_token is not None) and (userdjango is not None):
        if user_token == userdjango:
            return True
        else:
            return False
    else:
        return False


'''
definicion para logear un usuario desde la aplicación
'''


@csrf_exempt
def login(request):

    print("Login")

    try:
        print(request.POST)
        try:
            datos = json.loads(request.POST['data'])
            us = datos.get('usuario')
            password = datos.get('password')
            os_user = datos.get('os_user')
            usuario = get_object_or_None(User, email=us)

        except Exception as e:
            us = request.POST['usuario']
            password = request.POST['password']
            os_user = request.POST['os_user']

        if (us is None and password is None) or (us == "" and password == ""):
            response_data = {'result': 'error', 'message': 'Falta el usuario y el password'}
            return JsonResponse(response_data)
            #return http.HttpResponse(json.dumps(response_data), content_type="application/json")

        if us is None or us == "":
            response_data = {'result': 'error', 'message': 'Falta el usuario'}
            return http.HttpResponse(json.dumps(response_data), content_type="application/json")

        if password is None or password == "":
            response_data = {'result': 'error', 'message': 'Falta el password'}
            return http.HttpResponse(json.dumps(response_data), content_type="application/json")

        user = auth.authenticate(username=us, password=password)

        if user is None:
            user = auth.authenticate(email=us, password=password)

        if user is not None:
            email = user.email
            user.username = email
            user.save()
            if user.is_active:
                user_token = get_object_or_None(Tokenregister, user=user)

                if user_token is None:
                    print('user_token is none')
                    token1 = str(user.id) + "_" + Token.id_generator()
                    tokenform = Tokenregister(token=token1, user=user)
                    tokenform.save()
                    user_token = get_object_or_None(Tokenregister, user=user)
                    datosExtra = get_object_or_None(DatosExtraUser, usuario=user)

                    if datosExtra is None:
                        datosExtra = DatosExtraUser.objects.create(usuario=user)

                    response_data = {'result': 'ok', 'message': 'Usuario logueado', 'token': user_token.token,
                                     'usuario': user.username,
                                     'nombre': user.first_name,
                                     'tipo_sesion': datosExtra.tipo
                                     }
                else:
                    token1 = str(user.id) + "_" + Token.id_generator()
                    user_token.token = token1
                    user_token.save()
                    datosExtra = get_object_or_None(DatosExtraUser, usuario=user)
                    print(datosExtra)
                    if datosExtra is None:
                        datosExtra = DatosExtraUser.objects.create(usuario=user)

                    os_temp = user.datosextrauser.onesignal_id
                    datosExtra.onesignal_id = os_user
                    datosExtra.save()


                    response_data = {'result': 'ok', 'message': 'Usuario logueado', 'token': user_token.token,
                                     'usuario': user.username,
                                     'nombre': user.first_name,
                                     'tipo_sesion': datosExtra.tipo
                                     }
                if (os_user != "" and os_user is not None):
                    datosExtra.onesignal_id = os_user
                    datosExtra.save()
                return JsonResponse(response_data)
            else:
                response_data = {'result': 'error', 'message': 'Usuario no activo'}

                return JsonResponse(response_data)
        else:
            response_data = {'result': 'error',
                             'message': 'Usuario no válido, pruebe con su email o actualice la aplicación'}

            return JsonResponse(response_data)

    except Exception as e:
        response_data = {'errorcode': 'U0001', 'result': 'error', 'message': str(e)}

        return JsonResponse(response_data)


@csrf_exempt
def registro_login_google(request):
    """
    Peticion login 2020
    :param request:
    :return:
    """
    try:
        try:
            datos = json.loads(request.POST['data'])
            email = datos.get('email')
            nombre = datos.get('nombre')
            url_imagen = datos.get('imagen')
            token_google = datos.get('token_google')
            os_user = datos.get('os_user')
            password = ""

        except Exception as e:

            email = request.POST['email']
            nombre = request.POST['nombre']
            url_imagen = request.POST['imagen']
            token_google = request.POST['token_google']
            os_user = request.POST['os_user']
            password = ""

        tipo = 'google'
        # user = auth.authenticate(username=email, password="")
        user = get_object_or_None(User, email=email)

        if user is not None:
            datosExtra = get_object_or_None(DatosExtraUser, usuario=user)

            if datosExtra is None:
                datosExtra = DatosExtraUser.objects.create(usuario=user)

            if user.is_active:
                token_google_correcto = comprobar_token_google(token_google)
                if token_google_correcto:

                    user.first_name = nombre
                    user.save()

                    user_token = get_object_or_None(Tokenregister, user=user)
                    # es_criador = Criador.objects.filter(user=user).exists()

                    if user_token is None:
                        token1 = str(user.id) + "_" + Token.id_generator()
                        tokenform = Tokenregister(token=token1, user=user)
                        tokenform.save()
                        user_token = get_object_or_None(Tokenregister, user=user)
                        datosExtra.onesignal_id = os_user
                        datosExtra.save()
                        response_data = {'result': 'ok', 'message': 'Usuario logueado', 'token': user_token.token,
                                         'usuario': user.username,
                                         'nombre': user.first_name,
                                         # 'criador': es_criador,
                                         'tipo_sesion': datosExtra.tipo
                                         }
                        return http.HttpResponse(json.dumps(response_data), content_type="application/json")
                    else:

                        token1 = str(user.id) + "_" + Token.id_generator()
                        user_token.token = token1
                        user_token.save()

                        os_temp = user.datosextrauser.onesignal_id
                        datosExtra.onesignal_id = os_user
                        datosExtra.save()

                        response_data = {'result': 'ok', 'message': 'Usuario logueado', 'token': user_token.token,
                                         'usuario': user.username,
                                         'nombre': user.first_name,
                                         # 'criador': es_criador,
                                         'tipo_sesion': datosExtra.tipo
                                         }
                        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

                else:
                    response_data = {'result': 'error', 'message': 'Token de goole no valido, llamar a logout'}

                    return http.HttpResponse(json.dumps(response_data), content_type="application/json")

            else:

                response_data = {'result': 'error', 'message': 'Usuario no activo'}

                return http.HttpResponse(json.dumps(response_data), content_type="application/json")
        else:

            user = User.objects.create(username=email, email=email, first_name=nombre)

            if (os_user != "" and os_user is not None):
                usuario = DatosExtraUser.objects.create(usuario=user,
                                                        tipo=tipo, onesignal_id=os_user
                                                        )
            else:
                usuario = DatosExtraUser.objects.create(usuario=user,
                                                        tipo=tipo, onesignal_id=os_user
                                                        )
            user.save()
            usuario.save()
            # mail_registro(user)

            token1 = str(user.id) + "_" + Token.id_generator()
            tokenform = Tokenregister(token=token1, user=user)
            tokenform.save()
            user_token = get_object_or_None(Tokenregister, user=user)
            datosExtra = get_object_or_None(DatosExtraUser, usuario=user)

            if datosExtra is None:
                datosExtra = DatosExtraUser.objects.create(usuario=user)

            response_data = {'result': 'ok', 'message': 'Usuario logueado', 'token': user_token.token,
                             'usuario': user.username,
                             'nombre': user.first_name,
                             'user': False,
                             'tipo_sesion': datosExtra.tipo
                             }

            return http.HttpResponse(json.dumps(response_data), content_type="application/json")


    except Exception as e:
        response_data = {'errorcode': 'U0001', 'result': 'error', 'message': str(e)}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")


def comprobar_token_google(token_google):
    url = 'https://oauth2.googleapis.com/tokeninfo?id_token=' + token_google

    respuesta = requests.get(url).json()

    try:

        error = respuesta['error']
        return False

    except Exception as e:

        return True


'''
definicion para logear un usuario desde la aplicación java
'''


@csrf_exempt
def logout(request):
    try:
        try:
            datos = json.loads(request.POST['data'])
            token = datos.get('token')
            userdjango_id = datos.get('usuario_id')

        except Exception as e:
            token = request.POST['token']
            userdjango_id = request.POST['usuario_id']

        if comprobar_usuario2(token, userdjango_id):
            userdjango = get_userdjango_by_token(token)

            user_token = get_object_or_None(Tokenregister, user=userdjango)
            if user_token is None:
                response_data = {'result': 'ok', 'message': 'Usuario ya deslogueado'}
            else:

                user_token.delete()
                response_data = {'result': 'ok', 'message': 'Usuario ya deslogueado'}
        else:
            response_data = {'result': 'error', 'message': 'Usuario no logueado'}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'U0002', 'result': 'error', 'message': str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")


'''
definicion para comprobar el token
'''


@csrf_exempt
def comprobar_token(request):
    try:
        try:
            datos = json.loads(request.POST['data'])
            token = datos.get('token')
            userdjango_id = datos.get('usuario_id')

        except Exception as e:
            token = request.POST['token']
            userdjango_id = request.POST['usuario_id']

        if token != "" and comprobar_usuario2(token, userdjango_id):
            response_data = {'result': 'ok', 'message': 'Usuario logueado'}

        else:
            response_data = {'result': 'error', 'message': 'Usuario no logueado'}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'U0003', 'result': 'error', 'message': str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")


'''
metodo para que un usuario pueda ver su perfil, necesario estar loegueado y pasar su id y token
'''

@csrf_exempt
def get_perfil(request):
    try:
        try:
            datos = json.loads(request.POST['data'])
            token = datos.get('token')
            usuario_id = datos.get('usuario_id')

        except Exception as e:
            token = request.POST['token']
            usuario_id = request.POST['usuario_id']

        if comprobar_usuario2(token,usuario_id):
            userdjango = get_userdjango_by_token(token)


            response_data = {'result': 'ok', 'message': 'Perfil de usuario',
                             'usuario': userdjango.datosextrauser.toJSON(),
                             }
        else:
            response_data = {'result': 'error', 'message': 'Usuario no logueado'}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")
    except Exception as e:
        logger.exception(e)
        response_data = {'errorcode': 'U0004', 'result': 'error', 'message': 'Error en perfil de usuario: ' + str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

'''
metodo para subir una foto en base 64
'''
@csrf_exempt
def set_foto_android(request):
    try:

        try:
            datos = json.loads(request.POST['data'])
            token = datos.get('token')
            usuario_id = datos.get('usuario_id')
            imagen = datos.get('imagen')
        except Exception as e:
            token = request.POST['token']
            usuario_id = request.POST['usuario_id']
            imagen = request.POST['imagen']

        if comprobar_usuario2(token, usuario_id):
            user = get_userdjango_by_token(token)
            imgdata = base64.b64decode(imagen)
            tama = (len(imagen) * 3) / 4 - imagen.count('=', -2)

            if tama <= 2000000:
                for tf in imghdr.tests:
                    extension = tf(imgdata, None)
                    if extension:
                        break
                lista = ['jpg', 'JPG', 'png', 'PNG', 'jpeg', 'JPEG']
                if extension in lista:
                    try:
                        os.remove(settings.MEDIA_ROOT) + user.datosextrauser.foto
                    except:
                        pass
                    nombre = 'usuario' + str(user.pk) + '.' + extension
                    lpath = settings.MEDIA_IMAGE + "perfiles/" + nombre
                    destino = open(lpath, 'wb+')
                    destino.write(imgdata)
                    destino.close()

                    user.datosextrauser.imagen = "imagenes/perfiles/" + nombre
                    user.datosextrauser.save()

                response_data = {'result': 'ok',
                                 'message': 'Foto subida correctamente'}
            else:
                response_data = {'result': 'error',
                                 'message': 'Foto demasiado pesada'}

        else:
            response_data = {'result': 'error', 'message': 'Sesiones no cargadas'}


        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        logger.exception(e)
        response_data = {'errorcode': 'U0006', 'result': 'error',
                         'message': 'Error en busqueda de sesiones : ' + str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def cambiar_pass(request):
    try:
        try:
            datos = json.loads(request.POST['data'])
            token = datos.get('token')
            userdjango_id = datos.get('usuario_id')
            antiguapass = datos.get('antigua')
            nuevapass = datos.get('nueva')

        except Exception as e:
            token = request.POST['token']
            userdjango_id = request.POST['usuario_id']
            antiguapass = request.POST['antigua']
            nuevapass = request.POST['nueva']

        if comprobar_usuario2(token, userdjango_id):
            userdjango = get_userdjango_by_token(token)
            if userdjango.check_password(antiguapass):
                token = get_object_or_None(Tokenregister, user=userdjango)
                token.delete()
                userdjango.set_password(nuevapass)
                userdjango.save()
                response_data = {'result': 'ok', 'message': 'Password cambiado'}
            else:
                response_data = {'result': 'error', 'message': 'Password antiguo incorrecto'}
        else:
            response_data = {'result': 'error', 'message': 'Usuario no logueado'}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'U0005', 'result': 'error', 'message': 'Error en perfil de usuario: ' + str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def cambiar_email(request):
    # print ("cambiando email")
    try:
        try:
            datos = json.loads(request.POST['data'])
            email = datos.get('email')
            token = datos.get('token')
            usuario_id = datos.get('usuario_id')
            print("datos que llegan")
            print(datos)
        except Exception as e:
            token = request.POST['token']
            usuario_id = request.POST['usuario_id']
            email = request.POST['email']

        if comprobar_usuario(token, usuario_id):
            userdjango = get_userdjango_by_token(token)
            userdjango.email = email
            userdjango.username = email
            userdjango.save()
            response_data = {'result': 'ok', 'message': 'Email cambiado'}
            print(response_data)

        else:
            response_data = {'result': 'error', 'message': 'Usuario no logueado'}
            print(response_data)

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'U0005', 'result': 'error',
                         'message': 'Error en perfil de usuario: ' + str(e)}
        print(response_data)
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def cambiar_publicidad(request):
    # print ("cambiar_publicidad")
    try:
        try:
            datos = json.loads(request.POST['data'])
            publicidad = datos.get('publicidad')
            token = datos.get('token')
            usuario_id = datos.get('usuario_id')
        except Exception as e:
            token = request.POST['token']
            usuario_id = request.POST['usuario_id']
            publicidad = request.POST['publicidad']

        if comprobar_usuario(token, usuario_id):
            userdjango = get_userdjango_by_token(token)
            userdjango.datosextrauser.publicidad = publicidad
            userdjango.save()
            response_data = {'result': 'ok', 'message': 'Publicidad cambiado'}
        else:
            response_data = {'result': 'error', 'message': 'Usuario no logueado'}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'U0005', 'result': 'error',
                         'message': 'Error en perfil de usuario: ' + str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def cambiar_nombre(request):
    # print ("cambiar_nombre")
    try:
        try:
            datos = json.loads(request.POST['data'])
            nombre = datos.get('nombre')
            token = datos.get('token')
            usuario_id = datos.get('usuario_id')
        except Exception as e:
            token = request.POST['token']
            usuario_id = request.POST['usuario_id']
            nombre = request.POST['nombre']

        if comprobar_usuario(token, usuario_id):
            userdjango = get_userdjango_by_token(token)
            userdjango.first_name = nombre
            userdjango.save()
            response_data = {'result': 'ok', 'message': 'Nombre cambiado'}
        else:
            response_data = {'result': 'error', 'message': 'Usuario no logueado'}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'U0005', 'result': 'error',
                         'message': 'Error en perfil de usuario: ' + str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def cambiar_descripcion(request):
    # print ("cambiar_descripcion")
    try:
        try:
            datos = json.loads(request.POST['data'])
            descripcion = datos.get('descripcion')
            token = datos.get('token')
            usuario_id = datos.get('usuario_id')
        except Exception as e:
            token = request.POST['token']
            usuario_id = request.POST['usuario_id']
            descripcion = request.POST['descripcion']

        if comprobar_usuario(token, usuario_id):
            userdjango = get_userdjango_by_token(token)
            userdjango.datosextrauser.descripcion = descripcion
            userdjango.datosextrauser.save()
            response_data = {'result': 'ok', 'message': 'Descripcion cambiada'}
        else:
            response_data = {'result': 'error', 'message': 'Usuario no logueado'}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'U0005', 'result': 'error',
                         'message': 'Error en perfil de usuario: ' + str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def cambiar_apellidos(request):
    print("cambiar_apellidos")
    try:
        try:
            datos = json.loads(request.POST['data'])
            apellidos = datos.get('apellido')
            token = datos.get('token')
            usuario_id = datos.get('usuario_id')
            print(datos)
        except Exception as e:
            token = request.POST['token']
            usuario_id = request.POST['usuario_id']
            apellidos = request.POST['apellido']
            print("EXCEPT")
            print(datos)

        if comprobar_usuario(token, usuario_id):
            print("hola")
            userdjango = get_userdjango_by_token(token)
            print(apellidos)
            userdjango.last_name = apellidos
            userdjango.save()
            response_data = {'result': 'ok', 'message': 'Apellidos cambiado'}
            print(response_data)
        else:
            response_data = {'result': 'error', 'message': 'Error al cambiar apellidos'}
            print(response_data)
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

        print(response_data)

    except Exception as e:
        response_data = {'errorcode': 'U0005', 'result': 'error',
                         'message': 'Error en cambiar apellido: ' + str(e)}

        print(response_data)
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def cambiar_datos(request):
    try:
        try:
            datos = json.loads(request.POST['data'])
            email = datos.get('email')
            nombre = datos.get('nombre')
            apellidos = datos.get('apellidos')
            token = datos.get('token')
            usuario_id = datos.get('usuario_id')
            publicidad = datos.get('publicidad')
            ciudad = datos.get('ciudad')
        except Exception as e:

            token = request.POST['token']
            usuario_id = request.POST['usuario_id']
            email = request.POST['email']
            nombre = request.POST['nombre']
            apellidos = request.POST['apellidos']
            publicidad = request.POST['publicidad']
            ciudad = request.POST['ciudad']

        if comprobar_usuario(token, usuario_id):
            userdjango = get_userdjango_by_token(token)

            if email == "":
                pass
            else:
                userdjango.email = email
                userdjango.username = email

            if nombre == "":
                pass
            else:
                userdjango.first_name = nombre

            if apellidos == "":
                pass
            else:
                userdjango.last_name = apellidos

            if publicidad == "":
                pass
            else:
                userdjango.datosextrauser.publicidad = publicidad

            if ciudad == "":
                pass
            else:
                userdjango.datosextrauser.ciudad = ciudad

            userdjango.save()
            response_data = {'result': 'ok', 'message': 'Datos cambiados correctamente'}
        else:
            response_data = {'result': 'error', 'message': 'Usuario no logueado'}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'U0005', 'result': 'error',
                         'message': 'Error en perfil de usuario: ' + str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")


@csrf_exempt
def registrar_usuario(request):
    try:
        try:
            datos = json.loads(request.POST['data'])
            nombre = datos.get('nombre')
            email = datos.get('email')
            password = datos.get('password')

        except Exception as e:
            nombre = request.POST['nombre']
            password = request.POST['password']
            email = request.POST['email']

        if (nombre is None and email is None and password is None) or (nombre == "" and password == "" and email == ""):
            response_data = {'result': 'error', 'message': 'Falta el nombre usuario, email y password'}
            return http.HttpResponse(json.dumps(response_data), content_type="application/json")

        if nombre is None or nombre == "":
            response_data = {'result': 'error', 'message': 'Falta el nombre de usuario'}
            return http.HttpResponse(json.dumps(response_data), content_type="application/json")

        if password is None or password == "":
            response_data = {'result': 'error', 'message': 'Falta el password'}
            return http.HttpResponse(json.dumps(response_data), content_type="application/json")

        if email is None or email == "":
            response_data = {'result': 'error', 'message': 'Falta el email'}
            return http.HttpResponse(json.dumps(response_data), content_type="application/json")

        usuarios = User.objects.filter(username=email)
        usuarios_email = User.objects.filter(email=email)

        if usuarios.count() == 0 and usuarios_email.count() == 0:
            if usuarios_email.count() == 0:
                user = User.objects.create(username=email,
                                           first_name=nombre,
                                           email=email)

                user.set_password(password)
                usuario = DatosExtraUser.objects.create(usuario=user,recibir_comunicaciones=True)

                user.save()
                usuario.save()

                response_data = {'result': 'ok', 'message': 'Usuario creado correctamente',
                                     'usuario': usuario.toJSON()}
                print(response_data)


            else:
                response_data = {'result': 'error', 'message': 'Este email ya existe'}
        else:
            response_data = {'result': 'error', 'message': 'Este nombre de usuario ya existe'}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

    except Exception as e:
        response_data = {'errorcode': 'U0005', 'result': 'error', 'message': 'Error en crear usuario. ' + str(e)}

        return http.HttpResponse(json.dumps(response_data), content_type="application/json")

def generar_qr(cadena):
    qr = qrcode.QRCode(
        version = 1,
        error_correction= qrcode.constants.ERROR_CORRECT_H,
        box_size = 10,
        border = 4
    )

    info = cadena

    qr.add_data(info)
    qr.make(fit=True)
    imagen = qr.make_image()

    return imagen.save('codigo.png')


@csrf_exempt
def registrar_maquina(request):
    try:
        datos = json.loads(request.POST['data'])
        usuario_id = datos.get('usuario_id')
        token = datos.get('token')
        nombre_maquina = datos.get('nombre_maquina')
    except Exception as e:
        usuario_id = request.POST['usuario_id']
        token = request.POST['token']


    if comprobar_usuario(token, usuario_id):
        print("comprueba usuario")

        nombre_maquina = request.POST['nombre_maquina']

        nueva_maquina = Maquina.objects.create(nombre_maquina)

        nueva_maquina.foto(generar_qr(nueva_maquina.pk))

        nueva_maquina.save()
        print('Maquina creada')
    else:
        response_data= {'result': 'error', 'message': 'Usuario no logeado'}
    return JsonResponse(response_data)
@csrf_exempt
def registrar_entrenamiento(request):
    try:
        datos = json.loads(request.POST['data'])
        usuario_id = datos.get('usuario_id')
        token = datos.get('token')
        fecha = datos.get('fecha')
        hora = datos.get('hora');
        nombre_maquina = datos.get('nombre_maquina')
        tiempo_uso = datos.get('tiempo_uso')
        id_maquina = datos.get('id_maquina')
    except Exception as e:
        usuario_id = request.POST['usuario_id']
        token = request.POST['token']
        fecha = request.POST['fecha']
        hora = request.POST['hora']
        nombre_maquina = request.POST['nombre_maquina']
        id_maquina = request.POST['id_maquina']

    if comprobar_usuario(token, usuario_id):
        userdjango = get_userdjango_by_token(token)
        try:
          actividad = Actividad.objects.get(fecha=fecha)
        except Exception as e:
            actividad = Actividad.objects.create(usuario=userdjango, fecha=fecha,nombre_actividad=nombre_maquina)
            actividad.save()

        entrenamiento = Entrenamiento.objects.create(usuario=userdjango, Nombre_maquina=nombre_maquina, fecha=fecha, hora=hora, tiempo_uso=tiempo_uso)
        entrenamiento.save()
        response_data = {'result': 'ok', 'message': 'Todo bien, todo correcto, y yo que me alegro'}
    else:
        response_data= {'result': 'error', 'message': 'Usuario no logeado'}
    return JsonResponse(response_data)





@csrf_exempt
def get_maquina(request):
    print(request)
    try:
        datos = json.loads(request.POST['data'])
        usuario_id = datos.get('usuario_id')
        token = datos.get('token')
        id_maquina = datos.get('id_maquina')
    except Exception as e:
        usuario_id = request.POST['usuario_id']
        token = request.POST['token']
        id_maquina = request.POST['id_maquina']

    if comprobar_usuario(token, usuario_id):
        try:
            maquina = Maquina.objects.get(pk=id_maquina)
            response_data = {'result': 'ok', 'message': 'ok', 'nombre': maquina.Nombre_maquina,
                             "id_maquina": maquina.pk}
        except Exception as e:
            response_data = {'result': 'error', 'message': 'Máquina no encontrada'}
    else:
        response_data = {'result': 'login_error', 'message': 'Fallo de sesión'}

    return JsonResponse(response_data)
@csrf_exempt
def get_entrenamientos(request):
    print(request)
    try:
        datos = json.loads(request.POST['data'])
        usuario_id = datos.get('usuario_id')
        token = datos.get('token')
        fecha = datos.get('fecha')
    except Exception as e:
        usuario_id = request.POST['usuario_id']
        token = request.POST['token']
        fecha = request.POST['fecha']

    lista = []

    if comprobar_usuario(token, usuario_id):

        userdjango = get_userdjango_by_token(token)
        os_temp = userdjango.datosextrauser.onesignal_id
        notificaciones.notificacioInicioSesion(os_temp)

        entrenamientos = Entrenamiento.objects.all()

        if entrenamientos.filter(fecha=fecha) is not None:
            entrenamientos = entrenamientos.filter(fecha=fecha)
            for entrenar in entrenamientos:
                lista.append(entrenar.toJSON())
            response_data = {'result': 'ok', 'lista': lista}
        else:
            response_data = {'result': 'error', 'message': 'No se han encontrado entrenamientos con fehca' + fecha}
    else:
        response_data = {'result': 'login_error', 'message': 'Fallo de sesión'}
    return JsonResponse(response_data)



@csrf_exempt
def get_actividades(request):
    print(request)
    try:
        datos = json.loads(request.POST['data'])
        usuario_id = datos.get('usuario_id')
        token = datos.get('token')
    except Exception as e:
        usuario_id = request.POST['usuario_id']
        token = request.POST['token']

    lista = []

    if comprobar_usuario(token, usuario_id):

        userdjango = get_userdjango_by_token(token)

        actividades = Actividad.objects.all()
        if actividades.filter(usuario=userdjango) is not None:

            actividades = actividades.filter(usuario=userdjango)
            for actividad in actividades:
                lista.append(actividad.toJSON())

            response_data = {'result': 'ok', 'lista': lista}

        else:
            response_data = {'result': 'error', 'message': 'No se han encontrado actividades'}
    else:
        response_data = {'result': 'login_error', 'message': 'Fallo de sesión'}
    return JsonResponse(response_data)

@csrf_exempt
def get_anuncios(request):
    print(request)
    try:
        datos = json.loads(request.POST['data'])
        usuario_id = datos.get('usuario_id')
        token = datos.get('token')
    except Exception as e:
        usuario_id = request.POST['usuario_id']
        token = request.POST['token']

    lista = []

    if comprobar_usuario(token, usuario_id):
        anuncios = Anuncio.objects.all()
        for oferta in anuncios:
            lista.append(oferta.toJSON())
        response_data = {'result': 'ok', 'lista': lista}
    else:
        response_data = {'result': 'login_error', 'message': 'Fallo de sesión'}
    return JsonResponse(response_data)
def enviar(mensaje):
    mensaje.send()


def enviar_email(asunto, mensaje, mensaje_html, destinos):
    msg = EmailMessage(asunto, mensaje_html, settings.EMAIL_HOST_USER, destinos)
    msg.content_subtype = "html"

    t = threading.Thread(target=enviar, args=(msg,))
    t.start()

class GuardarTarjeta(CreateView):
    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk=self.kwargs['pk'])
        print(request.META["HTTP_TOKEN"])

        token = request.META["HTTP_TOKEN"]

        if comprobar_usuario(token , self.kwargs['pk']):

            try:
                user.datosextrauser.id_customer_stripe
            except:
                DatosExtraUser.objects.create(usuario=user)

            if user.datosextrauser.id_customer_stripe is None or user.datosextrauser.id_customer_stripe == "":
                # si no hay cliente lo creamos y guardamos su id
                stripe.api_key = local_settings.STRIPE_SECRET_KEY
                cliente_stripe = stripe.Customer.create(
                    description=user.username,
                    email=user.email
                )
                user.datosextrauser.id_customer_stripe = cliente_stripe['id']
                user.datosextrauser.save()

            checkout_session = funciones_stripe.guardar_tarjeta(user)
            return render(self.request, "checkout.html", {'user': user,
                                        'CHECKOUT_SESSION_ID': checkout_session.id})
        else:
            return render(self.request, "sesion_expirada.html", {})

@csrf_exempt
def eraserCards(request):
    try:
        datos = json.loads(request.POST['data'])
        usuario_id = datos.get("usuario_id")
        token = datos.get('token')
    except Exception as e:
        usuario_id = request.POST['usuario_id']
        token = request.POST['token']

    if comprobar_usuario(token, usuario_id):
        user = get_userdjango_by_token(token)
        funciones_stripe.borrar_todos_metodos_pago(user)
        response_data = {'result': 'ok', 'message': 'tarjetas borradas'}

    else:
        response_data = {'result': 'error', 'message': 'usuario incorrecto', 'codigo': "nice"}
    return JsonResponse(response_data)

@csrf_exempt
def get_tarjetas(request):
    try:
        try:
            datos = json.loads(request.POST['data'])
            token = datos.get("token")
            usuario_id = datos.get("usuario_id")
        except:
            usuario_id = request.POST['usuario_id']
            token = request.POST['token']

        if comprobar_usuario(token, usuario_id):
            user = get_userdjango_by_token(token)
            lista = []
            payment_methods = funciones_stripe.get_tarjetas(user)['data']
            # payment_methods = StripeCard.objects.filter(user=get_userdjango_by_token(token))
            created = 0
            pm = None
            if payment_methods is not None and payment_methods.__len__() > 0:
                for paymen_method in payment_methods:

                    if paymen_method['created'] > created:
                        created = paymen_method['created']
                        pm = paymen_method
                    else:
                        funciones_stripe.borrar_metodo_pago(paymen_method['id'])

                lista.append({'pk': pm['id'],
                              'caducidad': str(pm['card']['exp_month']) + "/" + str(pm['card']['exp_year']),
                              'end_digits': pm['card']['last4'],
                              'titular': "Tarjeta",
                              'tipo': pm['card']['brand']})
                response_data = {'result': 'ok', 'message': 'ok', 'lista': lista}
            else:
                response_data = {'result': 'no_cards', 'message': 'ok'}
        else:
            # print "error"
            response_data = {'result': 'error', 'message': 'no_ok'}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")
    except Exception as e:
        print(e)
        response_data = {'errorcode': 'U0005', 'result': 'error', 'message': 'Error en crear usuario. ' + str(e)}
        return http.HttpResponse(json.dumps(response_data), content_type="application/json")
# def generate_link(user):
#     random = get_random_string(length=30)
#     validacion_bd = Validacion.objects.create(usuario=user, validation_id=random)
#     link_validacion = 'https://example.com/validacion/' + str(user.pk) + "_" + validacion_bd.validation_id
#     return link_validacion