from django.shortcuts import render
from _lib.Config import config
from datetime import datetime, timedelta
import os
from .Openweather import Openweather

def landing_page(request):
    """
    View to display weather dashboard
    Pass weather data from your weather API to the template
    """
    url = config.get_url_forecast()
    openweather = Openweather(url)
    openweather.parse_data()
    openweather.save_parsed_data_to_json_file(config.get_path_prot())
    
    # Calculate times for forecasts
    now = datetime.now()
    time_3h = now + timedelta(hours=3)
    time_6h = now + timedelta(hours=6)
    time_9h = now + timedelta(hours=9)
    

    if openweather.get_parsed_data_valid():
        city = openweather.get_city()
        sunrise = openweather.get_sunrise()
        sunset = openweather.get_sunset()
        temp_now = openweather.get_temperature('now')
    else:
        city = 'Waidhaus'
        sunrise = '06:00:00'
        sunset = '18:00:00'
        temp_now = 22

    # Example weather data structure
    # Replace this with actual data from your weather API
    context = {
        'city' : city,
        'sunrise': sunrise,
        'sunset' : sunset,
        'current': {
            'time': 'Now',
            'temp': temp_now,
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

