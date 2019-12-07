from django import forms
from .models import *

class PBIForm(forms.ModelForm):
    class Meta:
        model = PBI
        fields = ('title', 'card', 'conversation', \
            'storypoints', 'priority','status')

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
                ).filter(status=PBI.NOTSTARTED)

    class Meta:
        model = SprintBacklog
        fields = ('hours_available', 'pbi')
        field_classes = {
            'pbi': PBIMultipleChoice
        }
        widgets = {
            'pbi': forms.CheckboxSelectMultiple
        }

class DeletePBIFromSBForm(forms.Form):
    pbi = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple
    )
    
    def __init__(self, *args, **kwargs):
        try:
            sb_id = kwargs.pop('pk')
            sb = SprintBacklog.objects.get(pk=sb_id)
        except (KeyError, SprintBacklog.DoesNotExist):
            super().__init__(*args, **kwargs)
            self.fields['pbi'].queryset = PBI.objects.all()
        else:
            super().__init__(*args, **kwargs)
            self.fields['pbi'].queryset = sb.pbi.all()

    def clean_pbi(self):
        selected_pbis = self.cleaned_data['pbi']
        if self.fields['pbi'].queryset.count()-len(selected_pbis)<1:
            raise forms.ValidationError("The sprint backlog must "
                    "contain at least 1 pbi!")
        return selected_pbis

class AddPBIToSBForm(forms.Form):
    pbi = forms.ModelMultipleChoiceField(
        queryset=PBI.objects.filter(status=PBI.NOTSTARTED),
        widget=forms.CheckboxSelectMultiple
    )

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

class InviteDeveloperForm(forms.Form):
    dev = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(
            role=User.DEVELOPER
        ).filter(developer__project=None),
        widget=forms.CheckboxSelectMultiple
    )

class InviteProductOwnerForm(forms.Form):
    product_owner = forms.ModelChoiceField(
        queryset=User.objects.filter(role=User.PRODUCTOWNER)
    )

class InviteScrumMasterForm(forms.Form):
    scrum_master = forms.ModelChoiceField(
        queryset=User.objects.filter(role=User.SCRUMMASTER)
    )