#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

# In[189]:


##### The code has two basic steps
#### 1. In each iteration of the for loop, through the order Book,
####    we first update BuyPrecedence and SellPrecedence
#### 2. Once, step 1 is complete, we check for trades, until
####    no more trades are possible at the current time, and
####    new orders have to come in. This is achieved by a while
####    loop inside the main for loop


import pandas as pd
import csv
import datetime as dt
#Create a Data Frame
OrderBook = pd.read_csv('orderbook3_copy.csv')

#OrderBook = OrderBook.head(100)

# Take Date and Time as Strings and return a Python datetime object
def DateTimeObject(Date,Time):
    Day = Date[0]
    count = 0
    Hour = ''
    Minute = ''
    Second = ''
    for s in Time:
        if s==':':
            count = count + 1
        else:
            if count == 0:
                Hour = Hour + s
            elif count == 1:
                Minute = Minute + s
            elif count == 2:
                Second = Second + s
    return dt.datetime(year = 2006,month = 4,day = int(Day),hour = int(Hour),minute = int(Minute),second = int(Second))            

OutFile = open('RecTradesNew.csv','w')
Writer = csv.writer(OutFile)


# In[190]:


#Initialize everything
nrows = OrderBook.shape[0]
BuyOrders = {}
SellOrders = {}
BuyPrecedence = []
SellPrecedence = []
count = 0


# In[ ]:


