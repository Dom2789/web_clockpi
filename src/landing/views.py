from django.shortcuts import render
from django.conf import settings
from datetime import datetime, timedelta
import os

def landing_page(request):
    """
    View to display weather dashboard
    Pass weather data from your weather API to the template
    """
    
    # Calculate times for forecasts
    now = datetime.now()
    time_3h = now + timedelta(hours=3)
    time_6h = now + timedelta(hours=6)
    time_9h = now + timedelta(hours=9)
    
    # Example weather data structure
    # Replace this with actual data from your weather API
    context = {
        'city' : 'Waidhaus',
        'sunrise': '06:00:00',
        'sunset' : '18:00:00',
        'current': {
            'time': 'Now',
            'temp': 22,
            'feelslike' : 27,
            'description' : 'clouds',
            'wind_speed': 150,
            'wind_direction': 'NW'
        },
        'forecast_3h': {
            'time': time_3h.strftime('%H:%M'),
            'temp': 20,
            'feelslike' : 27,
            'description' : 'clouds',
            'wind_speed': 12,
            'wind_direction': 'N'
        },
        'forecast_6h': {
            'time': time_6h.strftime('%H:%M'),
            'temp': 18,
            'feelslike' : 27,
            'description' : 'clouds',
            'wind_speed': 10,
            'wind_direction': 'NE'
        },
        'forecast_9h': {
            'time': time_9h.strftime('%H:%M'),
            'temp': 16,
            'feelslike' : 27,
            'description' : 'clouds',
            'wind_speed': 8.7,
            'wind_direction': 'E'
        }
    }
    
    return render(request, 'landing/landing_page.html', context)

