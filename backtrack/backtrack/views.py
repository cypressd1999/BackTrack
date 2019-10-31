from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from . import models
from backtrack.forms import PBIForm

def addPBI(request):
    form = PBIForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return HttpResponse("saved")
    else:
        return render(request, "backtrack/pb.html", \
            {"form": form})