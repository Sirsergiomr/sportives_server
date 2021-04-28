# -*- encoding: utf-8 -*-
import os

import qrcode
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.template.defaultfilters import slugify



class DatosExtraUser(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="imagenes/perfiles", default="imagenes/perfiles/usuario.png")
    publicidad = models.BooleanField(default=False)
    onesignal_id = models.CharField(max_length=40, null=True, blank=True)
    onesignal_registration = models.CharField(max_length=70, null=True, blank=True)
    tipo = models.CharField(max_length=8, blank=False, null=False, default="django")
    saldo = models.IntegerField(default=0)  # saldo en centimos
    recibir_comunicaciones = models.BooleanField(default=False)
    validado = models.BooleanField(default=False)
    descripcion = models.CharField(max_length=240, blank=True, null=True)
    id_customer_stripe = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return u"%s" % self.usuario.username

    def toJSON(self):
        json = {'pk': self.pk,
                'nombre': self.usuario.first_name,
                'apellido': self.usuario.last_name,
                'email': self.usuario.email,
                'publicidad': self.publicidad,
                'imagen': str(self.imagen),
                'recibir_comunicaciones': bool(self.recibir_comunicaciones),
                'descripcion': self.descripcion,
                'tipo': self.tipo
                }
        return json


def user_new_unicode(self):
    return self.username  # if self.get_full_name() == "" else self.get_full_name()


# Replace the __unicode__ method in the User class with out new implementation
User.__unicode__ = user_new_unicode

def upload_maquina(instance, filename):
    return os.path.join("maquinas/%s" % instance.usuario.slug, filename)


def generar_qr(cadena):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4
        )

        info = cadena

        qr.add_data(info)
        qr.make(fit=True)
        imagen = qr.make_image()
        filename = 'codigo_' + str(cadena) + '.png'
        imagen.save('static/media/'+filename)
        return filename

class Maquina(models.Model):
    Nombre_maquina = models.CharField(max_length=55,blank=True)
    slug = models.SlugField(max_length=50, editable=False)
    foto = models.ImageField(upload_to=upload_maquina, blank=True, null=True)
    print('Foto name : '+str(foto.name))
    def save(self, *args, **kwargs):
            self.slug = slugify(self.Nombre_maquina)
            super(Maquina, self).save(*args, **kwargs)
            self.foto = generar_qr(self.pk)
            super(Maquina, self).save(*args, **kwargs)

    def __str__(self):
        return u"%s" % self.Nombre_maquina

    def toJSON(self):
        json = {'pk': self.pk,
                'nombre':self.Nombre_maquina,
                'foto': str(self.foto)}
        return json


class Entrenamiento(models.Model):
    usuario = models.ForeignKey(User,on_delete=models.CASCADE)
    Nombre_maquina = models.CharField(max_length=55, blank=True)
    fecha = models.DateField(auto_now_add=False)
    hora = models.TimeField(auto_now_add=False)
    tiempo_uso = models.TimeField(default='00:00:00')

    def toJSON(self):
        json = {'pk': self.pk,
                'usuario_pk': self.usuario.pk,
                'usuario_username': self.usuario.username,
                'fecha': self.fecha,
                'hora':self.hora,
                'nombre_maquina': self.Nombre_maquina,
                'tiempo_uso':self.tiempo_uso
                }
        return json
class Actividad(models.Model):
    usuario  = models.ForeignKey(User,on_delete=models.CASCADE)

    fecha = models.DateField(auto_now_add=False)

    nombre_actividad = models.CharField(max_length=55, blank=True, null=True)
    descripcion = models.CharField(max_length=240, blank=True, null=True)
    def __str__(self):
        return u"%s" % self.nombre_actividad
    def toJSON(self):
        json = {'pk': self.pk,
                'nombre':self.nombre_actividad,
                'usuario_pk': self.usuario.pk,
                'usuario_username': self.usuario.username,
                'fecha':str(self.fecha),
                'descripcion': self.descripcion,
                }
        return json

class Tokenregister(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=80)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return u"%s" % self.user.username

class Validacion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    validation_id = models.CharField(max_length=55, null=False, blank=False)
    expire = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return u"%s" % self.usuario.username + "-" + u"%s" % self.validation_id
