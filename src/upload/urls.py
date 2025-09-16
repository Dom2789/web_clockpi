from django.urls import path
from . import views

urlpatterns = [
    path('', views.file_list, name='file_list'),
    path('upload/', views.upload_file, name='upload_file'),
    path('file/<int:file_id>/', views.view_file, name='view_file'),
    path('selected/<int:file_id>/', views.view_selected, name='view_selected'),
]