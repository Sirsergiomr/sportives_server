
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from usuarios import views_admin, views

urlpatterns = [


    url(r'^prueba/$', login_required(views_admin.Prueba.as_view()), name='prueba_custom'),


]