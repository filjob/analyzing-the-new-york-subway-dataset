# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 16:03:46 2015

@author: 101003537
"""

import numpy as np
import scipy
import scipy.stats
import pandas

def mann_whitney_plus_means(tw):
    '''
    This function will consume the turnstile_weather dataframe containing
    our final turnstile weather data. 
    
    You will want to take the means and run the Mann Whitney U-test on the 
    ENTRIESn_hourly column in the turnstile_weather dataframe.
    
    This function should return:
        1) the mean of entries with rain
        2) the mean of entries without rain
        3) the Mann-Whitney U-statistic and p-value comparing the number of entries
           with rain and the number of entries without rain
    
    You should feel free to use scipy's Mann-Whitney implementation, and you 
    might also find it useful to use numpy's mean function.
    
    Here are the functions' documentation:
    http://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html
    http://docs.scipy.org/doc/numpy/reference/generated/numpy.mean.html
    
    You can look at the final turnstile weather data at the link below:
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv
    '''
    tw['weekDays'] = \
        tw['DATEn'].apply(lambda x: \
        datetime.datetime.strptime(x, '%Y-%m-%d').strftime('%w'))

    '''
    wd1 = '1'
    wd2 = '5'
    
    with_rain_mean = np.mean(tw['ENTRIESn_hourly'][(tw.rain == 1) & ((tw.weekDays < wd1) | (tw.weekDays > wd2))])
    without_rain_mean = np.mean(tw['ENTRIESn_hourly'][(tw.rain == 0) & ((tw.weekDays < wd1) | (tw.weekDays > wd2))])
    '''
    
    unit = 'R550'    
    
    with_rain_mean = np.mean(tw['ENTRIESn_hourly'][(tw.UNIT == unit) & (tw.UNIT == unit)])
    without_rain_mean = np.mean(tw['ENTRIESn_hourly'][(tw.rain == 0) & (tw.UNIT == unit)])    
    
    
    (U, p) = scipy.stats.mannwhitneyu(tw['ENTRIESn_hourly'][(tw.rain == 1) & (tw.UNIT == unit)], tw['ENTRIESn_hourly'][(tw.rain == 0) & (tw.UNIT == unit)])
    
    return with_rain_mean, without_rain_mean, U, p # leave this line for the grader

pandas.set_option("display.max_rows",1)
dataPath = 'C:\\Users\\101003537\\Documents\\ITO\\Trainings\\Data Analyst\\turnstile_data_master_with_weather.csv'
dataframe = pandas.read_csv(dataPath)
print mann_whitney_plus_means(dataframe)