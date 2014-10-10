__author__ = 'diego.freitas'

import numpy as np
import scipy
import scipy.stats
import pandas

def mann_whitney_plus_means(turnstile_weather):
    entries_with_rain = turnstile_weather[turnstile_weather.rain == 1].ENTRIESn_hourly
    entries_without_rain = turnstile_weather[turnstile_weather.rain == 0].ENTRIESn_hourly
    with_rain_mean = np.mean(entries_with_rain)
    without_rain_mean = np.mean(entries_without_rain)
    U, p = scipy.stats.mannwhitneyu(entries_with_rain,entries_without_rain)
    return with_rain_mean, without_rain_mean, U, p

print(mann_whitney_plus_means(pandas.read_csv('turnstile_data_master_with_weather.csv')));