#!/usr/bin/env python
# coding: utf-8

# In[72]:


#Author: Cameron R. Shabahang
#From the tradebook and order data snapshots of every minute
#Estimate probability of hidden order using classification
#Estimate amount of a hidden order using regression
#Describe a liquidity seeking algorithm

#Source: Avellanada et. al (2010), "Forecasting Prices in Presence of Hidden Liquidity"

#Prob(deltaP>0|OB)=p(OB)
#deltaP = next midprice move
#OB = pair of bid and ask sizes
#p(x,y;H) = (x+H)/(x+y+2H)

#Estimation procedure
# 1) Remove zero and negative spreads
# 2) Bucket the bid and ask sizes by taking deciles of the bid and ask size and normalizing
# 3) Compute the empirical probability that the price goes up u(ij)
# 4) Count the number of occurences and denote the distribution d(ij)
# 5) Minimize least squares for the negative correlated queues and obtain hidden liquidity

import pandas as pd
import numpy as np
order = pd.read_excel("PS1Data_orderbook.xlsx")
trade = pd.read_excel("PS1Data_tradebook.xlsx")
#print(order)
#print(trade)

print(order)


# In[ ]:





# In[73]:


#Return index with unique values
num_bid = []
num_ask = []
bids = order[~order.bors.str.contains("S")]
bid_size = bids[['date', 'time','vo']]
bid_size = bid_size.rename(columns={"vo": "Bid Size"})
print('Bid size: ')
print(bid_size)

asks = order[~order.bors.str.contains("B")]
ask_size = asks[['date', 'time','vo']]
ask_size = ask_size.rename(columns={'vo': 'Ask Size'})
print('\nAsk size:')
print(ask_size)

bid_ask = pd.merge(bid_size, ask_size, how = 'outer')
bid_ask


# In[82]:


#Remove zero and negative spreads 

bid_ask = bid_ask.dropna(axis=0, how='any', subset=['Bid Size', 'Ask Size'])
#for i in range(len(bid_ask.index)):
    #if bid_ask['Bid Size'][i]<= bid_ask['Ask Size'][i]:
        #bid_ask = bid_ask.drop(axis = 0)
#bid_ask
bid_ask['Comp'] = np.where((bid_ask['Bid Size'] > bid_ask['Ask Size']) , bid_ask['Bid Size'], np.nan)
ba = bid_ask.dropna(axis=0, how='any', subset=['Comp'])
ba = ba.drop(['Comp'], axis = 1)
ba


# In[ ]:


#Bucket the bid and ask sizes by taking deciles of the bid and ask size and normalizing


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





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[75]:


#Liquidity-seeking algorithms

#For a highly illiquid stock, algorithms try to match every order that has a favorable price 
#Called liquidity-seeking algorithms

#Source: Barclays - "Hydra"
#It starts with more differentiated levels of dark and lit aggression that the buy-side trader 
#wants to utilize in seeking liquidity – termed Quiet, Neutral, Aggressive and Dark Only. 
#What Barclays has added for the buy-side trader are standardized parameters to govern the 
#execution framework for the strategy. These parameters determine how the strategy interacts 
#with dark liquidity, thus enabling the configuration of more unique execution styles. Furthermore, 
#traders can customize these parameters – allowing a trader to fine-tune the execution styles.


# In[76]:


#Source: Almgren - "A Dynamic Algorithm for Smart Order Routing" (2007)

#To begin with, let us focus on a single venue and a single side, let us say buy
#orders posted on the bid. Suppose that we see a series of trades executing at
#the bid prices, of sizes S1, S2, . . . . For each execution Sn, let us denote
#sn = visible liquidity just before execution n, and
#rn = hidden liquidity just before execution n.

#Note: These would be calculated in the last section

#Thus wn is the quantity executed against hidden liquidity, which will be zero
#if the executed quantity is less than the visible quantity. Our task is to form
#some estimate ˆrn+1 of the hidden liquidity remaining after the execution.

#Each time we observe an execution with wn > 0, we increase rˆn by wn,
#the amount of the execution that can be attributed to hidden liquidity.

#As time passes, we decrease ˆrn toward zero using an exponential decay.
#It will be more appropriate to use trade time than clock time, so an
#equivalent statement would be that on each execution, whether wn = 0
#or wn > 0, we multiply ˆrn by a fixed factor ρ with 0 < ρ < 1.

#rˆn+1 = ρ rˆn + wn.


# In[ ]:




