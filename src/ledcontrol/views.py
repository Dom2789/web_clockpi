from django.shortcuts import render
from . import led_logger
import json
from _lib.mqtt import mqtt_publish
from django.conf import settings

def led_control(request):
    if request.method == 'POST':
        red = request.POST.get('red')
        green = request.POST.get('green')
        blue = request.POST.get('blue')
        option = request.POST.get('option')
        
        # Process your data here
        led_logger.info(f"RGB: {red}, {green}, {blue} Selected option: {option}")
        
        # Create dictonary and publish with MQTT as JSON-string
        led = {"brightness":50, "mode":option, "red":int(red), "green":int(green), "blue":int(blue)}
        _ip = getattr(settings, "BROKER_IP")
        _topic = getattr(settings, "TOPIC_PUBLISH")
        mqtt_publish(_ip, _topic, json.dumps(led), led_logger)
        # JSON-representation
        """
        {
        "brightness": 200,
        "mode": "wipe",
        "red": 123, 
        "green": 456, 
        "blue": 789
        }
        """

        """
        {"brightness": 200, "mode": "wipe", "red": 123, "green": 456, "blue": 789}
        """

    # Define your dropdown options
    options = [
        {'value': 'wipe', 'label': 'single color'},
        {'value': 'chase', 'label': 'theater chase'},
        {'value': 'rainbow', 'label': 'rainbow wheel'},
        {'value': 'temperature', 'label': 'temperature gradient'},
    ]
    
    return render(request, 'ledcontrol/led_control.html', {'options': options})