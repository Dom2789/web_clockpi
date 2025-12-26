from django.urls import path
from . import views

app_name = 'ledcontrol'

urlpatterns = [
    path('led',views.led_control , name='led_control'),

]