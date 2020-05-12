#!/usr/bin/env python
# coding: utf-8

# In[27]:


#Author: Cameron R. Shabahang
#Design algorithm for trading and compare performance with standard algorithm
#Use VWAP or any other algorithm as a benchmark
#Transaction cost analysis: implementation shortfall, IS vs. cost estimate, reversion
#If using block trading, use identifier of the hidden order 
#Use machine learning techniques, bid-ask, spread, vol, volume, past return
#Training, testing, and hold-out sample
#Use orderbook and tradebook given to run simulation 
import pandas as pd

#orderbook = pd.read_csv('data_orderbook.csv')
#tradebook = pd.read_csv('data_tradebook.csv')
import pandas as pd
import csv
import datetime
import numpy as np
import matplotlib.pyplot as plt
#Create a Data Frame
OrderBook = pd.read_csv('data_orderbook.csv')
OutFile = open('RecTradesFinalProject.csv','w')
Writer = csv.writer(OutFile)

nrows = OrderBook.shape[0]
BuyOrders = {}
SellOrders = {}

MarketBuyPrecedence = []
MarketSellPrecedence = []

LimitBuyPrecedence = []
LimitSellPrecedence = []

count = 0


def MakeTrade(BOrder,SOrder,BVol,SVol,Date,Time,BuyPrice,SellPrice,File,BuyDate,BuyTime,SellDate,SellTime,OType,Bid,Ask):
    #print(OType)
    #print(BOrder)
    #print(SOrder)
    TradeVolume = min(BVol,SVol)
    BVol=BVol-TradeVolume
    SVol=SVol-TradeVolume
    DString = Date+' '+Time
    TradeTime = datetime.datetime.strptime(DString, '%d-%b-%y %H:%M:%S')
    DString = BuyDate+' '+BuyTime
    BuyTime = datetime.datetime.strptime(DString, '%d-%b-%y %H:%M:%S')
    DString = SellDate+' '+SellTime
    SellTime = datetime.datetime.strptime(DString, '%d-%b-%y %H:%M:%S')
            
    
   # print(TradeTime)
   # print(TradeVolume)
    
    
    if OType == '2SidedLimit':
        if BuyTime>=SellTime:
            TradePrice = SellPrice
        else:
            TradePrice = BuyPrice
    
    elif OType == 'MarketSell':
        TradePrice = BuyPrice
    
    elif OType == 'MarketBuy':
        TradePrice = SellPrice
    
    #print(TradePrice)
    Writer = csv.writer(File)
    Writer.writerow([BOrder,SOrder,TradeTime,TradePrice,TradeVolume,Bid,Ask])
    
    return BVol,SVol,TradePrice,TradeVolume

Trades = 0
TradePrices=[]
TradeVol=[]
MA20 = []
MA5 = []
UpperBand=[]
LowerBand=[]
DataPoints = 0

