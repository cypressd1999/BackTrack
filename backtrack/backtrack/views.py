from django.http import HttpResponseRedirect, HttpResponse, \
    JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, \
    UpdateView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.views import LoginView
from django.db.models import Q

from backtrack.models import *
from backtrack.forms import *

class AddPBI(CreateView):
    form_class = PBIForm
    template_name = "backtrack/addpbi.html"

    def form_valid(self, form):
        project = get_object_or_404(
                Project,
                name=self.kwargs.get('project_name')
        )
        new_pbi = form.save(commit=False)
        pb = ProductBacklog.objects.get(
            project=self.kwargs.get('project_name')
        )
        new_pbi.product_backlog = pb
        if new_pbi.storypoints:
            pb.total_story_points += new_pbi.storypoints
            pb.remaining_story_points += new_pbi.storypoints
            pb.save()
        new_pbi.save()
        return super().form_valid(form)

class CreateProject(CreateView):
    model = Project
    fields = ['name']
    template_name = 'backtrack/create_project.html'

    def form_valid(self, form):
        form.save()
        new_pb = ProductBacklog.objects.create(
                project=form.instance
            )
        new_pb.save()
        return super().form_valid(form)

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
                return render(
                    request,
                    'backtrack/delete_pbi.html',
                    {'project': project,
                    'error_message':\
                        "You cannot delete a started pbi"
                    }
                )
            if selected_pbi.storypoints:
                pb.total_story_points -= \
                    selected_pbi.storypoints
                pb.remaining_story_points -= \
                    selected_pbi.storypoints
            selected_pbi.delete()
            pb.save()
        return HttpResponseRedirect(
            reverse('backtrack:view pb', 
            kwargs={'project_name': project_name})
        )

class CreateSB(CreateView):
    form_class = SBForm
    template_name = "backtrack/create_sb.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_name'] = \
            self.kwargs.get('project_name')
        return context

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


class AddTask(CreateView):
    form_class = TaskForm
    template_name = 'backtrack/addtask.html'
    current_sprint = None

    def dispatch(self, request, *args, **kwargs):
        self.current_sprint = SprintBacklog.objects.filter(
                Q(is_current_sprint=True),
                Q(pbi__product_backlog__project__name=\
                    kwargs.get('project_name'))
            )[0]
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'sprint_backlog': self.current_sprint
        })
        return kwargs

    def form_valid(self, form):
        form.instance.sprint_backlog = self.current_sprint
        user = self.request.user
        form.instance.developer = Developer.objects.get(user=user)
        return super().form_valid(form)

class UpdateTask(UpdateView):
    form_class = UpdateTaskForm
    model = Task
    template_name = "backtrack/update_task.html"

    def form_valid(self, form):
        if form.has_changed() and \
            ('finished_hours' in form.changed_data or \
                'total_hours' in form.changed_data):
            if form.instance.finished_hours == 0:
                form.instance.status = Task.NOTSTARTED
            elif form.instance.finished_hours < \
                form.instance.total_hours:
                form.instance.status = Task.INPROGRESS
            else:
                form.instance.status = Task.FINISHED
        return super().form_valid(form)

def ajax_change_contrib(request):
    user = request.user
    task_id = request.GET.get('task_id')
    sb_id = request.GET.get('sb_id')
    task = Task.objects.get(pk=task_id)
    task.developer = user.developer
    task.save()
    arg = {'success': True}
    return JsonResponse(arg)

