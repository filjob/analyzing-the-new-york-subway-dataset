# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 15:34:29 2015

@author: 101003537
"""

import numpy as np
import pandas
import matplotlib.pyplot as plt

def entries_histogram(tw):
    '''
    Before we perform any analysis, it might be useful to take a
    look at the data we're hoping to analyze. More specifically, let's 
    examine the hourly entries in our NYC subway data and determine what
    distribution the data follows. This data is stored in a dataframe
    called turnstile_weather under the ['ENTRIESn_hourly'] column.
    
    Let's plot two histograms on the same axes to show hourly
    entries when raining vs. when not raining. Here's an example on how
    to plot histograms with pandas and matplotlib:
    turnstile_weather['column_to_graph'].hist()
    
    Your histograph may look similar to bar graph in the instructor notes below.
    
    You can read a bit about using matplotlib and pandas to plot histograms here:
    http://pandas.pydata.org/pandas-docs/stable/visualization.html#histograms
    
    You can see the information contained within the turnstile weather data here:
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv
    '''
    
    plt.figure()
    plt.xlim(xmax = 6000)
    plt.xlabel('Hourly entries')
    
    plt.title('Histogram of hourly entries (bins = 200)')
    #tw['ENTRIESn_hourly'].plot(kind='hist', bins = 200, legend=True, \
    #                            label = 'All data')
    tw['ENTRIESn_hourly'][tw['rain']  == 0].plot(kind='hist', alpha=0.75, \
        bins = 200, legend=True, label = 'No rain') 
        
    tw['ENTRIESn_hourly'][tw['rain']  == 1].plot(kind='hist', alpha=0.75, \
        bins = 200, legend=True, label = 'Rain') # your code here to plot a historgram for hourly entries when it is raining
    plt.ylabel('Frequency')
    
    return plt
    
pandas.set_option("display.max_rows",1)
dataPath = 'C:\\Users\\101003537\\Documents\\ITO\\Trainings\\Data Analyst\\turnstile_data_master_with_weather.csv'
dataframe = pandas.read_csv(dataPath)
plt = entries_histogram(dataframe)
print plt