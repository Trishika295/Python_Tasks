
# Task 28 — Atmos Weather Intelligence

A professional, real-time weather dashboard built using Python and Streamlit.

## Features

- Search for cities and view their state/province and country.
- Persistent history of up to 20 recently searched locations.
- Current temperature and feels-like temperature.
- Humidity, wind speed, precipitation, and atmospheric pressure.
- Sunrise, sunset, UV index, and daily weather conditions.
- Seven-day weather forecast.
- Hourly temperature chart and detailed weather table.
- Automatic and manual weather refresh.
- Clean dashboard without a sidebar.
- Live weather information from Open-Meteo.

## Technologies

- Python
- Streamlit
- Requests
- Pandas
- Open-Meteo Geocoding API
- Open-Meteo Forecast API

## Installation

```bash
python -m pip install -r requirements.txt
```

## Run the application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in the terminal, usually:

http://localhost:8501

## API Configuration

This project uses Open-Meteo's public geocoding and forecast APIs.
No API key is required for this version.

## Search History

The application automatically creates `search_history.json`
to store recent searches locally.

## Disclaimer

Weather information is supplied by Open-Meteo. Availability and
update frequency depend on the upstream weather data service.
