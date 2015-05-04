# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 13:10:01 2015

@author: 101003537
"""

import numpy as np
import pandas
from ggplot import *
import datetime
from scipy.stats import probplot, norm
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab

"""
In this question, you need to:
1) implement the compute_cost() and gradient_descent() procedures
2) Select features (in the predictions procedure) and make predictions.

"""

def normalize_features(df):
    """
    Normalize the features in the data set.
    """
    mu = df.mean()
    sigma = df.std()
    
    if (sigma == 0).any():
        raise Exception("One or more features had the same value for all samples, and thus could " + \
                         "not be normalized. Please do not include features with only a single value " + \
                         "in your model.")
    df_normalized = (df - df.mean()) / df.std()

    return df_normalized, mu, sigma

def compute_cost(features, values, theta):
    """
    Compute the cost function given a set of features / values, 
    and the values for our thetas.
    
    This can be the same code as the compute_cost function in the lesson #3 exercises,
    but feel free to implement your own.
    """
    m = len(values)
    predValues = np.dot(features, theta)
    cost = np.square(predValues - values).sum() / (2 * m)

    return cost

def gradient_descent(features, values, theta, alpha, num_iterations):
    """
    Perform gradient descent given a data set with an arbitrary number of features.
    
    This can be the same gradient descent code as in the lesson #3 exercises,
    but feel free to implement your own.
    """
    
    m = len(values)
    cost_history = []

    for i in range(num_iterations):
        predValues = np.dot(features, theta)
        theta = theta - ((alpha / m) * np.dot((predValues - values),features))
        
    cost_history = compute_cost(features, values, theta)
    
    return theta, pandas.Series(cost_history)

def predictions(dataframe):
    '''
    The NYC turnstile data is stored in a pandas dataframe called weather_turnstile.
    Using the information stored in the dataframe, let's predict the ridership of
    the NYC subway using linear regression with gradient descent.
    
    You can download the complete turnstile weather dataframe here:
    https://www.dropbox.com/s/meyki2wl9xfa7yk/turnstile_data_master_with_weather.csv    
    
    Your prediction should have a R^2 value of 0.20 or better.
    You need to experiment using various input features contained in the dataframe. 
    We recommend that you don't use the EXITSn_hourly feature as an input to the 
    linear model because we cannot use it as a predictor: we cannot use exits 
    counts as a way to predict entry counts. 
    
    Note: Due to the memory and CPU limitation of our Amazon EC2 instance, we will
    give you a random subet (~15%) of the data contained in 
    turnstile_data_master_with_weather.csv. You are encouraged to experiment with 
    this computer on your own computer, locally. 
    
    
    If you'd like to view a plot of your cost history, uncomment the call to 
    plot_cost_history below. The slowdown from plotting is significant, so if you 
    are timing out, the first thing to do is to comment out the plot command again.
    
    If you receive a "server has encountered an error" message, that means you are 
    hitting the 30-second limit that's placed on running your program. Try using a 
    smaller number for num_iterations if that's the case.
    
    If you are using your own algorithm/models, see if you can optimize your code so 
    that it runs faster.
    '''
    # Select Features (try different features!)
    features = dataframe[['rain', 'fog', 'meantempi']]
    
    # Add UNIT to features using dummy variables

    dummy_units = pandas.get_dummies(dataframe['UNIT'], prefix='unit')
    features = features.join(dummy_units)

    dataframe['weekday'] = dataframe['DATEn'].apply(lambda x: datetime.datetime.strptime(x, '%Y-%m-%d').strftime('%w'))
    dummy_units = pandas.get_dummies(dataframe['weekday'], prefix='weekday')
    features = features.join(dummy_units)
    
    dummy_units = pandas.get_dummies(dataframe['Hour'], prefix='hour')
    features = features.join(dummy_units)

    
    # Values
    values = dataframe['ENTRIESn_hourly']
    m = len(values)

    features, mu, sigma = normalize_features(features)
    features['ones'] = np.ones(m) # Add a column of 1s (y intercept)
    
    # Convert features and values to numpy arrays
    features_array = np.array(features)
    values_array = np.array(values)

    # Set values for alpha, number of iterations.
    alpha = 0.1 # please feel free to change this value
    num_iterations = 75 # please feel free to change this value

    # Initialize theta, perform gradient descent
    theta_gradient_descent = np.zeros(len(features.columns))
    theta_gradient_descent, cost_history = gradient_descent(features_array, 
                                                            values_array, 
                                                            theta_gradient_descent, 
                                                            alpha, 
                                                            num_iterations)
    
    plot = None
    # -------------------------------------------------
    # Uncomment the next line to see your cost history
    # -------------------------------------------------
    #plot = plot_cost_history(alpha, cost_history)
    # 
    # Please note, there is a possibility that plotting
    # this in addition to your calculation will exceed 
    # the 30 second limit on the compute servers.
    print features
    print '{0}'.format(theta_gradient_descent)
    predictions = np.dot(features_array, theta_gradient_descent)
    return predictions, plot


def plot_cost_history(alpha, cost_history):
   """This function is for viewing the plot of your cost history.
   You can run it by uncommenting this

       plot_cost_history(alpha, cost_history) 

   call in predictions.
   
   If you want to run this locally, you should print the return value
   from this function.
   """
   cost_df = pandas.DataFrame({
      'Cost_History': cost_history,
      'Iteration': range(len(cost_history))
   })
   return ggplot(cost_df, aes('Iteration', 'Cost_History')) + \
      geom_point() + ggtitle('Cost History for alpha = %.3f' % alpha )

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
    ax1 = plt.subplot(121)
    plt.xlim(xmin = -5000, xmax = 5000)
    plt.xlabel('Residuals')
    plt.title('Histogram of Residuals (normalised)')
    
    residuals = (turnstile_weather['ENTRIESn_hourly'] - predictions)
    mu = np.mean(residuals)
    sigma = np.std(residuals)
    
    residuals.hist(bins = 150, normed = 1)
    range = np.arange(-5000, 5000, 150)
    plt.plot(range, mlab.normpdf(range, mu, sigma))
    plt.ylabel('Frequency')

    ax2 = plt.subplot(122)
    plt.ylim(ymin = -5000, ymax = 5000)
    res = probplot(residuals, plot=plt)
    plt.xlabel('Normal order statistic medians')
    plt.ylabel('Residuals')
    
    plt.show()
    
    return plt

pandas.set_option("display.max_rows",1)
dataPath = 'C:\\Users\\101003537\\Documents\\ITO\\Trainings\\Data Analyst\\turnstile_data_master_with_weather.csv'
dataframe = pandas.read_csv(dataPath)
pred, plot = predictions(dataframe)
compute_r_squared(dataframe['ENTRIESn_hourly'], pred)

plot_residuals(dataframe, pred)