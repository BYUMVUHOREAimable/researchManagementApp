from django.urls import include, path
from . import views
from data.views import dashboard_view
urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('<int:pk>/', views.project_detail, name='project_detail'),
    path('<int:pk_project>/participants/', include('users.urls')),
    path('<int:project_id>/data/', include('data.urls')),
    path('<int:project_id>/analytics/', dashboard_view, name='analytics'),
    path('new/', views.project_create, name='project_create'),
    path('<int:pk>/edit/', views.project_update, name='project_update'),
    path('<int:pk>/delete/', views.project_delete, name='project_delete'),
]
