from django.urls import path
from . import views

urlpatterns = [
    path('view_selected', views.file_list, name='file_list'),
    path('select/', views.select_file, name='select_file'),
    path('refresh/', views.refresh_files, name='refresh_files'),
    path('file/<int:file_id>/', views.view_file, name='view_file'),
    path('selected/<int:file_id>/', views.view_selected, name='view_selected'),
    path('select-all/<int:file_id>/', views.select_all_lines, name='select_all_lines'),
    path('clear-all/<int:file_id>/', views.clear_all_selections, name='clear_all_selections'),
]