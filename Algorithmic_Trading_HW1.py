#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import csv
import datetime
#Create a Data Frame
OrderBook = pd.read_csv('data_orderbook.csv')
OutFile = open('RecTrades.csv','w')
Writer = csv.writer(OutFile)

nrows = OrderBook.shape[0]
BuyOrders = {}
SellOrders = {}

MarketBuyPrecedence = []
MarketSellPrecedence = []

LimitBuyPrecedence = []
LimitSellPrecedence = []

count = 0

def MakeTrade(BOrder,SOrder,BVol,SVol,Date,Time,BuyPrice,SellPrice,File,BuyDate,BuyTime,SellDate,SellTime,OType):
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
    Writer.writerow([BOrder,SOrder,TradeTime,TradePrice,TradeVolume])
    
    return BVol,SVol


#This is the main for loop, to parse through the Order Book
TradeCount = 0
for i in range(nrows):
    #print("Progress {:2.1%}".format(i/nrows), end="\r")
    if (i%500)==0:
        print('Progress :',i,'Trades:',TradeCount,end='\r')
        
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
        
    else:
        if OrderBook['bors'][i] == 'B':
            price = OrderBook['lp'][i]
            date = OrderBook['date'][i]
            time = OrderBook['time'][i]
            volume = OrderBook['vo'][i]
            Market = OrderBook['mkt'][i]          
            BuyOrders[OrderBook['orno'][i]] = {'P':price,'D':date,'T':time,'V':volume,'M':Market}            
                
            if len(LimitBuyPrecedence)==0:
                LimitBuyPrecedence.append(OrderBook['orno'][i])
            else:
                res_list = list(filter(lambda x: (float(OrderBook['lp'][i])>float(BuyOrders[LimitBuyPrecedence[x]]['P'])), range(len(LimitBuyPrecedence)))) 
                if len(res_list)==0:
                    LimitBuyPrecedence.append(OrderBook['orno'][i])
                else:
                    LimitBuyPrecedence.insert(res_list[0],OrderBook['orno'][i])
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
        print('\nReached End')
        
        
    else:
        while len(MarketBuyPrecedence)>0 and len(LimitSellPrecedence)>0:
            TradeCount = TradeCount + 1
            BOrder = MarketBuyPrecedence[0]
            SOrder = LimitSellPrecedence[0]
            
            [BuyOrders[BOrder]['V'],SellOrders[SOrder]['V']] = MakeTrade(BOrder,SOrder,BuyOrders[BOrder]['V'],SellOrders[SOrder]['V'],
                                                               OrderBook['date'][i],OrderBook['time'][i],BuyOrders[BOrder]['P'],
                                                               SellOrders[SOrder]['P'],OutFile,BuyOrders[BOrder]['D'],BuyOrders[BOrder]['T'],
                                                               SellOrders[SOrder]['D'],SellOrders[SOrder]['T'],'MarketBuy') 
            if BuyOrders[BOrder]['V'] == 0:
                            del BuyOrders[BOrder]
                            MarketBuyPrecedence.remove(BOrder)
            if SellOrders[SOrder]['V'] == 0:
                            del SellOrders[SOrder]
                            LimitSellPrecedence.remove(SOrder)
            
            
            
            
            
            
        while len(MarketSellPrecedence)>0 and len(LimitBuyPrecedence)>0:
            TradeCount = TradeCount + 1
            BOrder = LimitBuyPrecedence[0]
            SOrder = MarketSellPrecedence[0]
            
            [BuyOrders[BOrder]['V'],SellOrders[SOrder]['V']] = MakeTrade(BOrder,SOrder,BuyOrders[BOrder]['V'],SellOrders[SOrder]['V'],
                                                               OrderBook['date'][i],OrderBook['time'][i],BuyOrders[BOrder]['P'],
                                                               SellOrders[SOrder]['P'],OutFile,BuyOrders[BOrder]['D'],BuyOrders[BOrder]['T'],
                                                               SellOrders[SOrder]['D'],SellOrders[SOrder]['T'],'MarketSell') 
            if BuyOrders[BOrder]['V'] == 0:
                            del BuyOrders[BOrder]
                            LimitBuyPrecedence.remove(BOrder)
            if SellOrders[SOrder]['V'] == 0:
                            del SellOrders[SOrder]
                            MarketSellPrecedence.remove(SOrder)
            
            
        while len(LimitBuyPrecedence)>0 and len(LimitSellPrecedence)>0:
            TradeCount = TradeCount + 1
            BOrder = LimitBuyPrecedence[0]
            SOrder = LimitSellPrecedence[0]
            
            if float(BuyOrders[BOrder]['P'])>=float(SellOrders[SOrder]['P']):
                [BuyOrders[BOrder]['V'],SellOrders[SOrder]['V']] = MakeTrade(BOrder,SOrder,BuyOrders[BOrder]['V'],SellOrders[SOrder]['V'],
                                                               OrderBook['date'][i],OrderBook['time'][i],BuyOrders[BOrder]['P'],
                                                               SellOrders[SOrder]['P'],OutFile,BuyOrders[BOrder]['D'],BuyOrders[BOrder]['T'],
                                                               SellOrders[SOrder]['D'],SellOrders[SOrder]['T'],'2SidedLimit') 
                if BuyOrders[BOrder]['V'] == 0:
                            del BuyOrders[BOrder]
                            LimitBuyPrecedence.remove(BOrder)
                if SellOrders[SOrder]['V'] == 0:
                            del SellOrders[SOrder]
                            LimitSellPrecedence.remove(SOrder)
            else:
                break


# In[6]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




