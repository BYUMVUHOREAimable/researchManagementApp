from django.urls import path
from . import views

urlpatterns = [
    path('', views.data_collection_list, name='data_collection_list'),
    path('<int:data_collection_id>/', views.data_collection_detail, name='data_collection_detail'),
    path('add/', views.data_collection_create, name='data_collection_create'),
    path('<int:data_collection_id>/edit/', views.data_collection_update, name='data_collection_update'),
    path('<int:data_collection_id>/delete/', views.data_collection_delete, name='data_collection_delete'),
    path('api/research-projects/', views.get_research_projects, name='research-projects'),
    path('api/research-projects/<int:project_id>/data/', views.get_project_with_data, name='project-with-data'),
    
]
