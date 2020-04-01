#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import datetime
TradeFile = open('PS1Data_tradebook.csv','r')
OrderFile = open('PS1Data_orderbook.csv','r')
TradeBook = csv.reader(TradeFile)
OrderBook = csv.reader(OrderFile)
OutFile = open('RecreatedTrades.csv','w')
Writer = csv.writer(OutFile)


DateTimeList = []
BorS = []
OrderNo = []
Size = []
LimitPrice = []
Mkt = []
#Column Titles
#symbol	series	date	time	orno	bors	vd	vo	lp	mkt
for row in OrderBook:
    if row[1]!='series':
        #print(row)
        year = 2006
        month = 4
        day = int(row[2][0])
        hour = int(row[3].split(':')[0])
        minute = int(row[3].split(':')[1])
        second = int(row[3].split(':')[2])
        DateTimeList.append(datetime.datetime(year,month,day,hour,minute,second))
        OrderNo.append(float(row[4]))
        BorS.append(row[5])
        Size.append(int(row[7]))
        Mkt.append(row[9])
        if row[9]=='N':
            LimitPrice.append(float(row[8]))
        else:
            LimitPrice.append(-1)


SellPrecedence = []
BuyPrecedence = []
for i in range(len(DateTimeList)):
    CurrentOrder = OrderNo[i]
    #print('\n',i)
    #print(BuyPrecedence)
    #print(SellPrecedence)
    if Mkt[i]=='N':
        ###################### LIMIT BUY  #######################
        if BorS[i]=='B':
            
            #### Check if updates are needed #########
            EntryNo = 0
            Exists = 'No'
            for entry in BuyPrecedence:
                if OrderNo[i] == entry[0]:
                    Exists = 'Yes'
                    break
                else:
                    EntryNo = EntryNo + 1
            if Exists == 'Yes':
                BuyPrecedence.pop(EntryNo)
            
            P = LimitPrice[i]
            Time = DateTimeList[i]
            
            #Find out location of new Entry
            if len(BuyPrecedence)>0:
                counter = 0
                for row in BuyPrecedence:
                    if row[1]>P:
                        #print('here')
                        counter = counter + 1
                        
                    elif row[1]==P:
                        if Time>row[2]:
                            counter = counter+1
                #if counter > 0:
                    #print(i,'Counter yes. Counter : ',counter)
                    
            #Current entry is appended to the Precedence List. The list is also updated and increased in size by 1 element
            if(len(BuyPrecedence)>0):
                
                TempPrecedence = []
                for j in range(len(BuyPrecedence)):
                    TempPrecedence.append(0)
                    TempPrecedence[j]=BuyPrecedence[j]
                
                BuyPrecedence = []
                for j in range(len(TempPrecedence)+1):
                    if j < counter:
                        BuyPrecedence.append(TempPrecedence[j])
                    elif j == counter:
                        BuyPrecedence.append([OrderNo[i],LimitPrice[i],DateTimeList[i],Size[i]])
                    elif j>counter:
                        BuyPrecedence.append(TempPrecedence[j-1])
                    
                    
                    
            elif len(BuyPrecedence) == 0:
                BuyPrecedence.append([OrderNo[i],LimitPrice[i],DateTimeList[i],Size[i]])
                
            
            
        ######################   LIMIT SELL   ######################
        elif BorS[i]=='S':
            
            EntryNo = 0
            Exists = 'No'
            for entry in SellPrecedence:
                if OrderNo[i] == entry[0]:
                    Exists = 'Yes'
                    break
                else:
                    EntryNo = EntryNo + 1
            if Exists == 'Yes':
                SellPrecedence.pop(EntryNo)
            
            
            
            P = LimitPrice[i]
            Time = DateTimeList[i]
            # To find the index where the current entry is to be added
            if len(SellPrecedence)>0:
                counter = 0
                for row in SellPrecedence:
                    if row[1]<P:
                        counter = counter + 1
                    elif row[1]==P:
                        if Time>row[2]:
                            counter = counter+1
                    
            #Current entry is appended to the Precedence List. The list is also updated and increased in size by 1 element
            if(len(SellPrecedence)>0):              
                TempPrecedence = []
                for j in range(len(SellPrecedence)):
                    TempPrecedence.append(0)
                    TempPrecedence[j]=SellPrecedence[j]
                SellPrecedence = []
                for j in range(len(TempPrecedence)+1):
                    if j < counter:
                        SellPrecedence.append(TempPrecedence[j])
                    elif j == counter:
                        SellPrecedence.append([OrderNo[i],LimitPrice[i],DateTimeList[i],Size[i]])
                    elif j>counter:
                        SellPrecedence.append(TempPrecedence[j-1])
            elif len(SellPrecedence) == 0:
                SellPrecedence.append([OrderNo[i],LimitPrice[i],DateTimeList[i],Size[i]])
            ###################     CHECK FOR TRADES         ################
        if len(SellPrecedence)>0:
            if len(BuyPrecedence)>0:
                while BuyPrecedence[0][1]>=SellPrecedence[0][1]:
                    
                    print('\n',i,'Matching Trade Found')
                    #print(SellPrecedence)
                  
                    if BuyPrecedence[0][3]>SellPrecedence[0][3]:
                        Volume = SellPrecedence[0][3]
                    elif BuyPrecedence[0][3]<=SellPrecedence[0][3]:
                        Volume = BuyPrecedence[0][3]
                    
                    #print(BuyPrecedence[0][1],BuyPrecedence[0][2],SellPrecedence[0][1],SellPrecedence [0][2])
                    if BuyPrecedence[0][2] >= SellPrecedence [0][2]:
                        TrPrice = SellPrecedence[0][1]
                    elif BuyPrecedence[0][2]<SellPrecedence[0][2]:
                        TrPrice = BuyPrecedence[0][1]
        
                    print('Time : ',DateTimeList[i])
                    print('Price :',TrPrice)
                    print('Volume :',Volume)
                    print('BuyOrder No :',BuyPrecedence[0][0])
                    print('SellOrder No : ',SellPrecedence[0][0])
                    
                    Writer.writerow([DateTimeList[i],TrPrice,Volume,BuyPrecedence[0][0],SellPrecedence[0][0]])
                
                # Update Buy and Sell Precedence Lists
                
                #Buy List
                
                    BuyPrecedence[0][3] = BuyPrecedence[0][3]-Volume
                #Order Size has been completely filled out. Erase from List. Make a deep copy of new List
                    if BuyPrecedence[0][3]<=0:
                        BuyPrecedence.pop(0)
                       
                    #Sell List
                    SellPrecedence[0][3] = SellPrecedence[0][3]-Volume
                #Order Size has been completely filled out. Erase from List. Make a deep copy of new List
                    if SellPrecedence[0][3]<=0:
                        SellPrecedence.pop(0)
                      
    elif Mkt[i]=='Y':
        CurrentOrder = OrderNo[i]
        ##################    MARKET BUYS ###################
        
        if BorS[i]=='B':
            Target = Size[i]
            Available = SellPrecedence[0][3]
            
            
            while Target > 0:
                Volume = min(Target,Available)
                TrPrice = SellPrecedence[0][1]
                print('\nMarket Buy')
                print('Time : ',DateTimeList[i])
                print('Price :',TrPrice)
                print('Volume :',Volume)
                print('BuyOrder No :',OrderNo[i])
                print('SellOrder No : ',SellPrecedence[0][0])
                Writer.writerow([DateTimeList[i],TrPrice,Volume,OrderNo[i],SellPrecedence[0][0]])

                if Target > Available:
                    Target = Target - Available
                    SellPrecedence[0][3] = 0
                elif Target < Available:
                    Target = 0
                    SellPrecedence[0][3] = Available - Target
                elif Target == Available:
                    Target = 0
                    SellPrecedence[0][3] = 0
            
                if SellPrecedence[0][3]<=0:
                    Temp = []
                    for k in range(1,len(SellPrecedence)):
                        Temp.append([])
                        Temp[k-1]=SellPrecedence[k]
                    SellPrecedence=[]
                    for item in Temp:
                        SellPrecedence.append(item)
            

            
        ################ Market Sells ###########   
        elif BorS[i]=='S':
            Target = Size[i]
            Available = BuyPrecedence[0][3]
            while Target > 0:
                Volume = min(Target,Available)
                TrPrice = BuyPrecedence[0][1]
                
                
                print('\nMarket Sell')
                print('Time : ',DateTimeList[i])
                print('Price :',TrPrice)
                print('Volume :',Volume)
                print('BuyOrder No :',BuyPrecedence[0][0])
                print('SellOrder No : ',OrderNo[i])
                Writer.writerow([DateTimeList[i],TrPrice,Volume,BuyPrecedence[0][0],OrderNo[i]])
                if Target > Available:
                    Target = Target - Available
                    BuyPrecedence[0][3] = 0
                elif Target < Available:
                    Target = 0
                    BuyPrecedence[0][3] = Available - Target
                elif Target == Available:
                    Target = 0
                    BuyPrecedence[0][3] = 0
            
                if BuyPrecedence[0][3]<=0:
                    Temp = []
                    for k in range(1,len(BuyPrecedence)):
                        Temp.append([])
                        Temp[k-1]=BuyPrecedence[k]
                    BuyPrecedence=[]
                    for item in Temp:
                        BuyPrecedence.append(item)


# In[ ]:




