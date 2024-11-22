from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import ResearchProject
from .forms import ResearchProjectForm

# List View
def project_list(request):
    projects = ResearchProject.objects.all()
    return render(request, 'project_list.html', {'projects': projects})

# Detail View
def project_detail(request, pk):
    project = get_object_or_404(ResearchProject, pk=pk)
    return render(request, 'project_detail.html', {'project': project})

# Create View
@login_required
def project_create(request):
    if request.method == "POST":
        form = ResearchProjectForm(request.POST)
        if form.is_valid():
            form.instance.created_by = request.user
            form.save()
            return redirect('project_list')
    else:
        form = ResearchProjectForm()
    return render(request, 'project_form.html', {'form': form})

# Update View
def project_update(request, pk):
    project = get_object_or_404(ResearchProject, pk=pk)
    if request.method == "POST":
        form = ResearchProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    else:
        form = ResearchProjectForm(instance=project)
    return render(request, 'project_form.html', {'form': form})

# Delete View
def project_delete(request, pk):
    project = get_object_or_404(ResearchProject, pk=pk)
    if request.method == "POST":
        project.delete()
        return redirect('project_list')
    return render(request, 'project_confirm_delete.html', {'project': project})
