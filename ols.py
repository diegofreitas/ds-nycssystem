__author__ = 'diego'


import pandas
from pandas import DataFrame
import statsmodels.formula.api as smf
from functions import *

def predictions(weather_turnstile):
    features = weather_turnstile[['UNIT','rain', 'Hour', 'meantempi', 'weekday']]
    model = smf.ols('ENTRIESn_hourly ~ UNIT * Hour + rain + meantempi + weekday', data=weather_turnstile).fit()
    print model.summary()
    return model.predict(features)

weather_turnstile = pandas.read_csv('turnstile_data_master_with_weather.csv')
weather_turnstile['weekday'] = weather_turnstile.DATEn.apply(get_day_week)

weather_turnstile_norm = DataFrame()

weather_turnstile_norm['UNIT'] = weather_turnstile.UNIT
weather_turnstile_norm['rain'] = weather_turnstile.rain
weather_turnstile_norm['Hour'] = normalize(weather_turnstile.Hour)
weather_turnstile_norm['meantempi'] = normalize(weather_turnstile.meantempi)
weather_turnstile_norm['weekday'] = normalize(weather_turnstile.weekday)
weather_turnstile_norm['ENTRIESn_hourly'] = normalize(weather_turnstile.ENTRIESn_hourly)

predictions = predictions(weather_turnstile_norm)
print compute_r_squared(weather_turnstile_norm.ENTRIESn_hourly, predictions)