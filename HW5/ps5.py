# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: 
# Collaborators (discussion):
# Time:

import pylab
import re
import numpy as np
from matplotlib import pyplot as plt
import math
# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return np.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    curves = []
    for deg in degs:
        curves.append(np.polyfit(x, y, deg))
    return curves


def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    num = []
    denom = []
    mean = np.mean(y)
    for i in range(len(y)):
        numvalue = (y[i] - estimated[i])**2
        denomvalue = (y[i] - mean)**2
        num.append(numvalue)
        denom.append(denomvalue)
    numsum = np.sum(num)
    denomsum = np.sum(denom)
    r2 = (1 - (numsum / denomsum))
    return r2

def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    x = np.array(x)
    y = np.array(y)
    yEstimates = []
    r2s = []
    serrs = 0
    i=0
    j=0
    fig, axs = plt.subplots(math.ceil(math.sqrt(len(models))), math.ceil(math.sqrt(len(models))))
    for model in models:
        yEstimates.append([])
        r2s.append([])
        yEstimates[i] = np.polyval(model, x)
        r2s[i] = r_squared(y, yEstimates[i])
        if i == 0 and j == 0:
            serrs = se_over_slope(x, y, yEstimates[i], model)
        axs[i, j].scatter(x, y, c='blue', s=0.2)
        axs[i, j].plot(x, yEstimates[i], c='green')
        axs[i, j].set_title(f'{r2s[i]}\nDegree: {len(model) - 1}')
        i+=1
        if i % (math.ceil(math.sqrt(len(models)))) == 0:
            i=0
            j+=1
    plt.show()




def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    avgtemps = []
    for year in years:
        yeartemps = []
        for city in multi_cities:
            citytemps = climate.get_yearly_temp(city, year)
            yeartemps.append(np.mean(citytemps))
        avgtemps.append(np.mean(yeartemps))
    return avgtemps
def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    movingAvg = []
    for i in range(len(y)):
        if i >= window_length - 1:
            cumsum = float(np.sum(y[i-window_length+1:i+1]))
            movingAvg.append(float(cumsum/float(window_length)))
        else:
            cumsum = float(np.sum(y[:i+1]))
            movingAvg.append(cumsum/float(i+1))
    return np.array(movingAvg)




def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    num = 0.0
    for i in range(len(y)):
        num += (y[i] - estimated[i])**2
    return math.sqrt(num/len(y))


def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    stds = []
    for year in years:
        daily_temp_norm = np.zeros(365)
        daily_temp_leap = np.zeros(366)
        for city in multi_cities:
            if len(climate.get_yearly_temp(city, year)) == 365:
                daily_temp_norm += climate.get_yearly_temp(city, year)
            else:
                daily_temp_leap += climate.get_yearly_temp(city, year)
        if sum(daily_temp_norm) > sum(daily_temp_leap):
            daily_temp = daily_temp_norm
        else:
            daily_temp = daily_temp_leap
        daily_temp = daily_temp / len(multi_cities)
        mean = np.mean(daily_temp)
        varience = 0.0
        for temp in list(daily_temp):
            varience += (temp - mean)**2
        stds.append(math.sqrt(varience/len(daily_temp)))
    return np.array(stds)





def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    x = np.array(x)
    y = np.array(y)
    yEstimates = []
    rmses = []
    serrs = 0
    i = 0
    j = 0
    fig, axs = plt.subplots(math.ceil(math.sqrt(len(models))), math.ceil(math.sqrt(len(models))))
    for model in models:
        yEstimates.append([])
        rmses.append([])
        yEstimates[i] = np.polyval(model, x)
        rmses[i] = rmse(y, yEstimates[i])
        axs[i, j].scatter(x, y, c='blue', s=0.2)
        axs[i, j].plot(x, yEstimates[i], c='green')
        axs[i, j].set_title(f'{rmses[i]}\nDegree: {len(model) - 1}')
        i += 1
        if i % (math.ceil(math.sqrt(len(models)))) == 0:
            i = 0
            j += 1
    plt.show()

