# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import scipy
import statsmodels.api as sm
from ggplot import *
import datetime
from scipy.stats import probplot, norm, t
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

"""
In this optional exercise, you should complete the function called 
predictions(turnstile_weather). This function takes in our pandas 
turnstile weather dataframe, and returns a set of predicted ridership values,
based on the other information in the dataframe.  

In exercise 3.5 we used Gradient Descent in order to compute the coefficients
theta used for the ridership prediction. Here you should attempt to implement 
another way of computing the coeffcients theta. You may also try using a reference implementation such as: 
http://statsmodels.sourceforge.net/devel/generated/statsmodels.regression.linear_model.OLS.html

One of the advantages of the statsmodels implementation is that it gives you
easy access to the values of the coefficients theta. This can help you infer relationships 
between variables in the dataset.

You may also experiment with polynomial terms as part of the input variables.  

The following links might be useful: 
http://en.wikipedia.org/wiki/Ordinary_least_squares
http://en.wikipedia.org/w/index.php?title=Linear_least_squares_(mathematics)
http://en.wikipedia.org/wiki/Polynomial_regression

This is your playground. Go wild!

How does your choice of linear regression compare to linear regression
with gradient descent computed in Exercise 3.5?

You can look at the information contained in the turnstile_weather dataframe below:
https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv

Note: due to the memory and CPU limitation of our amazon EC2 instance, we will
give you a random subset (~10%) of the data contained in turnstile_data_master_with_weather.csv

If you receive a "server has encountered an error" message, that means you are hitting 
the 30 second limit that's placed on running your program. See if you can optimize your code so it
runs faster.
"""
def workingday(day):
    workingDay = 0
    if day < 5:
        workingDay = 1
        
    return workingDay

def predictions(weather_turnstile):
    wt = weather_turnstile
    #wt['sqPrecipi'] = np.square(wt[['precipi']])
    #wt['sqMintempi'] = np.square(wt[['mintempi']])
    wt["DATEn"] = pd.to_datetime(wt["DATEn"])
    wt['weekDays'] = wt['DATEn'].apply(lambda x: x.weekday())
    #wt['weekdays'] = wt['DATEn'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').strftime('%w'))
    #wt['workingDays'] = wt['weekDays'].apply(lambda x: workingday(x))
    features = sm.add_constant(wt[['rain', 'fog', 'meantempi']])

    dummy_units = pd.get_dummies(wt['UNIT'], prefix='unit')
    features = features.join(dummy_units)
    

    dummy_units = pd.get_dummies(wt['weekDays'], prefix='weekday')
    features = features.join(dummy_units)
    
    dummy_units = pd.get_dummies(wt['Hour'], prefix='hour')
    features = features.join(dummy_units)

    
    model = sm.OLS(wt['ENTRIESn_hourly'], features)
    results = model.fit()
    print(results.summary(xname = ['rain', 'fog', 'meantempi','weekday_0','weekday_1','weekday_2','weekday_3','weekday_4','weekday_5','weekday_6']))


    predictions = model.predict(results.params, features)
    
    return predictions

def compute_r_squared(data, predictions):
    '''
    In exercise 5, we calculated the R^2 value for you. But why don't you try and
    and calculate the R^2 value yourself.
    
    Given a list of original data points, and also a list of predicted data points,
    write a function that will compute and return the coefficient of determination (R^2)
    for this data.  numpy.mean() and numpy.sum() might both be useful here, but
    not necessary.

    Documentation about numpy.mean() and numpy.sum() below:
    http://docs.scipy.org/doc/numpy/reference/generated/numpy.mean.html
    http://docs.scipy.org/doc/numpy/reference/generated/numpy.sum.html
    '''     
    
    data = np.array(data)
    predictions = np.array(predictions)
    r_squared = 1 - (np.square(data - predictions).sum() / np.square(data - np.mean(data)).sum())
    print 'r^2 = {0}'.format(r_squared)

def plot_residuals(turnstile_weather, predictions):
    '''
    Using the same methods that we used to plot a histogram of entries
    per hour for our data, why don't you make a histogram of the residuals
    (that is, the difference between the original hourly entry data and the predicted values).
    Try different binwidths for your histogram.

    Based on this residual histogram, do you have any insight into how our model
    performed?  Reading a bit on this webpage might be useful:

    http://www.itl.nist.gov/div898/handbook/pri/section2/pri24.htm
    '''
    
    #fig = plt.figure()
    #ax1 = plt.subplot(211)
    plt.xlim(xmin = -5000, xmax = 5000)
    plt.xlabel('Residuals')
    plt.title('Histogram of Residuals')
    
    residuals = (turnstile_weather['ENTRIESn_hourly'] - predictions)
    mu = np.mean(residuals)
    sigma = np.std(residuals)
    
    residuals.hist(bins = 500, normed = 0)
    #range = np.arange(-10000, 10000, 500)
    #plt.plot(range, mlab.normpdf(range, mu, sigma))
    plt.ylabel('Frequency')

    #ax2 = plt.subplot(212)
    #plt.ylim(ymin = -5000, ymax = 5000)
    #res = probplot(residuals, plot=plt)
    #plt.xlabel('Quantiles')
    #plt.ylabel('Ordered Residuals')
    
   
    #prbplt = sm.ProbPlot(residuals, dist = t, fit = True, loc = mu, scale = sigma)
    #prbplt.qqplot()
    #prbplt.probplot(line = 'r')
    #prbplt.ppplot()
    
    plt.show()
    
    return plt

pd.set_option("display.max_rows",1)
dataPath = 'C:\\Users\\101003537\\Documents\\ITO\\Trainings\\Data Analyst\\turnstile_data_master_with_weather.csv'
dataframe = pd.read_csv(dataPath)
pred = predictions(dataframe)
compute_r_squared(dataframe['ENTRIESn_hourly'], pred)

plot_residuals(dataframe, pred)