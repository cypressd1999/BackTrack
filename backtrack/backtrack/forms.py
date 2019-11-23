from django import forms
from .models import *

class PBIForm(forms.ModelForm):
    class Meta:
        model = PBI
        fields = ('title', 'card', 'conversation', \
            'storypoints', 'priority')

PBIFormSet = forms.inlineformset_factory(
    PBI, Confirmation, fields=('content', 'done')
)

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

class UpdateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', \
            'total_hours', 'finished_hours')

    def clean(self):
        cleaned_data = super().clean()
        finished_hours = cleaned_data.get('finished_hours')
        total_hours = cleaned_data.get('total_hours')
        if finished_hours > total_hours:
            raise forms.ValidationError("The finished hours \
                exceeds the total hours!")

class ConfirmationForm(forms.ModelForm):
    class Meta:
        model = Confirmation
        fields = ('content', 'done')