#This is the main for loop, to parse through the Order Book
for i in range(nrows):
    print(i)
    #Check for existing orders and delete them, as they have to be updated
    if OrderBook['orno'][i] in BuyOrders:
        del BuyOrders[OrderBook['orno'][i]]
        #if OrderBook['orno'][i] in BuyPrecedence:
        BuyPrecedence.remove(OrderBook['orno'][i])
        
    elif OrderBook['orno'][i] in SellOrders:
        del SellOrders[OrderBook['orno'][i]]
     #   if OrderBook['orno'][i] in SellPrecedence:
        SellPrecedence.remove(OrderBook['orno'][i])
            
    ####Enter here for market Orders
    if OrderBook['mkt'][i]=='Y':
        
     ##########                         ###################
     ########### MARKET ORDERS FOLLOW!!!! #################### 
     ###########                        ################# 
        
        ###Enter here for Market buys
        if OrderBook['bors'][i] == 'B':
            check = 'no'
            
            #Set default market price to -1,
            #since market orders always get executed at the available price
            price = -1
            #Fill in other details of the order
            time = DateTimeObject(OrderBook['date'][i],OrderBook['time'][i])
            volume = OrderBook['vo'][i]
            Market = OrderBook['mkt'][i]
            #Write to Buy dictionary
            BuyOrders[OrderBook['orno'][i]] = {'P':price,'T':time,'V':volume,'M':Market}
            
                
            #if BuyPrecedence has no elements, then the code
            #under the following else clause will run into an error
            #Hence, this if statement is necessary
            if len(BuyPrecedence)==0:
                BuyPrecedence.append(OrderBook['orno'][i])
            else:
                BuyListSize = len(BuyPrecedence)
                #Compare against exisiting orders for precedence                
                for j in range(BuyListSize):
                    if BuyOrders[BuyPrecedence[j]]['M']=='Y':
                        continue
                    else:
                        BuyPrecedence.insert(j,OrderBook['orno'][i])
                        check='yes'
                        break
                #Suppose only Market orders were present in
                #Buy precedence, then the new incoming Market
                #order has to be placed at the end. This
                #is not accounted for in the preceding if else
                #block. So,the following three lines ensure this            
                TempBuySize = len(BuyPrecedence)
                if TempBuySize == BuyListSize:
                    BuyPrecedence.append(OrderBook['orno'][i])
                
                    
                
        #Enter here for market sells
        elif OrderBook['bors'][i] == 'S':
            #Set default market price to -1,
            #since market orders always get executed at the available price
            price = -1
            
            #Fill other details of the order
            time = DateTimeObject(OrderBook['date'][i],OrderBook['time'][i])
            volume = OrderBook['vo'][i]
            Market = OrderBook['mkt'][i]

            #Write to sell dictionary
            SellOrders[OrderBook['orno'][i]] = {'P':price,'T':time,'V':volume,'M':Market}
            
                
            #if SellPrecedence has no elements, then the code
            #under the following else clause will run into an error
            #Hence, this if statement is necessary
            if len(SellPrecedence)==0:
                SellPrecedence.append(OrderBook['orno'][i])
            else:
                SellListSize = len(SellPrecedence)
                #Compare against exisiting orders for precedence
                for j in range(SellListSize):
                    if SellOrders[SellPrecedence[j]]['M']=='Y':
                        continue
                    else:
                        SellPrecedence.insert(j,OrderBook['orno'][i])
                        break
                #Suppose only Market orders were present in
                #Buy precedence, then the new incoming Market
                #order has to be placed at the end. This
                #is not accounted for in the preceding if else
                #block. So,the following three lines ensure this
                
                TempSellSize = len(SellPrecedence)
                if TempSellSize == SellListSize:
                    SellPrecedence.append(OrderBook['orno'][i])
                
                
     ##########                         ###################
     ########### LIMIT ORDERS FOLLLOW!!!! #################### 
     ###########                        ################# 

          
                
                
                
            
    elif OrderBook['mkt'][i] == 'N':
        #Enter here for Limit Buys
        if OrderBook['bors'][i] == 'B':

            #Gather order Details
            price = OrderBook['lp'][i]
            time = DateTimeObject(OrderBook['date'][i],OrderBook['time'][i])
            volume = OrderBook['vo'][i]
            Market = OrderBook['mkt'][i]
            
            #Write to buy dictionary
            BuyOrders[OrderBook['orno'][i]] = {'P':price,'T':time,'V':volume,'M':Market}
                
            
            #if BuyPrecedence has no elements, then the code
            #under the following else clause will run into an error
            #Hence, this if statement is necessary            
            if len(BuyPrecedence)==0:
                BuyPrecedence.append(OrderBook['orno'][i])
            else:
                BuyListSize = len(BuyPrecedence)
                #Compare against exisiting orders for precedence
                for j in range(BuyListSize):
                    
                    #Market orders get precedence always. Hence, we skip
                    if BuyOrders[BuyPrecedence[j]]['M']=='Y':
                        continue
                    elif BuyOrders[BuyPrecedence[j]]['M']=='N':
                        #Since we are in BuyPrecedence, lower prices
                        #imply lower precedence. Additionally, if prices
                        #were to match with existing ones, we must still
                        #account for time precedence. 'continue' ensures
                        #this is taken care of       
                        if float(OrderBook['lp'][i])<=float(BuyOrders[BuyPrecedence[j]]['P']):
                            continue
                        #Upon encountering a price in BuyPrecedence, which
                        #is lesser than Current order price, we insert
                        #our order here
                        elif float(OrderBook['lp'][i])>float(BuyOrders[BuyPrecedence[j]]['P']):
                            BuyPrecedence.insert(j,OrderBook['orno'][i])
                            break
                #If the current Buy Order limit price were to be
                #lower than all limit prices present in Buy Precedence
                #then, current entry has to go at the end. The preceding
                #if else block does not account for this. This is taken
                #care of, by the following three lines
                TempBuySize = len(BuyPrecedence)
                if TempBuySize == BuyListSize:
                    BuyPrecedence.append(OrderBook['orno'][i])
                
                
                    
        if OrderBook['bors'][i] == 'S':

            #Gather order data
            price = OrderBook['lp'][i]
            time = DateTimeObject(OrderBook['date'][i],OrderBook['time'][i])
            volume = OrderBook['vo'][i]
            Market = OrderBook['mkt'][i]
            
            #Write to Sell Order dictionary
            SellOrders[OrderBook['orno'][i]] = {'P':price,'T':time,'V':volume,'M':Market}
             
            #if SellPrecedence has no elements, then the code
            #under the following else clause will run into an error
            #Hence, this if statement is necessary
            
            if len(SellPrecedence)==0:
                SellPrecedence.append(OrderBook['orno'][i])
            else:
                SellListSize = len(SellPrecedence)
                #Compare against exisiting orders for precedence
                for j in range(SellListSize):
                    if SellOrders[SellPrecedence[j]]['M']=='Y':
                        continue
                    elif SellOrders[SellPrecedence[j]]['M']=='N':
                        #Since we are in SellPrecedence, higher prices
                        #imply lower precedence. Additionally, if prices
                        #were to match with existing ones, we must still
                        #account for time precedence. 'continue' ensures
                        #this is taken care of
                        if float(OrderBook['lp'][i])>=float(SellOrders[SellPrecedence[j]]['P']):
                            continue
                        #Upon encountering a price in SellPrecedence, which
                        #is greater than Current order price, we insert
                        #our order here
                        elif float(OrderBook['lp'][i])<float(SellOrders[SellPrecedence[j]]['P']):
                            SellPrecedence.insert(j,OrderBook['orno'][i])
                            break
                #If the current Sell Order limit price were to be
                #greater than all limit prices present in Buy Precedence
                #then, current entry has to go at the end. The preceding
                #if else block does not account for this. This is taken
                #care of, by the following three lines
                TempSellSize = len(SellPrecedence)
                if TempSellSize == SellListSize:
                    SellPrecedence.append(OrderBook['orno'][i])
                
               
         ### Check for trades continuously, until no
        # more trades are possible and we have to consider the 
        #next order from the order book
            
    while(len(BuyPrecedence)>0 and len(SellPrecedence)>0):
        #Loop 0
        #the variable match is used to break out of the
        #while loop, in case no trades are possible. This is
        # the case, when market orders when only Market orders exist
        #on both sides, or when there is a Bid-Ask Gap
        Match = 1
        for BOrder in BuyPrecedence:
            #Loop 1a If Top Buy order is a Market order, then
            #enter here
            if BuyOrders[BOrder]['M']=='Y':
                LCount = 0
                for SOrder in SellPrecedence:
                    #Loop 1a,2a
                    LCount = LCount + 1
                    if SellOrders[SOrder]['M']=='N':
                        #print('TradeFound1')
                        ##Note down trade details and write to output file
                        TradeVolume = min(BuyOrders[BOrder]['V'],SellOrders[SOrder]['V'])
                        BuyOrders[BOrder]['V']=BuyOrders[BOrder]['V']-TradeVolume
                        SellOrders[SOrder]['V']=SellOrders[SOrder]['V']-TradeVolume
                        TradeTime = DateTimeObject(OrderBook['date'][i],OrderBook['time'][i])
                        
                        TradePrice = SellOrders[SOrder]['P']
                        Writer.writerow([BOrder,SOrder,TradeTime,TradePrice,TradeVolume])
                        
                        #if volume has been filled, remove the order
                        if BuyOrders[BOrder]['V'] == 0:
                            del BuyOrders[BOrder]
                            BuyPrecedence.remove(BOrder)
                        if SellOrders[SOrder]['V'] == 0:
                            del SellOrders[SOrder]
                            SellPrecedence.remove(SOrder)
                        break #Breaks out of Loop 2a i.e Sell Loop
                #Loop1a
                if LCount == len(SellPrecedence):
                    Match = 0
                    break #Breaks out of Loop 1a
            elif BuyOrders[BOrder]['M']=='N':
                #Loop 1b If top Market order is a Limit Order
                #enter here
                for SOrder in SellPrecedence:
                    #Loop 2b
                    #If top Sell Order is a Market Order, then
                    #trade is initiated since our Buy Order under
                    #consideration is a limit order
                
                    if SellOrders[SOrder]['M']=='Y':

                        #Note down trade details and write to output file
                        TradeVolume = min(BuyOrders[BOrder]['V'],SellOrders[SOrder]['V'])
                        BuyOrders[BOrder]['V']=BuyOrders[BOrder]['V']-TradeVolume
                        SellOrders[SOrder]['V']=SellOrders[SOrder]['V']-TradeVolume
                        TradeTime = DateTimeObject(OrderBook['date'][i],OrderBook['time'][i])
                        TradePrice = BuyOrders[BOrder]['P']
                        Writer.writerow([BOrder,SOrder,TradeTime,TradePrice,TradeVolume])
                        
                        #if volume has been filled, remove the order
                        if BuyOrders[BOrder]['V'] == 0:
                            del BuyOrders[BOrder]
                            BuyPrecedence.remove(BOrder)
                        if SellOrders[SOrder]['V'] == 0:
                            del SellOrders[SOrder]
                            SellPrecedence.remove(SOrder)
                        break # breaks out of Loop 2b
                    if SellOrders[SOrder]['M']=='N':
                        if float(BuyOrders[BOrder]['P'])>=float(SellOrders[SOrder]['P']):
               
                            TradeVolume = min(BuyOrders[BOrder]['V'],SellOrders[SOrder]['V'])
                            BuyOrders[BOrder]['V']=BuyOrders[BOrder]['V']-TradeVolume
                            SellOrders[SOrder]['V']=SellOrders[SOrder]['V']-TradeVolume
                            TradeTime = DateTimeObject(OrderBook['date'][i],OrderBook['time'][i])
                            #FIRST ORDER IN, GETS THE PRICE:
                            #when Limit orders match from both sides
                            #the order which came in earlier, sets the price 
                            if BuyOrders[BOrder]['T']>=SellOrders[SOrder]['T']:
                                TradePrice = SellOrders[SOrder]['P']
                            else:
                                TradePrice = BuyOrders[BOrder]['P']
                            Writer.writerow([BOrder,SOrder,TradeTime,TradePrice,TradeVolume])
                            
                            #If volume has been filled, remove the orders
                            if BuyOrders[BOrder]['V'] == 0:
                                del BuyOrders[BOrder]
                                BuyPrecedence.remove(BOrder)
                            if SellOrders[SOrder]['V'] == 0:
                                del SellOrders[SOrder]
                                SellPrecedence.remove(SOrder)
                            break #breaks out of Loop 2b
                        else:
                            #There is a Bid-Ask Gap since both Top Buy
                            #and Top Sell are Limit Orders. No trade is
                            #possible until a new order comes in. Hence
                            #we use Match to break out of the while loop
                            Match = 0


        #This finally breaks the while loop to avoid
        #running into an infinite loop
        if Match == 0:
            
            break #Breaks out of while loop


# In[ ]:




