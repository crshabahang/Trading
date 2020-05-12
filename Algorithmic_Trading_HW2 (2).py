#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Author: Cameron R. Shabahang
#1) Suppose you want to submit an order of 10000 shares to buy for each trading day
#Describe various algorithms: VWAP, TWAP, POV, IS
#Decompose the IS order for various components
#2) Do the same for 10000 orders to sell
#3) For each order, estimate the probability of execution
#4) Using tradebook and Huang and Stoll (1997), replicate results

#Import packages
import numpy as np
import pandas as pd
import datetime as dt
#Read data
orderbook = pd.read_excel('PS1Data_orderbook.xlsx')
tradebook = pd.read_excel('PS1Data_tradebook.xlsx')

#Return if bno or sno is equal to orno for market orders
def get_mkt_buy(X):
    if len(tradebook[tradebook.bno==X.orno])>0:
        return tradebook[trade_book.bno==X.orno].iloc[0]
def get_mkt_sell(X):
    if len(tradebook[tradebook.sno==X.orno])>0:
        return tradebook[tradebook.sno==X.orno].iloc[0]
#Return if tradebook orno is same as bno or sno for limit orders
def get_limit_sell(X):
    return orderbook[data.orno==X.sno].iloc[-1]
def get_limit_buy(X):
    return orderbook[data.orno==X.bno].iloc[-1]

#Apply the limit order functions on the limit price
trade_book['buy_p'] = tradebook.apply(get_limit_buy,axis = 1).lp
trade_book['sell_p'] = tradebook.apply(get_limit_sell,axis = 1).lp

data.loc[(data.bors=='B')&(data.mkt=='Y'),'lp']=data[(data.bors=='B')&(data.mkt=='Y')].apply(get_mkt_buy, axis = 1).lp
data.loc[(data.bors=='S')&(data.mkt=='Y'),'lp']=data[(data.bors=='S')&(data.mkt=='Y')].apply(get_mkt_sell, axis = 1).lp

orderbook = data.dropna().reset_index(drop = True)
tradebook = tradebook.dropna().reset_index(drop = True)

