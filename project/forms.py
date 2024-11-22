from django import forms
from .models import ResearchProject

class ResearchProjectForm(forms.ModelForm):
    class Meta:
        model = ResearchProject
        fields = ['title', 'description', 'start_date', 'end_date', 'status']
      