#This is the main for loop, to parse through the Order Book
TradeCount = 0
for i in range(nrows):
    #print("Progress {:2.1%}".format(i/nrows), end="\r")
    if (i%500)==0:
        print('Progress :',i,'Trades:',TradeCount,end='\r')
        
    #Check if order exists and delete, so that we can update
    if OrderBook['orno'][i] in BuyOrders:
        if BuyOrders[OrderBook['orno'][i]]['M']=='Y':
            MarketBuyPrecedence.remove(OrderBook['orno'][i])
        else:
            LimitBuyPrecedence.remove(OrderBook['orno'][i])
        del BuyOrders[OrderBook['orno'][i]]
        
    elif OrderBook['orno'][i] in SellOrders:
        if SellOrders[OrderBook['orno'][i]]['M']=='Y':
            MarketSellPrecedence.remove(OrderBook['orno'][i])
        else:
            LimitSellPrecedence.remove(OrderBook['orno'][i])
                
        del SellOrders[OrderBook['orno'][i]]

    #Append market Orders
    if OrderBook['mkt'][i]=='Y':
        if OrderBook['bors'][i] == 'B':            
                    price = -1
                    date = OrderBook['date'][i]
                    time = OrderBook['time'][i]
                    volume = OrderBook['vo'][i]
                    Market = OrderBook['mkt'][i]          
                    BuyOrders[OrderBook['orno'][i]] = {'P':price,'D':date,'T':time,'V':volume,'M':Market}
                    MarketBuyPrecedence.append(OrderBook['orno'][i])
        else:                
                    price = -1
                    date = OrderBook['date'][i]
                    time = OrderBook['time'][i]
                    volume = OrderBook['vo'][i]
                    Market = OrderBook['mkt'][i]          
                    SellOrders[OrderBook['orno'][i]] = {'P':price,'D':date,'T':time,'V':volume,'M':Market}
                    MarketSellPrecedence.append(OrderBook['orno'][i])
    
    #Set limit order in Precedence List  
    else:
        if OrderBook['bors'][i] == 'B':
            price = OrderBook['lp'][i]
            date = OrderBook['date'][i]
            time = OrderBook['time'][i]
            volume = OrderBook['vo'][i]
            Market = OrderBook['mkt'][i]          
            BuyOrders[OrderBook['orno'][i]] = {'P':price,'D':date,'T':time,'V':volume,'M':Market}            
            #If nothing exists at current time, append    
            if len(LimitBuyPrecedence)==0:
                LimitBuyPrecedence.append(OrderBook['orno'][i])
            else:
                #Insert limit order as per price and time precedence
                res_list = list(filter(lambda x: (float(OrderBook['lp'][i])>float(BuyOrders[LimitBuyPrecedence[x]]['P'])), range(len(LimitBuyPrecedence)))) 
                if len(res_list)==0:
                    LimitBuyPrecedence.append(OrderBook['orno'][i])
                #If incoming limit order has the least price priority, append at the end
                else:
                    LimitBuyPrecedence.insert(res_list[0],OrderBook['orno'][i])
                    
                    
                    
                    
                    
        #Same logic as aove
        else:
            price = OrderBook['lp'][i]
            date = OrderBook['date'][i]
            time = OrderBook['time'][i]
            volume = OrderBook['vo'][i]
            Market = OrderBook['mkt'][i]          
            SellOrders[OrderBook['orno'][i]] = {'P':price,'D':date,'T':time,'V':volume,'M':Market}            
                
            if len(LimitSellPrecedence)==0:
                LimitSellPrecedence.append(OrderBook['orno'][i])
            else:
                res_list = list(filter(lambda x: (float(OrderBook['lp'][i])<float(SellOrders[LimitSellPrecedence[x]]['P'])), range(len(LimitSellPrecedence)))) 
                if len(res_list)==0:
                    LimitSellPrecedence.append(OrderBook['orno'][i])
                else:
                    LimitSellPrecedence.insert(res_list[0],OrderBook['orno'][i])

                    
                    

    if i == nrows-1:
        print('\nLast Call')
        
    #Match Market Buys with Limit Sells. Keep looping till Market orders are filled out  
    # or Limit orders run out
    
    while len(MarketBuyPrecedence)>0 and len(LimitSellPrecedence)>0:
        
            
            TradeCount = TradeCount + 1
            BOrder = MarketBuyPrecedence[0]
            SOrder = LimitSellPrecedence[0]
            
            Ask = SellOrders[LimitSellPrecedence[0]]['P']
            if len(LimitBuyPrecedence)>0:
                Bid = BuyOrders[LimitBuyPrecedence[0]]['P']
            else:
                Bid = 0
            
            
            [BuyOrders[BOrder]['V'],SellOrders[SOrder]['V'],TP,TV] = MakeTrade(BOrder,SOrder,BuyOrders[BOrder]['V'],SellOrders[SOrder]['V'],
                                                                     OrderBook['date'][i],OrderBook['time'][i],BuyOrders[BOrder]['P'],
                                                                     SellOrders[SOrder]['P'],OutFile,BuyOrders[BOrder]['D'],BuyOrders[BOrder]['T'],
                                                                     SellOrders[SOrder]['D'],SellOrders[SOrder]['T'],'MarketBuy',Bid,Ask)
            Trades=Trades+1
            TradePrices.append(TP)
            TradeVol.append(TV)
            if Trades>=5:
                MAData = np.asarray(TradePrices[Trades-20:Trades])
                
            MAData = np.asarray(TradePrices[0:Trades])
            MA20.append(np.mean(MAData))
            UpperBand.append(np.mean(MAData)+2*np.std(MAData))
            LowerBand.append(np.mean(MAData)-2*np.std(MAData))
            DataPoints = Trades
    
    
            if BuyOrders[BOrder]['V'] == 0:
                            del BuyOrders[BOrder]
                            MarketBuyPrecedence.remove(BOrder)
            if SellOrders[SOrder]['V'] == 0:
                            del SellOrders[SOrder]
                            LimitSellPrecedence.remove(SOrder)
            
            
            
            
            
    #Match Market Sells with Limit Buys. Keep looping till Market orders are filled out  
    # or Limit orders run out
    while len(MarketSellPrecedence)>0 and len(LimitBuyPrecedence)>0:
            TradeCount = TradeCount + 1
            BOrder = LimitBuyPrecedence[0]
            SOrder = MarketSellPrecedence[0]
            
            Bid = BuyOrders[LimitBuyPrecedence[0]]['P']
            if len(LimitSellPrecedence)>0:
                Ask = SellOrders[LimitSellPrecedence[0]]['P']
            else:
                Ask = 0
            
            
            [BuyOrders[BOrder]['V'],SellOrders[SOrder]['V'],TP,TV] = MakeTrade(BOrder,SOrder,BuyOrders[BOrder]['V'],SellOrders[SOrder]['V'],
                                                                     OrderBook['date'][i],OrderBook['time'][i],BuyOrders[BOrder]['P'],
                                                                     SellOrders[SOrder]['P'],OutFile,BuyOrders[BOrder]['D'],BuyOrders[BOrder]['T'],
                                                                     SellOrders[SOrder]['D'],SellOrders[SOrder]['T'],'MarketSell',Bid,Ask)
            Trades=Trades+1
            TradePrices.append(TP)
            TradeVol.append(TV)
            if Trades>=5:
                MAData = np.asarray(TradePrices[Trades-20:Trades])
            
            MAData = np.asarray(TradePrices[0:Trades])
            MA20.append(np.mean(MAData))
            UpperBand.append(np.mean(MAData)+2*np.std(MAData))     
            LowerBand.append(np.mean(MAData)-2*np.std(MAData))                
            DataPoints = Trades

            if BuyOrders[BOrder]['V'] == 0:
                            del BuyOrders[BOrder]
                            LimitBuyPrecedence.remove(BOrder)
            if SellOrders[SOrder]['V'] == 0:
                            del SellOrders[SOrder]
                            MarketSellPrecedence.remove(SOrder)
            
    #Match Limit Buys and Sells. Trade happens, if there is a price overlap
    #in Bid(Buy) and Ask(Sell)
    while len(LimitBuyPrecedence)>0 and len(LimitSellPrecedence)>0:
            
            BOrder = LimitBuyPrecedence[0]
            SOrder = LimitSellPrecedence[0]
            
            if float(BuyOrders[BOrder]['P'])>=float(SellOrders[SOrder]['P']):
                TradeCount = TradeCount + 1
                [BuyOrders[BOrder]['V'],SellOrders[SOrder]['V'],TP,TV] = MakeTrade(BOrder,SOrder,BuyOrders[BOrder]['V'],SellOrders[SOrder]['V'],
                                                                         OrderBook['date'][i],OrderBook['time'][i],BuyOrders[BOrder]['P'],
                                                                         SellOrders[SOrder]['P'],OutFile,BuyOrders[BOrder]['D'],BuyOrders[BOrder]['T'],
                                                                         SellOrders[SOrder]['D'],SellOrders[SOrder]['T'],'2SidedLimit',BuyOrders[LimitBuyPrecedence[0]]['P'],SellOrders[LimitSellPrecedence[0]]['P'])  
                Trades=Trades+1
                TradePrices.append(TP)
                TradeVol.append(TV)
                if Trades>=5:
                    MAData = np.asarray(TradePrices[Trades-20:Trades])
                MAData = np.asarray(TradePrices[0:Trades])
                MA20.append(np.mean(MAData))
                UpperBand.append(np.mean(MAData)+2*np.std(MAData))
                LowerBand.append(np.mean(MAData)-2*np.std(MAData))
                DataPoints = Trades 
        

                if BuyOrders[BOrder]['V'] == 0:
                            del BuyOrders[BOrder]
                            LimitBuyPrecedence.remove(BOrder)
                if SellOrders[SOrder]['V'] == 0:
                            del SellOrders[SOrder]
                            LimitSellPrecedence.remove(SOrder)
            else:
                break


# In[ ]:





# In[30]:


import matplotlib.pyplot as plt
plt.plot(TradePrices)
plt.plot(MA20)
plt.plot(UpperBand)
plt.plot(LowerBand)
plt.ylim(2965,2995)
plt.xlim(1900,2200)


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





# In[ ]:





# In[ ]:




