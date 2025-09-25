from django.urls import path
from . import views

app_name = 'plot'

urlpatterns = [
    path('plot', views.plot_selection, name='plot_selection'),
    path('plot/<int:file_id>/', views.plot_data, name='plot_data'),
    path('api/data/<int:file_id>/', views.get_plot_data_api, name='plot_data_api'),
    path('api/files/', views.file_list_api, name='file_list_api'),
]