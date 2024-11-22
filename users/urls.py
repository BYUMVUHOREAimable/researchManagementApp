from django.urls import path
from . import views

urlpatterns = [
    path('', views.participant_list, name='participant_list'),
    path('<int:pk>/', views.participant_detail, name='participant_detail'),
    path('new/', views.participant_create, name='participant_create'),
    path('<int:pk>/edit/', views.participant_update, name='participant_update'),
    path('<int:pk>/delete/', views.participant_delete, name='participant_delete'),
]
