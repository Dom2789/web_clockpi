from django.urls import path
from . import views

app_name = 'plot'

urlpatterns = [
    path('plot', views.plot_selection, name='plot_selection'),
    path('plot/<int:file_id>/', views.plot_data, name='plot_data'),
    path('custom/<int:file_id>/', views.custom_plot_view, name='custom_plot'),  # ← custom_plot
    path('api/data/<int:file_id>/', views.get_plot_data_api, name='plot_data_api'),  # ← plot_data_api
    path('download/<int:file_id>/<str:plot_type>/', views.download_plot, name='download_plot'),
]