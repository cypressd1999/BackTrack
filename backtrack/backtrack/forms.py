from django import forms
from .models import Pbi

class PbiForm(forms.ModelForm):
    class Meta:
        model = Pbi
        fields = ('card', 'conversation', \
            'storypoints')
        