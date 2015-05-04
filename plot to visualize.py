# -*- coding: utf-8 -*-

from pandas import *
from ggplot import *
import datetime

def plot_weather_data(tw):
    '''
    You are passed in a dataframe called turnstile_weather. 
    Use turnstile_weather along with ggplot to make a data visualization
    focused on the MTA and weather data we used in assignment #3.  
    You should feel free to implement something that we discussed in class 
    (e.g., scatterplots, line plots, or histograms) or attempt to implement
    something more advanced if you'd like.  

    Here are some suggestions for things to investigate and illustrate:
     * Ridership by time of day or day of week
     * How ridership varies based on Subway station
     * Which stations have more exits or entries at different times of day
       (You can use UNIT as a proxy for subway station.)

    If you'd like to learn more about ggplot and its capabilities, take
    a look at the documentation at:
    https://pypi.python.org/pypi/ggplot/
     
    You can check out:
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv
     
    To see all the columns and data points included in the turnstile_weather 
    dataframe. 
     
    However, due to the limitation of our Amazon EC2 server, we are giving you a random
    subset, about 1/3 of the actual data in the turnstile_weather dataframe.
    '''
    #pandas.options.mode.chained_assignment = None
    #pandas.set_option('display.max_rows', 10)
    
    #minDate = datetime.strptime("1900-01-01", '%Y-%m-%d')
    #maxDate = datetime.strptime("1900-12-31", '%Y-%m-%d')
    #tw['Time'] = to_datetime(tw['TIMEn'], format = '%H:%M:%S')
    
    #print minDate, maxDate
    #print tw['Time']


    #plot = ggplot(tw, aes(x = 'Hour', y = 'inOutDiff', color = 'UNIT'))
    tw['hour'] = tw['TIMEn'].apply(lambda x: datetime.datetime.strptime(x, '%H:%M:%S').strftime('%H'))
    plt1 = ggplot(tw, aes(x = 'hour', y = 'ENTRIESn_hourly', xmax = 23, fill='rain'))
    plt1 += geom_bar(aes(x = 'hour', weight = 'ENTRIESn_hourly'))
    plt1 += ggtitle('Number of entries by hour')
    plt1 += xlab('hour') + ylab('Entries')

    #tw["DATEn"] = pandas.to_datetime(tw["DATEn"])
    #tw['weekDays'] = tw['DATEn'].apply(lambda x: x.weekday())
    tw['weekDays'] = \
        tw['DATEn'].apply(lambda x: \
        datetime.datetime.strptime(x, '%Y-%m-%d').strftime('%w-%A'))
    
    plt2 = ggplot(tw, \
        aes(x = 'weekDays', y = 'ENTRIESn_hourly', fill= 'rain'))
    plt2 += geom_bar(aes(x = 'weekDays', weight = 'ENTRIESn_hourly'))
    plt2 += ggtitle('Number of entries by day')
    plt2 += xlab('Day of the week') + ylab('Entries')

    '''
    tw['hour'] = tw['TIMEn'].apply(lambda x: datetime.datetime.strptime(x, '%H:%M:%S').strftime('%H'))
    plt1 = ggplot(tw, aes(x = 'hour', y = 'precipi', xmax = 23, fill='rain'))
    plt1 += geom_bar(aes(x = 'hour', weight = 'precipi'))
    plt1 += ggtitle('Number of entries by hour')
    plt1 += xlab('hour') + ylab('Entries')

    #tw["DATEn"] = pandas.to_datetime(tw["DATEn"])
    #tw['weekDays'] = tw['DATEn'].apply(lambda x: x.weekday())
    tw['weekDays'] = \
        tw['DATEn'].apply(lambda x: \
        datetime.datetime.strptime(x, '%Y-%m-%d').strftime('%w-%A'))
    
    plt2 = ggplot(tw, \
        aes(x = 'weekDays', y = 'rain', fill = 'rain'))
    plt2 += geom_bar(aes(x = 'weekDays', weight = 'rain'))
    plt2 += ggtitle('Number of entries by day')
    plt2 += xlab('Day of the week') + ylab('Entries')
    '''

    plt3 = ggplot(tw, aes(x = 'ENTRIESn_hourly', y = 'ENTRIESn_hourly'))
    #plt3 += geom_bar(aes(x = 'ENTRIESn_hourly', weight = 'ENTRIESn_hourly'))
    plt3 += geom_bar(aes(x = 'ENTRIESn_hourly', y = 'ENTRIESn_hourly'))
    plt3 += ggtitle('Histogram of Entries')
    plt3 += xlab('Entries') + ylab('Frequency')

    return plt1, plt2, plt3

pandas.set_option("display.max_rows",1)
dataPath = 'C:\\Users\\101003537\\Documents\\ITO\\Trainings\\Data Analyst\\turnstile_data_master_with_weather.csv'
dataframe = pandas.read_csv(dataPath)
plt1, plt2, plt3 = plot_weather_data(dataframe)
print plt1, plt2
