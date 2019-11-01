from django import forms
from .models import PBI, Project

class PBIForm(forms.ModelForm):
    class Meta:
        model = PBI
        fields = ('title', 'card', 'conversation', \
            'storypoints', 'priority')

class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name',)