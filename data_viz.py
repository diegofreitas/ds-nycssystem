__author__ = 'diego.freitas'
from pandas import *
from datetime import datetime
from ggplot import *

def get_day_week(date):
    return datetime.strftime(datetime.strptime(date,'%Y-%m-%d').date(),'%a')

def plot_weather_data(turnstile_weather):
    '''
    plot_weather_data is passed a dataframe called turnstile_weather.
    Use turnstile_weather along with ggplot to make a data visualization
    focused on the MTA and weather data we used in Project 3.

    You should feel free to implement something that we discussed in class
    (e.g., scatterplots, line plots, or histograms) or attempt to implement
    something more advanced if you'd like.

    Here are some suggestions for things to investigate and illustrate:
     * Ridership by time-of-day or day-of-week
     * How ridership varies by subway station
     * Which stations have more exits or entries at different times of day

    If you'd like to learn more about ggplot and its capabilities, take
    a look at the documentation at:
    https://pypi.python.org/pypi/ggplot/

    You can check out the link
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv
    to see all the columns and data points included in the turnstile_weather
    dataframe.

    However, due to the limitation of our Amazon EC2 server, we will give you only
    about 1/3 of the actual data in the turnstile_weather dataframe.
    '''

    turnstile_weather['day_week'] = turnstile_weather.DATEn.apply(get_day_week)
    grouped_dataframe = turnstile_weather[['day_week','ENTRIESn_hourly']]
    grouped_dataframe = grouped_dataframe.groupby('day_week',as_index=False).mean()
    plot = ggplot(grouped_dataframe, aes(x='day_week', y='ENTRIESn_hourly')) + \
            geom_bar(aes(x='day_week',weight='ENTRIESn_hourly'), fill='blue', stat="bar")+ \
            xlab('Day of Week') + ylab('Mean Entries Hourly')
    return plot


def plot_weather_data2(df):
    '''
    plot_weather_data is passed a dataframe called turnstile_weather.
    Use turnstile_weather along with ggplot to make another data visualization
    focused on the MTA and weather data we used in Project 3.

    Make a type of visualization different than what you did in the previous exercise.
    Try to use the data in a different way (e.g., if you made a lineplot concerning
    ridership and time of day in exercise #1, maybe look at weather and try to make a
    histogram in this exercise). Or try to use multiple encodings in your graph if
    you didn't in the previous exercise.

    You should feel free to implement something that we discussed in class
    (e.g., scatterplots, line plots, or histograms) or attempt to implement
    something more advanced if you'd like.

    Here are some suggestions for things to investigate and illustrate:
     * Ridership by time-of-day or day-of-week
     * How ridership varies by subway station
     * Which stations have more exits or entries at different times of day

    If you'd like to learn more about ggplot and its capabilities, take
    a look at the documentation at:
    https://pypi.python.org/pypi/ggplot/

    You can check out the link
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv
    to see all the columns and data points included in the turnstile_weather
    dataframe.

    However, due to the limitation of our Amazon EC2 server, we will give you only
    about 1/3 of the actual data in the turnstile_weather dataframe.
    '''
    df = df[['UNIT','Hour','ENTRIESn_hourly']]
    df = df.groupby(['UNIT','Hour'], as_index=False)['ENTRIESn_hourly'].mean()
    #df = df[(df.ENTRIESn_hourly < 5000)]
    #df = df[(df.ENTRIESn_hourly  5000)]
    plot = ggplot(df, aes(x='Hour',y='ENTRIESn_hourly',colour='UNIT', group='UNIT')) + geom_line() + geom_point()

    return plot

print(plot_weather_data2(pandas.read_csv("turnstile_data_master_with_weather_part.csv")))