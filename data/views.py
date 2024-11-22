import json
import os
from django.shortcuts import render, get_object_or_404, redirect
from .models import DataCollection, ResearchProject, Participant
from .forms import DataCollectionForm  # Assume you've created a form for DataCollection
from django.db.models import Count, Avg, Sum
from django.utils.timezone import now
from django.db.models.functions import TruncDate


# List all DataCollections for a specific project
def data_collection_list(request, project_id):
    project = get_object_or_404(ResearchProject, id=project_id)
    data_collections = project.data_collections.all()
    print(data_collections[0].data.url)
    return render(request, 'data_collection_list.html', {'project': project, 'data_collections': data_collections})

# Create a new DataCollection for a specific project and participant
def data_collection_create(request, project_id):
    project = get_object_or_404(ResearchProject, id=project_id)

    if request.method == 'POST':
        form = DataCollectionForm(request.POST, request.FILES)
        if form.is_valid():
            data_collection = form.save(commit=False)
            data_collection.project = project
            data_collection.save()
            return redirect('data_collection_list', project_id=project.id)
    else:
        form = DataCollectionForm()
    return render(request, 'data_collection_form.html', {'form': form})

# Detail view for a specific DataCollection
def data_collection_detail(request, project_id, data_collection_id):
    data_collection = get_object_or_404(DataCollection, id=data_collection_id, project_id=project_id)
    return render(request, 'data_collection_detail.html', {'data_collection': data_collection})

# Update an existing DataCollection
def data_collection_update(request, project_id, data_collection_id):
    data_collection = get_object_or_404(DataCollection, id=data_collection_id, project_id=project_id)
    if request.method == 'POST':
        form = DataCollectionForm(request.POST, request.FILES, instance=data_collection)
        if form.is_valid():
            form.save()
            return redirect('data_collection_detail', project_id=project_id, data_collection_id=data_collection.id)
    else:
        form = DataCollectionForm(instance=data_collection)
    return render(request, 'data_collection_form.html', {'form': form, 'project_id': project_id})

# Delete a DataCollection
def data_collection_delete(request, project_id, data_collection_id):
    data_collection = get_object_or_404(DataCollection, id=data_collection_id, project_id=project_id)
    if request.method == 'POST':
        data_collection.delete()
        return redirect('data_collection_list', project_id=project_id)
    return render(request, 'data_collection_confirm_delete.html', {'data_collection': data_collection})



def dashboard_view(request, project_id):
    project = project = get_object_or_404(ResearchProject, id=project_id)
    # Total number of participants
    total_participants = Participant.objects.filter(project=project).count()

    # Total number of data collected
    total_data_collected = DataCollection.objects.filter(project=project).count()

    # Average data collected by a participant
    avg_data_collected_per_participant = (
        total_data_collected / total_participants if total_participants > 0 else 0
    )

    # Participants over time (grouped by enrollment date)
    participants_over_time = (
        Participant.objects.filter(project=project).annotate(date_joined=TruncDate("user__date_joined"))
        .values("date_joined")
        .annotate(count=Count("id"))
        .order_by("date_joined")
    )
    participants_chart_data = {
        "labels": [str(entry["date_joined"]) for entry in participants_over_time],
        "data": [entry["count"] for entry in participants_over_time],
    }

    # Data collection over time (grouped by submission date)
    data_over_time = (
        DataCollection.objects.filter(project=project).annotate(date_submitted=TruncDate("data_submission_date"))
        .values("date_submitted")
        .annotate(count=Count("id"))
        .order_by("date_submitted")
    )
    data_collection_chart_data = {
        "labels": [str(entry["date_submitted"]) for entry in data_over_time],
        "data": [entry["count"] for entry in data_over_time],
    }

    # Data size over time (grouped by submission date, summed in KB)
    data_size_over_time = []
    for entry in data_over_time:
        date = entry["date_submitted"]
        size_for_date = 0
        data_entries = DataCollection.objects.filter(
            data_submission_date__date=date,
            project=project
        )  # Filter entries for this date
        for data_entry in data_entries:
            if data_entry.data and os.path.exists(data_entry.data.path):
                size_for_date += os.path.getsize(data_entry.data.path)  # Size in bytes
        data_size_over_time.append({"date": date, "total_size": size_for_date})

    data_size_chart_data = {
        "labels": [str(entry["date"]) for entry in data_size_over_time],
        "data": [
            entry["total_size"] / 1024 if entry["total_size"] else 0
            for entry in data_size_over_time
        ],  # Convert to KB
    }

    context = {
        "total_participants": total_participants,
        "total_data_collected": total_data_collected,
        "avg_data_collected_per_participant": avg_data_collected_per_participant,
        "participants_chart_data": participants_chart_data,
        "data_collection_chart_data": data_collection_chart_data,
        "data_size_chart_data": data_size_chart_data,
    }
    print(context)
    return render(request, "dashboard.html", context)
