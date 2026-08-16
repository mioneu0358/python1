"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
"""

from django.urls import path
from .views import *

app_name = "projects"

urlpatterns = [
    path('dashboard/', std_dashboard_view, name='std_dashboard'),
    path('api/journals/', get_journals, name='get_journals'),
    path('api/journals/save/', save_journal, name='save_journal'),
    path('api/journals/delete/', delete_journal, name='delete_journal'),  
    path('list/',project_list, name='list'),
    path("create/", project_create,name='create'),
    path('upload-image/', upload_image, name='upload_image'),
    path('<int:pk>/', project_detail, name='detail'),
    path('api/blocks/<int:block_id>/memo/', add_memo, name='add_memo'),
    path('<int:pk>/edit/', project_edit, name='edit'),
]
