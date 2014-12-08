__author__ = 'diego'


import pandas
import statsmodels.formula.api as smf
from functions import *

def predictions(weather_turnstile):
    weather_turnstile['weekday'] = weather_turnstile.DATEn.apply(get_day_week)
    features = weather_turnstile[['UNIT','rain', 'Hour', 'meantempi', 'weekday']]
    model = smf.ols('ENTRIESn_hourly ~ UNIT + rain + Hour + meantempi + weekday', data=weather_turnstile).fit()
    print model.summary()
    return model.predict(features)

data = pandas.read_csv('turnstile_data_master_with_weather.csv')

predictions = predictions(data)
print compute_r_squared(data.ENTRIESn_hourly, predictions)