"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to  For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', home, name='home')
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
    path('api/blocks/<int:block_id>/memo/', add_memo, name='add_memo'),
    path('<int:pk>/edit/', project_edit, name='edit'),
    path('api/search-users/', api_search_users, name='api_search_users'),
    path('<int:pk>/', project_detail, name='detail'),
    path('api/checklist/<int:pk>/toggle/', toggle_checklist, name='toggle_checklist'),
    path('api/create-team/', api_create_team, name='api_create_team'),
    path('api/teams/<int:team_id>/members/', api_get_team_members, name='api_team_members'),

    path('<int:project_id>/api/tree/', api_get_vfs_tree, name='api_vfs_tree'),
    path('<int:project_id>/api/folder/create/', api_create_folder, name='api_create_folder'),
    path('<int:project_id>/api/file/create/', api_create_file, name='api_create_file'),
    path('<int:project_id>/vfs/', project_vfs, name='vfs'),

    path('<int:project_id>/api/vfs/delete/', api_delete_vfs_item, name='api_delete_vfs_item'),
    path('<int:project_id>/api/backup/', api_backup_project, name='api_backup_project'),


    path('<int:project_id>/api/file/<int:file_id>/', api_get_file_content, name='api_get_file_content'),
    path('<int:project_id>/api/file/<int:file_id>/save/', api_save_file_content, name='api_save_file_content'),


    path('test/', test, name='test'),
]
