from django.urls import path
from . import views

urlpatterns = [
    path('research-projects/', views.get_research_projects, name='research-projects'),
    path('research-projects/<int:project_id>/data/', views.get_project_with_data, name='project-with-data'),
]