from django import forms
from .models import *

class PBIForm(forms.ModelForm):
    class Meta:
        model = PBI
        fields = ('title', 'card', 'conversation', \
            'storypoints', 'priority')

class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name',)

class PBIMultipleChoice(forms.ModelMultipleChoiceField):
    def label_from_instance(self, object):
        return "%s" % object.title

class SBForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        try:
            self.project_name = kwargs.pop('project_name')
        except KeyError:
            super().__init__(*args, **kwargs)
        else:
            super().__init__(*args, **kwargs)
            self.fields['pbi'].queryset = \
                PBI.objects.filter(
                    product_backlog__project__name=\
                        self.project_name
                ).exclude(status=PBI.FINISHED)

    class Meta:
        model = SprintBacklog
        fields = ('hours_available', 'pbi')
        field_classes = {
            'pbi': PBIMultipleChoice
        }
        widgets = {
            'pbi': forms.CheckboxSelectMultiple
        }

class TaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        try:
            self.sprintbacklog = kwargs.pop('sprint_backlog')
        except KeyError:
            super().__init__(*args, **kwargs)
        else:
            super().__init__(*args, **kwargs)
            self.fields['pbi'].queryset = \
                PBI.objects.filter(
                    sprintbacklog=\
                        self.sprintbacklog
                )

    class Meta:
        model = Task
        fields = ('title', 'description', 'total_hours', 'pbi')
