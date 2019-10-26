from django.shortcuts import render
from django.views.generic import TemplateView 
from backtrack.models import Pbi
from django.views.generic.list import ListView
# Create your views here.

class PB(ListView): 
    template_name = "pb.html" 
    model = Pbi