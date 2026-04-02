# web_clockpi

A Django web application designed to run on a Raspberry Pi, providing a weather dashboard, room sensor data visualization, file management, and LED control via MQTT.

## Features

- **Weather Dashboard** — Real-time weather forecast using the OpenWeather API (current + 3h, 6h, 9h forecasts)
- **Sensor Data Viewer** — Upload and browse room temperature log files with paginated line-by-line viewing and selection
- **Data Visualization** — Generate plots for line/word statistics and room temperature, pressure, and humidity over time
- **LED Control** — Web interface to set RGB color and animation mode, published to an IoT device via MQTT
- **Synthwave '84 theme** — Dark neon aesthetic using Bootstrap 5 with custom CSS

## Project Structure

```
src/
├── clockpi/        # Django project config (settings, urls)
├── landing/        # Weather forecast page
├── ledcontrol/     # LED control interface
├── plot/           # Data plotting and JSON API
├── upload/         # File management and line selection
├── _lib/           # Shared utilities (Config, API, MQTT, logging)
└── templates/      # HTML templates and global CSS
site/
└── public/
    ├── static/     # Served static files
    └── media/      # Uploaded/generated media
```

## Apps

### `landing`
Displays a weather forecast card grid. Fetches data from the OpenWeather API and renders current conditions plus three future time slots.

Route: `/`

### `upload`
Manages room sensor log files (`room_*.txt`). Allows selecting a file from the configured directory, viewing it page by page, and selecting specific lines for analysis.

Routes: `/list`, `/select/`, `/refresh/`, `/file/<id>/`, `/selected/<id>/`

### `plot`
Generates matplotlib/seaborn plots from selected file content. Supports standard statistical plots and a custom 3-panel plot for temperature, pressure, and humidity. Plot data is also exposed as a JSON API.

Routes: `/plot`, `/plot/<id>/`, `/custom/<id>/`, `/api/data/<id>/`, `/download/<id>/<type>/`

### `ledcontrol`
Sends RGB values and an animation mode (`wipe`, `chase`, `rainbow`, `temperature`) to an MQTT broker as a JSON payload.

Route: `/led`

## Configuration

The app reads external configuration from `/home/pi/_config/Webserver.txt` at startup. The file uses `key: value` pairs with `//` for comments.

Expected keys include OpenWeather API credentials, file paths (`PROT_FILES`), and MQTT broker connection info.

## Dependencies

| Package | Purpose |
|---|---|
| Django 4.2+ | Web framework |
| matplotlib 3.9+ | Plot generation |
| seaborn 0.13+ | Statistical plots |
| paho-mqtt 2.1+ | MQTT publishing |
| requests 2.32+ | HTTP API calls |

## Running

```bash
cd src
python manage.py migrate
python manage.py runserver
```

> Set `DEBUG = False` and configure `ALLOWED_HOSTS` in `settings.py` for production.