__author__ = 'diego.freitas'
from pandas import *
from datetime import datetime
from ggplot import *
from linear_regression import *

def get_day_week(date):
    return datetime.strftime(datetime.strptime(date,'%Y-%m-%d').date(),'%a')

def plot_weather_data(turnstile_weather):
    turnstile_weather = turnstile_weather[(turnstile_weather.rain == 1)]
    turnstile_weather['day_week'] = turnstile_weather.DATEn.apply(get_day_week)
    grouped_dataframe = turnstile_weather[['day_week','ENTRIESn_hourly']]
    grouped_dataframe = grouped_dataframe.groupby('day_week',as_index=False).mean()
    plot = ggplot(grouped_dataframe, aes(x='day_week', y='ENTRIESn_hourly')) + \
            geom_bar(aes(x='day_week',weight='ENTRIESn_hourly'), fill='blue', stat="bar")+ \
            xlab('Day of Week') + ylab('Mean Entries Hourly')
    return plot


def plot_entriesmean_by_hour(turnstile_weather):
    turnstile_weather = turnstile_weather[(turnstile_weather.rain == 0)]
    grouped_dataframe = turnstile_weather[['Hour','ENTRIESn_hourly']]
    grouped_dataframe = grouped_dataframe.groupby('Hour',as_index=False)['ENTRIESn_hourly'].mean()
    plot = ggplot(grouped_dataframe, aes(x='Hour', y='ENTRIESn_hourly')) + \
            geom_bar(aes(x='Hour',weight='ENTRIESn_hourly'), fill='blue', stat="bar")+ \
            xlab('Hour') + ylab('Mean Entries Hourly')
    return plot

def plot_weather_data2(df):

    df = df[(df.UNIT == 'R552')]
    df = df[['UNIT','Hour','ENTRIESn_hourly']]
    df = df.groupby(['UNIT','Hour'], as_index=False)['ENTRIESn_hourly'].mean()
    #df = df[(df.ENTRIESn_hourly < 5000)]
    #df = df[(df.ENTRIESn_hourly  5000)]
    plot = ggplot(df, aes(x='Hour',y='ENTRIESn_hourly',colour='UNIT', group='UNIT')) + geom_line() + geom_point()

    return plot
