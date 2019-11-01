from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from . import models
from backtrack.forms import PBIForm, CreateProjectForm

def addPBI(request, project_name):
    form = PBIForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            new_pbi = form.save(commit=False)
            project = get_object_or_404(
                models.Project,
                name=project_name
            )
            pb = get_object_or_404(
                models.ProductBacklog,
                project=project
            )
            new_pbi.product_backlog = pb
            new_pbi.save()
            return HttpResponse("pbi saved")
    else:
        return render(request, "backtrack/addpbi.html", \
            {"form": form})

def createProject(request):
    form = CreateProjectForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            new_project = form.save()
            new_pb = models.ProductBacklog.objects.create(
                project=new_project
            )
            new_pb.save()
            return HttpResponse("project saved")
    else:
        return render(
            request,
            "backtrack/create_project.html",
            {"form": form}
        )