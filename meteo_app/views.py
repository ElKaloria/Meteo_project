from django.shortcuts import render, reverse
from .forms import MeteoForm
import requests_cache
import openmeteo_requests
from retry_requests import retry
import pandas as pd
import requests


# Create your views here.


def meteo_request_view(request):
    if request.method == "POST":
        form = MeteoForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
            retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
            openmeteo = openmeteo_requests.Client(session=retry_session)
            geocode_city = openmeteo.weather_api('https://geocoding-api.open-meteo.com/v1/search',
                                                 params={'name': city, 'count': 1, 'language': 'ru', 'format': 'json'})
            weather_responses = openmeteo.weather_api("https://api.open-meteo.com/v1/forecast",
                                                      {"latitude": geocode_city[0].Latitude(),
                                                       "longitude": geocode_city[0].Longitude(),
                                                       "current": "temperature_2m",
                                                       "hourly": "temperature_2m"})
            response = weather_responses[0]
            current = response.Current()
            current_temperature_2m = current.Variables(0).Value()

            # Process hourly data. The order of variables needs to be the same as requested.
            hourly = response.Hourly()
            hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

            hourly_data = {"date": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left"
            ), "temperature_2m": hourly_temperature_2m}

            hourly_dataframe = pd.DataFrame(data=hourly_data).to_html(classes="table table-striped")
            return render(request, 'meteo_app/weather.html', {'city': city, 'curent_time': current.Time(),
                                                              'temperature': current_temperature_2m,
                                                              'hourly': hourly_dataframe})
    else:
        form = MeteoForm()
    return render(request, 'meteo_app/city_form.html', {'form': form})
