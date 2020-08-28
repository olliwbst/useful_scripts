#!python3

import sys
import json
import requests
from datetime import datetime
import pandas as pd
from exceptions import OWMApiResponseError


class WeatherGrabber:
    def __init__(self):
        # get OWM-key from textfile
        f = open(f'OWMKey.txt', 'r')
        self.OWM_key = f.read()
        f.close()
        self.city_name = None

        # get input parameters, if city was specified automatically export data-csv
        if len(sys.argv) > 1:
            self.city_name = ' '.join(sys.argv[1:])
            self.format_data(self.city_name, save=True)

    def get_weather_data(self, city_name):
        # make API-request with wanted parameters
        url = f'https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={self.OWM_key}&units=metric'
        response = requests.get(url)
        data = json.loads(response.text)
        response_code = int(data['cod'])

        if response_code == 200:
            return data
        else:
            raise OWMApiResponseError('Something went wrong with the weather request, '
                                      'OWM probably could not find your city!')

    def format_data(self, city_name, save: bool=False):
        data = self.get_weather_data(city_name)

        timezone = (data['city']['timezone']) - 7200  # -7200 because the api returns localized timestamps, we want UTC
        location = data['city']['name'] + ', ' + data['city']['country']
        sunrise = datetime.fromtimestamp(data['city']['sunrise'] + (timezone))
        sunset = datetime.fromtimestamp(data['city']['sunset'] + (timezone))

        # initializing dataframe
        df = pd.DataFrame(data['list'])

        # initializing temporary lists to format the data in a more practical shape further down
        temp = []
        feels_like = []
        temp_min = []
        temp_max = []
        pressure = []
        sea_level = []
        ground_level = []
        humidity = []

        weather_main = []
        weather_description = []

        wind_speed = []
        wind_deg = []

        for i in range(len(df)):
            # format timestamps to city's local time
            df.loc[i, 'dt'] = str(datetime.fromtimestamp(df['dt'][i] + (timezone))).replace(' ', '_')
            # convert clouds from dict to int
            df.loc[i, 'clouds'] = df['clouds'][i]['all']
            # fill missing rain values and replace dict with floats
            df['rain'] = df['rain'].fillna(0.0)
            if df.loc[i, 'rain'] != 0.0:
                df.loc[i, 'rain'] = df['rain'][i]['3h']

            # fill the temporary lists with the data from the nested structures of the api's response
            temp.append(df['main'][i]['temp'])
            feels_like.append(df['main'][i]['feels_like'])
            temp_min.append(df['main'][i]['temp_min'])
            temp_max.append(df['main'][i]['temp_max'])
            pressure.append(df['main'][i]['pressure'])
            sea_level.append(df['main'][i]['sea_level'])
            ground_level.append(df['main'][i]['grnd_level'])
            humidity.append(df['main'][i]['humidity'])
            weather_main.append(df['weather'][i][0]['main'])
            weather_description.append(df['weather'][i][0]['description'])
            wind_speed.append(df['wind'][i]['speed'])
            wind_deg.append(df['wind'][i]['deg'])

        # add the temporary lists as unique rows to the dataframe
        df['temp'] = temp
        df['feels_like'] = feels_like
        df['temp_min'] = temp_min
        df['temp_max'] = temp_max
        df['pressure'] = pressure
        df['sea_level'] = sea_level
        df['ground_level'] = ground_level
        df['humidity'] = humidity
        df['weather_main'] = weather_main
        df['weather_description'] = weather_description
        df['wind_speed'] = wind_speed
        df['wind_deg'] = wind_deg

        # drop nested rows and those containing irrelevant data
        df = df.drop(['dt_txt', 'sys', 'main', 'weather', 'wind', 'pop'], axis=1)

        # add new row with easy to interpret wind directions (generated from wind_deg)
        wind_directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW",
                           "W", "WNW", "NW", "NNW", "N"]
        df.append(pd.Series(name='wind_direction'))

        for i in range(len(df)):
            df.loc[i, 'wind_direction'] = wind_directions[int(round(df['wind_deg'][i] / 22.5))]

        if save:
            df.to_csv(f'{city_name}_weatherdata.csv')

        return df, location, sunrise, sunset


weather = WeatherGrabber()
