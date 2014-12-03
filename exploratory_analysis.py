__author__ = 'diego.freitas'

import pandas
import matplotlib.pyplot as plt

def entries_histogram(turnstile_weather):

    plt.figure()
    turnstile_weather[turnstile_weather.rain == 0].ENTRIESn_hourly.hist()
    turnstile_weather[turnstile_weather.rain == 1].ENTRIESn_hourly.hist()
    plt.suptitle("Entries per hour across all stations")
    plt.xlabel("Entries per hour")
    plt.ylabel("Number of occurrences")
    return plt

entries_histogram(pandas.read_csv('turnstile_data_master_with_weather.csv')).show()
