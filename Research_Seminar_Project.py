#!/usr/bin/env python
# coding: utf-8

# In[10]:


#Author: Cameron R. Shabahang
#Forecasting based on options market data

#Import packages
import csv
import math
import pandas as pd
import numpy as np
import datetime as dt
#A package to use non-linear least squares to fit a function to data
from scipy.optimize import curve_fit
#Import the API
from pandas_datareader.data import Options
import yfinance as yf

# Raw SVI parametrization
def rawSVI(k,a,b,rho,m,sigma):
    return a+b*(rho*(k-m)+np.sqrt((k-m)**2+sigma**2))

#Function to download option chain data from yfinance
def get_options(ticker):
    from pandas_datareader import data as pdr
    yf.pdr_override() 
    # download dataframe
    jpm = pdr.get_data_yahoo("JPM", start="2020-04-08", end="2020-05-08")
    underlying = (jpm['Adj Close'])
    opt = yf.Ticker("JPM")
    raw = opt.option_chain('2020-07-16')
    print(raw)
get_options('JPM')

def SVI_Fit(dataFile, expiry):
    #Load data from the csv file
    spx = np.recfromcsv(dataFile,skip_header=2)
    #Empty dictionary
    parameterDict = {}

    currentDate = dt.datetime(year = 2020,month = 3,day = 9)
    spot = 2809.87

    for item in expiry:
        imonth = int(item[0]+item[1])
        iday = int(item[3]+item[4])
        iyear = int(item[6]+item[7]+item[8]+item[9])
        dateExp = dt.datetime(year = iyear, month = imonth, day = iday)
        tau = (dateExp - currentDate).days/360
        parameterDict[item] = 'null'
        #Define lists
        strikes = []
        averageVol = []
        totVariance = []
        moneyness = []

        for data in spx:


            if data['expiration_date'].decode('utf-8') == item:

                strikes.append(float(data['strike']))
                iVol = 0.5*int(data['iv']+data['iv_1'])
                #Calculates average vol, total variance, and moneyness
                averageVol.append(iVol)
                totVariance.append(iVol*tau)
                moneyness.append(np.log(float(data['strike']/spot)))


        #Converts the input into an array
        k = np.asarray(strikes)
        w = np.asarray(totVariance)

        #scipy.optimize.curve_fit(f, xdata, ydata, p0=None, sigma=None, absolute_sigma=False, check_finite=True, bounds=(-inf, inf), method=None, jac=None, **kwargs)[source]
        print(item)
        popt, pcov = curve_fit(rawSVI,k,w,maxfev = 100000)

        parameterDict[item] = popt
    return parameterDict

dataFile = open('inputHW7.txt','r')
#List of expiries
expiry = ['04/17/2020','05/15/2020','06/19/2020','06/30/2020','07/17/2020','08/21/2020','09/18/2020','09/30/2020','10/16/2020','11/20/2020','12/18/2020','12/31/2020','03/19/2021','06/18/2021','12/17/2021']

output = SVI_Fit(dataFile,expiry)


#Writes the ouput file
with open('HW7_output.csv', mode ='w') as outfile:
    output_writer = csv.writer(outfile, delimiter= ',', quotechar= '"', quoting = csv.QUOTE_MINIMAL)
    for element in output:
        output_writer.writerow([element,output[element]])


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




