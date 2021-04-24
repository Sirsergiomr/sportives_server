# -*- encoding: utf-8 -*-
from django.core.mail import send_mail

from usuarios import forms, models
from usuarios import forms
from django.views.generic import ListView, FormView, DeleteView,CreateView, UpdateView
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, get_object_or_404
import django.http as http
from django.urls import reverse
from django.utils.encoding import smart_str
from django.contrib.auth.models import User
from annoying.functions import get_object_or_None
#from utilidades import enviarmail,contrasena
import datetime
from django.utils.timezone import utc
from django.db.models import Q


from django.http import HttpResponse
from django.contrib import auth
import json
from django.views.decorators.csrf import csrf_exempt

class Prueba(CreateView):
    template_name = 'admin/prueba.html'

    def get(self, request, *args, **kwargs):
        return render(request,self.template_name,{})