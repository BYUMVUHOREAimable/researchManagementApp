from django.shortcuts import render

# Create your views here.
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from django.shortcuts import render, get_object_or_404, redirect

from project.models import ResearchProject
from .models import Participant
from .forms import ParticipantForm
from .forms import SignUpForm


class HomeView(TemplateView):
    template_name = "home.html"


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("/")
        print(form.errors)
    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect("/")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

# List View
def participant_list(request, pk_project):
    print(pk_project)
    participants = Participant.objects.all()
    return render(request, 'participant_list.html', {'participants': participants})

# Detail View
def participant_detail(request, pk_project,pk):
    participant = get_object_or_404(Participant, pk=pk)
    return render(request, 'participant_detail.html', {'participant': participant})

# Create View
def participant_create(request, pk_project):
    if request.method == "POST":
        form = ParticipantForm(request.POST)
        if form.is_valid():
            project = get_object_or_404(ResearchProject, pk=pk_project)
            form.instance.project = project
            form.save()
            return redirect('participant_list', pk_project=pk_project)
    else:
        form = ParticipantForm()
    return render(request, 'participant_form.html', {'form': form})

# Update View
def participant_update(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == "POST":
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            return redirect('participant_list')
    else:
        form = ParticipantForm(instance=participant)
    return render(request, 'participant_form.html', {'form': form})

# Delete View
def participant_delete(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    if request.method == "POST":
        participant.delete()
        return redirect('participant_list')
    return render(request, 'participant_confirm_delete.html', {'participant': participant})



import requests
import pandas as pd
try:
    vehicle_api = requests.get('http://127.0.0.1:8000/vehicle_api')
    vehicle_api.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
    vehicle_api_data = vehicle_api.json()
    vehicle_owners_api = requests.get('http://127.0.0.1:8000/vehicle_owners_api')
    vehicle_owners_api.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
    vehicle_owners_api_data = vehicle_owners_api.json()
    vdf = pd.DataFrame(vehicle_api_data['vehicles'])
    odf = pd.DataFrame(vehicle_owners_api_data['owners'])
except requests.exceptions.RequestException as e:
    print(f"Error fetching data from API: {e}")
