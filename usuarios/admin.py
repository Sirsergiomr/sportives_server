from django.contrib import admin
from usuarios.models import *

admin.site.register(Tokenregister)
class DatosExtraAdmin(admin.ModelAdmin):
    list_display = ["usuario"]
admin.site.register(DatosExtraUser,DatosExtraAdmin)
admin.site.register(Validacion)
admin.site.register(Maquina)
admin.site.register(Entrenamiento)
admin.site.register(Activiadad)

