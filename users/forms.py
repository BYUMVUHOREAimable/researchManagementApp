
from django import forms
from .models import Participant
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text="Required")

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['user', 'status', 'project']
