__author__ = 'diego'


import pandas
import statsmodels.formula.api as smf
from functions import *

def predictions(weather_turnstile):
    features = weather_turnstile[['UNIT','rain', 'Hour', 'meantempi', 'weekday']]
    model = smf.ols('ENTRIESn_hourly ~ UNIT * Hour + rain + meantempi + weekday', data=weather_turnstile).fit()
    print model.summary()
    return model.predict(features)

weather_turnstile = pandas.read_csv('turnstile_data_master_with_weather.csv')
#weather_turnstile['weekday'] = weather_turnstile.DATEn.apply(get_day_week)
#weather_turnstile['hour_ampm'] = weather_turnstile.Hour.apply(convert_hour)
#weather_turnstile['hour_type'] = weather_turnstile.Hour.apply(ampm_hour)

predictions = predictions(weather_turnstile)
print compute_r_squared(weather_turnstile.ENTRIESn_hourly, predictions)