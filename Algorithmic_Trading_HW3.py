#!/usr/bin/env python
# coding: utf-8

# In[33]:


import pandas as pd
import numpy as np
from scipy.stats import poisson
import matplotlib.pyplot as plt

#Import orderbook and tradebook
order = pd.read_excel("PS1Data_orderbook.xlsx")
trade = pd.read_excel("PS1Data_tradebook.xlsx")

#From the trade book data for each day, estimate PIN
#Plot the time series pattern of PIN 

#Return index with unique values
num_days = len(trade.date.unique()) 
trade.date.unique()

#Choose four days to evaluate 
data_3 = trade[trade['date'] == '2006-04-03T00:00:00.000000000']
data_4 = trade[trade['date'] == '2006-04-04T00:00:00.000000000']
data_5 = trade[trade['date'] == '2006-04-05T00:00:00.000000000']
data_7 = trade[trade['date'] == '2006-04-07T00:00:00.000000000']


# In[34]:


#Append the buys and sells in array
num_buys = []
num_sells = []
num_buys.append(len(data_3.bno.unique()))
num_buys.append(len(data_4.bno.unique()))
num_buys.append(len(data_5.bno.unique()))
num_buys.append(len(data_7.bno.unique()))
num_sells.append(len(data_3.sno.unique()))
num_sells.append(len(data_4.sno.unique()))
num_sells.append(len(data_5.sno.unique()))
num_sells.append(len(data_7.sno.unique()))

def log_lik(x):
    alpha = x[0]
    delta = x[1]
    mu = x[2]
    epsilon = x[3]
    log_sum_lik = []
    i=0

    while (i < num_days):
        lik_no_news = (1-alpha)*poisson.pmf(num_buys[i], epsilon)*poisson.pmf(num_sells[i], epsilon)
        lik_bad_news = alpha*delta*poisson.pmf(num_buys[i], epsilon)*poisson.pmf(num_sells[i], mu+epsilon)
        lik_good_news = alpha*(1-delta)*poisson.pmf(num_buys[i], mu+epsilon)*poisson.pmf(num_sells[i], epsilon)
        sum_lik = lik_no_news+lik_bad_news+lik_good_news+1E-100
        log_sum_lik.append(np.log(sum_lik))
        i=i+1
    
    log_lik = sum(log_sum_lik)
    return log_lik


# In[35]:


from scipy.optimize import minimize
#Function to define minimization 
def minimization(x):
    x1 = x[0]
    x2 = x[1]
    x3 = x[2]
    x4 = x[3]
    return -log_lik(x)

x0 = [0.4, 0.3, 75, 200]
b1 = (0.0, 1.0)
b2 = (0.0, np.inf)
bnds = (b1, b1, b2, b2)
fit = minimize(minimization, x0, method='SLSQP',bounds=bnds)
print(fit)


# In[36]:


#Calculation of PIN
outputs = [] 
outputs = fit.x
PIN = outputs[0]*outputs[2]/(outputs[0]*outputs[2]+2*outputs[3])  
plt.plot(['2016-04'], [PIN], 'ro')


#From the tradebook data snapshots of each hour, estimate PIN
#Plot the time series pattern of PIN
pd.to_datetime(data_3['time'], format='%H:%M:%S')
data_3['hours'] = [t.hour for t in data_3['time']]

pd.to_datetime(data_4['time'], format='%H:%M:%S')
data_4['hours'] = [t.hour for t in data_4['time']]

pd.to_datetime(data_5['time'], format='%H:%M:%S')
data_5['hours'] = [t.hour for t in data_5['time']]

pd.to_datetime(data_7['time'], format='%H:%M:%S')
data_7['hours'] = [t.hour for t in data_7['time']]

data_3_b = data_3.groupby('hours').apply(lambda x: len(x['bno'].unique()))
data_3_s = data_3.groupby('hours').apply(lambda x: len(x['sno'].unique()))
num_buys = data_3_b.values
num_sells = data_3_s.values

fit = minimize(minimization, x0, method='SLSQP',bounds=bnds)
print(fit)

outputs = []  
outputs = fit.x

#PIN3 for the 3rd, PIN4 is for the 4th, etc. 
PIN3 = outputs[0]*outputs[2]/(outputs[0]*outputs[2]+2*outputs[3]) 


data_4_b = data_4.groupby('hours').apply(lambda x: len(x['bno'].unique()))
data_4_s = data_4.groupby('hours').apply(lambda x: len(x['sno'].unique()))
num_buys = data_4_b.values
num_sells = data_4_s.values

fit = minimize(minimization, x0, method='SLSQP',bounds=bnds)
print(fit)

