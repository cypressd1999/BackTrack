from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView
from django.db.models import Q

from backtrack.models import *
from backtrack.forms import *

def addPBI(request, project_name):
    form = PBIForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            new_pbi = form.save(commit=False)
            project = get_object_or_404(
                Project,
                name=project_name
            )
            pb = get_object_or_404(
                ProductBacklog,
                project=project
            )
            new_pbi.product_backlog = pb
            if new_pbi.storypoints:
                pb.total_story_points += new_pbi.storypoints
                pb.remaining_story_points += new_pbi.storypoints
                pb.save()
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
            new_pb = ProductBacklog.objects.create(
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

def deletePBI(request, project_name):
    project = get_object_or_404(Project, pk=project_name)
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
    except (KeyError, PBI.DoesNotExist):
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
            if selected_pbi.status != PBI.NOTSTARTED:
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
"""
def createSB(request, project_name):
    project = get_object_or_404(Project, pk=project_name)
    form = SBForm(
        request.POST or None,
        project_name=project_name
    )
    if request.method == 'POST':
        if form.is_valid():
            sb = form.save(commit=False)
            sb.sprint_number = 1
            sb.save()
            form.save_m2m()
            return HttpResponse("save fine")
    else:
        return render(
            request,
            "backtrack/create_sb.html",
            {"form": form}
        )
"""
class createSB(CreateView):
    form_class = SBForm
    template_name = "backtrack/create_sb.html"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'project_name': self.kwargs.get('project_name')
        })
        return kwargs

    def form_valid(self, form):
        last_sprint = \
            SprintBacklog.objects.filter(
                Q(is_current_sprint=True),
                Q(pbi__product_backlog__project__name=\
                    self.kwargs.get('project_name'))
            )
        if len(last_sprint) == 0:
            form.instance.sprint_number = 1
            form.instance.is_current_sprint = True
        else:
            last_sprint = last_sprint[0]
            form.instance.sprint_number = \
                last_sprint.sprint_number + 1
            last_sprint.is_current_sprint = False
            form.instance.is_current_sprint = True
            last_sprint.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('backtrack:create project')

#class createTask(CreateView):