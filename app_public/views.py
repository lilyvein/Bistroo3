from django.shortcuts import render
import urllib.parse
from  urllib.request import urlopen
import json
from django.shortcuts import render
from django.views.generic import (TemplateView, ListView, CreateView, UpdateView, DetailView, DeleteView) # vaated mida kasutame
from django.conf import settings

from app_admin.models import Category
from .models import * # kõik mudelid
from django.urls import reverse_lazy
# Create your views here.


class HomeView(TemplateView):
    template_name = 'app_public/public_menu.html'


