#!/usr/bin/env python
# coding: utf-8

# In[51]:


#alpha = probability of an information event
#delta = probability that the information is negative
#mu = arrival rate of traders who know the new information if it exists
#eps = arrival rate of uninformed traders
#PIN = unconditional probability of informed trading

#Import packages and read orderbook and tradebook with csv reader
from datetime import datetime
import pandas as pd
import csv
tradebookFile = open('tradebook3_new.csv','r')
orderbookFile = open('orderbook3_new.csv','r')
tradebook = csv.reader(tradebookFile)
orderbook = csv.reader(orderbookFile)
outfile = open('replicated.csv','w')
csvWriter = csv.writer(outfile)

#Create arrays for each relevant column of the csv file
dateTimeList = []
order = []
BorS = []
size = []
limitPrice = []
market = []

#Populate arrays for elements of the csv file
for row in orderbook:
    if row[1]!='series':
        year = 2006
        month = 4
        day = int(row[2][0])
        hour = int(row[3].split(':')[0])
        minute = int(row[3].split(':')[1])
        second = int(row[3].split(':')[2])
        dateTimeList.append(datetime.datetime(year,month,day,hour,minute,second))
       
        order.append(float(row[4]))
        BorS.append(row[5])
        size.append(int(row[7]))
        market.append(row[9])
        
        if row[9]=='N':
            limitPrice.append(float(row[8]))
        else:
            limitPrice.append(-1)

            
            
#Modify the orderbook and tradebook to place 10000 buy orders and 10000 sell orders
#Trader has started trading at 9:55:28 and ended at 15:59:03
#Place volume at equal time intervals
rawdata = pd.read_csv('orderbook3_new.csv', dtype = object)
#print(rawdata)

#Define method to calculate time between two times
def calcTime(s1, s2):
    s1 = timestart
    s2 = timend
    FMT = '%H:%M:%S'
    tdelta = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
    print(tdelta)
    return (tdelta)

#Define method to add a number of seconds to a time 
def addSecs(tm, secs):
    fulldate = datetime.datetime(2006, 4, 3, tm.hour, tm.minute, tm.second)
    fulldate = fulldate + datetime.timedelta(seconds=secs)
    return fulldate.time()

for i in range(4): 
    fulldate += datetime.timedelta(days=1)
    print(fulldate) 
    if rawdata['date'] == fulldate:
        timestart = rawdata['time'][0]
        timelen = len(rawdata)
        timeend = rawdata['time'][timelen-1]
        #Call the calcTime method
        diff = calcTime(timestart,timeend)
        seconds = diff.total_seconds()
        print(seconds)
        interval = 
else if 



#a = datetime.datetime.now().time()
#b = addSecs(a, interval)
#print(a)
#print(b)

        



#Calculate # of buy and # of sell orders
buy_count = 0
sell_count =0
for i in range (len(BorS)):
    if BorS[i]=='B':
        buy_count = buy_count+1
    else:
        sell_count = sell_count+1
print('The # of buy orders is: ' , buy_count)
print('The # of sell orders is:' , sell_count)

alpha, delta, mu, eps = 0,0,0,0

def PIN():
    prob_a = (alpha*mu)/((alpha*mu)+(2*eps))
    return prob_a




#def likel_pin(params,n_trades)
    #return likel_final

#INPUTS:
# n_trades(1,:) = number of 'no trades'
# n_trades(2,:) = number of buy-initiated trades
# n_trades(3,:) = number of sell-initiated trades
# params(1)     := eps = probability that an uninformed trader enters the market
# params(2)     := mu  = probability that an informed trader enters the market 
# params(3)     := alpha = probability that an informative trade takes place
# params(4)     := delta = probability of a low-price signal
#OUTPUT:
# likel_final: (negative of) value of the log-likelihood  

#Reference:
#
# Easley, D., N. M. Kiefer, M. O'Hara and J. B. Paperman, 1996, 
#
# "Liquidity, Information, and Infrequently Traded Stocks",  
#
# Journal of Finance, 51(4), 1405-36.
        
#N = n_trades(1,:); 
#B = n_trades(2,:);
#S = n_trades(3,:);
eps = params[1]
mu  = params[2]
alpha = params[3]
delta = params[4]
trad_days=len(n_trades)
likel  = []
likel1 = np.zeros(trad_days,1)
for j in range (len(trad_days)):
    buy_s     = B[j]
    sell_s    = S[j]
    notrade_s = N[j]
    A=(1-mu)*eps/2;
    part1 = (1-eps)^(notrade_s)
    part2 = (1-mu)^(notrade_s)
    part3 = A^(buy_s+sell_s)
    part4 = alpha*(1-delta)*((mu/A)+1)^(buy_s)
    part5 = alpha*delta*(mu/A+1)^(sell_s)
    part6 = (1-alpha)*( 1/(1-mu) )^(buy_s+sell_s+notrade_s)
    likel = likel + log( part1*part2*part3*( part4 + part5 + part6 ) );
    likel1[j]=log( part1*part2*part3*( part4 + part5 + part6 ) );
    likel_final = -likel 


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