#TWAP for buys
def buy_algo1(X):
    X['hour'] = X.time.apply(lambda X: X.strftime('%H'))
    length = len(X.hour.unique())-1
    Y = X[(X.hour!=X.hour.iloc[0])&(X.buy_p>=X.sell_p)].groupby('hour').apply(lambda M:
    #Fill code above
    return Y

#VWAP for buys                                                                          
def buy_algo2(X):
    X['hour'] = X.time.apply(lambda X: X.strftime('%H'))
    length = len(X.hour.unique())-1
    Y = X[(X.hour!=X.hour.iloc[0])&(X.buy_p>=X.sell_p)].groupby('hour').apply(lambda M:
    #Fill code above
    return 10000*(Y/Y.sum())

#TWAP for sells
def sell_algo1(X):
    X['hour'] = X.time.apply(lambda X: X.strftime('%H'))
    length = len(X.hour.unique())-1
    Y = X[(X.hour!=X.hour.iloc[0])&(X.buy_p<=X.sell_p)].groupby('hour').apply(lambda M:
    #Fill code above
    return Y

#VWAP for sells
def sell_algo2(X):
    X['hour'] = X.time.apply(lambda X: X.strftime('%H'))
    length = len(X.hour.unique())-1
    Y = X[(X.hour!=X.hour.iloc[0])&(X.buy_p<=X.sell_p)].groupby('hour').apply(lambda M:
    #Fill code above
    return 10000*(Y/Y.sum())

#Buy 10000 shares a day
buy1 = pd.DataFrame({'price':trade_book.groupby('date').apply(buy_algo1).applymap(lambd buy1.head()
buy2 = pd.DataFrame({'price':trade_book.groupby('date').apply(buy_algo1).applymap(lambd 'quantity':trade_book.groupby('date').apply(buy_algo2).applymap(np.round)
buy2.head()

#TWAP is time weighted average price of each day VWAP is volume weighted average price of each day
#IS is benchmark of implementation shortfall, which is price of first trade after 10am
Benchmark = pd.DataFrame({'TWAP':trade_book.groupby('date').apply(lambda X:X.p.mean()), 'VWAP':trade_book.groupby('date').apply(lambda X:(X.p*X.vol).s 'IS':trade_book.groupby('date').apply(lambda Y:Y.loc[Y.time.ap
Benchmark

#Execution Cost of Algo 1(Equally weighted)
cost1 = pd.merge(buy1,Benchmark,on='date')
Cost_ans = pd.DataFrame({'TWAP':cost1.groupby('date').apply(lambda X: ((X.price-X.TWAP)
'VWAP':cost1.groupby('date').apply(lambda X: ((X.price-X.VWAP)
'IS':cost1.groupby('date').apply(lambda X: ((X.price-X.IS)*X.q
Cost_ans

#Execution Cost of Algo 1(Volume weighted)
cost2 = pd.merge(buy2,Benchmark,on='date')
Cost_ans2 = pd.DataFrame({'TWAP':cost2.groupby('date').apply(lambda X: ((X.price-X.TWAP
'VWAP':cost2.groupby('date').apply(lambda X: ((X.price-X.VWAP)
'IS':cost2.groupby('date').apply(lambda X: ((X.price-X.IS)*X.
                                            
#Sell 10000 shares a day
sell1 = pd.DataFrame({'price':trade_book.groupby('date').apply(sell_algo1).applymap(lam sell2 = pd.DataFrame({'price':trade_book.groupby('date').apply(sell_algo1).applymap(lam 'quantity':trade_book.groupby('date').apply(sell_algo2).applymap(np.round
#Execution cost analysis
cost_s1 = pd.merge(sell1,Benchmark,on='date')
Cost_ans_s1 = pd.DataFrame({'TWAP':cost_s1.groupby('date').apply(lambda X: ((-X.price+X
'VWAP':cost_s1.groupby('date').apply(lambda X: ((-X.price+X.VW
'IS':cost_s1.groupby('date').apply(lambda X: ((-X.price+X.IS)*Cost_ans_s1
cost_s2 = pd.merge(sell2,Benchmark,on='date')
Cost_ans_s2 = pd.DataFrame({'TWAP':cost_s2.groupby('date').apply(lambda X: ((-X.price+X
'VWAP':cost_s2.groupby('date').apply(lambda X: ((-X.price+X.VW
'IS':cost_s2.groupby('date').apply(lambda X: ((-X.price+X.IS)*
Cost_ans_s2


orno = set(trade_book.bno.values)|set(trade_book.sno.values)
data['trade_status'] = data.orno.apply(lambda X: 1 if X in orno else 0)
data['hidden_sign'] = 1*(data.vo>data.vd)
data['date_time'] = data.apply(lambda X: dt.datetime.combine(X.date,X.time),axis = 1)
trade_book['date_time'] = trade_book.apply(lambda X: dt.datetime.combine(X.date,X.time)
data['delta_time'] = (data.date_time-data.date_time[0]).apply(lambda X: X.total_seconds
trade_book['delta_time'] = (trade_book.date_time-data.date_time[0]).apply(lambda X: X.t


def cal_vwap(M):
    if len(M)==0:
        return np.nan
    else:
        return (M.vol*M.p).sum()/M.vol.sum()
data['vwap_5min'] = data.apply(lambda X: cal_vwap(trade_book[(trade_book.delta_time<X.d

def cal_volume(M):
    if len(M)==0:
        return np.nan
    else:
        return M.vol.sum()
data['volume_5min'] = data.apply(lambda X: cal_volume(trade_book[(trade_book.delta_time


data['price_diff'] = (data.bors=='B')*(data.lp-data.vwap_5min)-(data.bors=='S')*(data.l
data = data.dropna().reset_index(drop =True)

import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import plot_roc_curve

#Using decision tree and random forest classifier to train model
X = data[['vo','hidden_sign','volume_5min','price_diff']].values
y = data[['trade_status']].values
 
enc = OneHotEncoder()
enc.fit(y)
y_ = enc.transform(y).toarray()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=4
clf = DecisionTreeClassifier()
y_score = clf.fit(X_train, y_train).decision_path(X_test)
tree1= clf.fit(X_train,y_train)
tree1.score(X_test, y_test)
cross_val_score(tree1,X_train, y_train,cv=3)
array([0.61043467, 0.61188569, 0.62097029])

#AUC_ROC Curve
clf_disp = plot_roc_curve(tree1, X_test, y_test)
rfc = RandomForestClassifier(n_estimators=10, random_state=42)
rfc.fit(X_train, y_train.ravel())
ax = plt.gca()
rfc_disp = plot_roc_curve(rfc, X_test, y_test, ax=ax, alpha=0.8)
clf_disp.plot(ax=ax, alpha=0.8
plt.show()

