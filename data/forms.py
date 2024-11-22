# forms.py
from django import forms
from .models import DataCollection

class DataCollectionForm(forms.ModelForm):
    class Meta:
        model = DataCollection
        fields = ['data', 'participant']