class PBView(ListView):
    model = PBI
    template_name = "backtrack/view_pb.html"

    def get_queryset(self):
        return PBI.objects.filter(
            product_backlog__project__name=\
                self.kwargs.get('project_name')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_name']= self.kwargs.get('project_name')
        pbi_list = self.get_queryset()
        CumStoryPoints = [0]
        inf = False
        for pbi in pbi_list:
            if inf:
                CumStoryPoints.append('inf')
            elif pbi.storypoints is None:
                inf = True
                CumStoryPoints.append('inf')
            else :
                CumStoryPoints.append(
                    CumStoryPoints[-1]+pbi.storypoints
                )
        context['CumStoryPoints'] = CumStoryPoints
        return context

class SBView(ListView):
    model = SprintBacklog
    template_name = "backtrack/sb_view.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['project_name']= self.kwargs.get('project_name')
        sprintbacklog_list = SprintBacklog.objects.filter(
            pbi__product_backlog__project__name=\
                self.kwargs.get('project_name')
        ).distinct().order_by('sprint_number')
        storypoints_list = []
        for sb in sprintbacklog_list:
            s = 0
            for pbi in sb.pbi.all():
                if pbi.storypoints is None:
                    s = 'Not decided'
                    break
                else:
                    s += pbi.storypoints
            storypoints_list.append(s)
        context['sprintbacklog_list'] = sprintbacklog_list
        context['storypoints_list'] = storypoints_list
        return context

class TaskView(ListView, SingleObjectMixin):
    template_name = "backtrack/task_view.html"

    class RowData:
        def __init__(self, pbi, task_category, 
                finished_hours, total_hours):
            self.pbi = pbi
            self.task_category = task_category
            self.finished_hours = finished_hours
            self.total_hours = total_hours
            self.remaining_hours = total_hours - finished_hours

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(
                queryset=SprintBacklog.objects.all()
            )
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.GET.get('view_my_task'):
            context['view_my_task'] = True
        else:
            context['view_my_task'] = False
        pbi_list = self.get_queryset()
        row_data_list = []
        total_storypoints = 0; inf = False
        for pbi in pbi_list:
            if not inf:
                if pbi.storypoints is None:
                    inf = True
                    total_storypoints = 'inf'
                else:
                    total_storypoints += pbi.storypoints
            task_no = []; task_inp = []; task_fn = []
            finished_hours = 0
            total_hours = 0
            for task in pbi.task_set.all():
                if task.sprint_backlog.id != self.object.id:
                    continue
                if context['view_my_task'] and task.developer != \
                        self.request.user.developer:
                    continue
                if task.status == Task.NOTSTARTED:
                    task_no.append(task)
                elif task.status == Task.INPROGRESS:
                    task_inp.append(task)
                elif task.status == Task.FINISHED:
                    task_fn.append(task)
                finished_hours += task.finished_hours
                total_hours += task.total_hours
            task_category = [task_no, task_inp, task_fn]
            row_data_list.append(
                self.RowData(
                    pbi,task_category,
                    finished_hours, total_hours
                )
            )
        context['sb'] = self.object
        context['pk'] = self.object.pk
        context['row_data_list'] = row_data_list
        context['total_storypoints'] = total_storypoints
        context['hours_available'] = self.object.hours_available
        context['project_name'] = \
            self.object.pbi.all()[0].product_backlog.project.name
        return context
                    
    def get_queryset(self):
        return self.object.pbi.all()

class ViewPBI(ListView, SingleObjectMixin):
    template_name = 'backtrack/view_pbi.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(
            queryset=PBI.objects.all()
        )
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *kwargs):
        context = super().get_context_data(*kwargs)
        context['pbi'] = self.object
        context['confirmation_list'] = self.get_queryset()
        context['project_name'] = \
            self.object.product_backlog.project.name
        context['pk'] = self.object.pk
        return context
        
    def get_queryset(self):
        return self.object.confirmation_set.all()

class ModifyPBI(UpdateView):
    model = PBI
    form_class = PBIForm
    template_name = "backtrack/modify_pbi.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        confirmation_form = PBIFormSet(instance=self.object)
        return self.render_to_response(
            self.get_context_data(
                form=form,
                confirmation_form=confirmation_form
            )
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        confirmation_form = PBIFormSet(
            instance=self.object, 
            data=request.POST
        )
        if form.is_valid() and confirmation_form.is_valid():
            return self.form_valid(form, confirmation_form)
        else:
            return self.form_invalid(form, confirmation_form)
    
    def form_valid(self, form, confirmation_form):
        if form.has_changed():
            form.save()
        if confirmation_form.has_changed():
            confirmation_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, confirmation_form):
        return self.render_to_response(self.get_context_data(
            form=form, confirmation_form=confirmation_form
        ))

class AddConfirmation(CreateView):
    template_name = 'backtrack/confirmation_form.html'
    form_class = ConfirmationForm

    def form_valid(self, form):
        pbi = PBI.objects.get(pk=self.kwargs.get('pk'))
        form.instance.pbi = pbi
        return super().form_valid(form)

class LoginView(LoginView):
    template_name = 'backtrack/login.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['next'] = reverse('backtrack:view task',
        kwargs={'pk': 1})
        return context