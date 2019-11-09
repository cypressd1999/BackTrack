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
            if new_pbi.storypoints:
                pb.total_story_points += new_pbi.storypoints
                pb.remaining_story_points += new_pbi.storypoints
                pb.save()
            new_pbi.save()
            return HttpResponse("<h1>pbi saved</h1>")
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
            return HttpResponse("<h1>project saved</h1>")
    else:
        return render(
            request,
            "backtrack/create_project.html",
            {"form": form}
        )

def deletePBI(request, project_name):
    project = get_object_or_404(models.Project, pk=project_name)
    if request.method == 'GET':
        return render(request, 'backtrack/delete_pbi.html', \
            {'project': project})
    try:
        selected_pbis = []
        pb = project.productbacklog
        for pbi in request.POST.getlist('pbi'):
            selected_pbis.append(
                pb.pbi_set.get(pk=pbi)
            )
    except (KeyError, models.PBI.DoesNotExist):
        return render(
            request,
            'backtrack/delete_pbi.html',
            {
                'project': project,
                'error_message': "You didn't select a pbi"
            }
        )
    else:
        for selected_pbi in selected_pbis:
            if selected_pbi.status != models.PBI.NOTSTARTED:
                return render(request,'backtrack/delete_pbi.html',
                    {'project': project,
                    'error_message':\
                        "You cannot delete a started pbi"
                    }
                )
            if selected_pbi.storypoints:
                pb.total_story_points -= selected_pbi.storypoints
                pb.remaining_story_points -= \
                    selected_pbi.storypoints
            selected_pbi.delete()
            pb.save()
        return HttpResponse('deleted')