#List 'outputs' to hold alpha, delta, mu, and epsilon 
outputs = []  
outputs = fit.x

PIN4 = outputs[0]*outputs[2]/(outputs[0]*outputs[2]+2*outputs[3])   

data_5_b = data_5.groupby('hours').apply(lambda x: len(x['bno'].unique()))
data_5_s = data_5.groupby('hours').apply(lambda x: len(x['sno'].unique()))
num_buys = data_5_b.values
num_sells = data_5_s.values

fit = minimize(minimization, x0, method='SLSQP',bounds=bnds)
print(fit)

outputs = []  
outputs = fit.x

PIN5 = outputs[0]*outputs[2]/(outputs[0]*outputs[2]+2*outputs[3])   

data_7_b = data_7.groupby('hours').apply(lambda x: len(x['bno'].unique()))
data_7_s = data_7.groupby('hours').apply(lambda x: len(x['sno'].unique()))
num_buys = data_7_b.values
num_sells = data_7_s.values

fit = minimize(minimization, x0, method='SLSQP',bounds=bnds)
print(fit)

outputs = []  
outputs = fit.x

PIN7 = outputs[0]*outputs[2]/(outputs[0]*outputs[2]+2*outputs[3])   

plt.plot(['2006-04-03','2006-04-04','2006-04-05','2006-04-07'], [PIN3,PIN4,PIN5,PIN7])


#From the order book data snapshots of every hour for every day, estimate the PIO
#PIO = probability of informed order
#PIO is derived from buy and sell orders
#PIN=alpha*mu/(alpha*mu+2*epsilon)

num_days = len(order.date.unique()) 
order.date.unique()

data_3 = order[order['date'] == '2006-04-03T00:00:00.000000000']
data_4 = order[order['date'] == '2006-04-04T00:00:00.000000000']
data_5 = order[order['date'] == '2006-04-05T00:00:00.000000000']
data_7 = order[order['date'] == '2006-04-07T00:00:00.000000000']

pd.to_datetime(data_3['time'], format='%H:%M:%S')
data_3['hours'] = [t.hour for t in data_3['time']]

pd.to_datetime(data_4['time'], format='%H:%M:%S')
data_4['hours'] = [t.hour for t in data_4['time']]

pd.to_datetime(data_5['time'], format='%H:%M:%S')
data_5['hours'] = [t.hour for t in data_5['time']]

pd.to_datetime(data_7['time'], format='%H:%M:%S')
data_7['hours'] = [t.hour for t in data_7['time']]


data_3_b = data_3.groupby('hours').apply(lambda x: (x['bors']=='B').sum())
data_3_s = data_3.groupby('hours').apply(lambda x: (x['bors']=='S').sum())
num_buys = data_3_b.values
num_sells = data_3_s.values

fit = minimize(minimization, x0, method='SLSQP',bounds=bnds)
print(fit)

outputs = []
outputs = fit.x

PIO3 = outputs[0]*outputs[2]/(outputs[0]*outputs[2]+2*outputs[3])


data_4_b = data_4.groupby('hours').apply(lambda x: (x['bors']=='B').sum())
data_4_s = data_4.groupby('hours').apply(lambda x: (x['bors']=='S').sum())
num_buys = data_4_b.values
num_sells = data_4_s.values

fit = minimize(minimization, x0, method='SLSQP',bounds=bnds)
print(fit)

outputs = []  
outputs = fit.x

PIO4 = outputs[0]*outputs[2]/(outputs[0]*outputs[2]+2*outputs[3])


data_5_b = data_5.groupby('hours').apply(lambda x: (x['bors']=='B').sum())
data_5_s = data_5.groupby('hours').apply(lambda x: (x['bors']=='S').sum())
num_buys = data_5_b.values
num_sells = data_5_s.values

fit = minimize(minimization, x0, method='SLSQP',bounds=bnds)
print(fit)

outputs = []  
outputs = fit.x

PIO5 = outputs[0]*outputs[2]/(outputs[0]*outputs[2]+2*outputs[3])


data_7_b = data_7.groupby('hours').apply(lambda x: (x['bors']=='B').sum())
data_7_s = data_7.groupby('hours').apply(lambda x: (x['bors']=='S').sum())
num_buys = data_7_b.values
num_sells = data_7_s.values

fit = minimize(minimization, x0, method='SLSQP',bounds=bnds)
print(fit)
outputs = []  
outputs = fit.x

PIO7 = outputs[0]*outputs[2]/(outputs[0]*outputs[2]+2*outputs[3])

plt.plot(['2006-04-03','2006-04-04','2006-04-05','2006-04-07'], [PIO3,PIO4,PIO5,PIO7])


# In[ ]:




