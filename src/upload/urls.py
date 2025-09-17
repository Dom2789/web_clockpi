from django.urls import path
from . import views

urlpatterns = [
    path('', views.file_list, name='file_list'),
    path('select/', views.select_file, name='select_file'),
    path('refresh/', views.refresh_files, name='refresh_files'),
    path('file/<int:file_id>/', views.view_file, name='view_file'),
    path('selected/<int:file_id>/', views.view_selected, name='view_selected'),
]