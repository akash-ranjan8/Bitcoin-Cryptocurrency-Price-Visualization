#!/usr/bin/env python
# coding: utf-8

# In[4]:


import os
import numpy as np
import pickle
import quandl
import pandas as pd
import plotly.offline as py
import plotly.graph_objs as go
py.init_notebook_mode(connected=True)


# In[5]:


quandl.ApiConfig.api_key = 'tWWv7RoNKzyaxKKRnc8d'


# In[10]:


def get_quandl_data(quandl_code):
  cache_path = '{}.pkl'.format(quandl_code).replace('/','-')
  try:
    f = open(cache_path,'rb')
    df = pickle.load(f)
    print('Loaded {} from cache'.format(quandl_code))
  except (OSError,IOError) as e:
    df=quandl.get(quandl_code,returns="pandas")
    df.to_pickle(cache_path)
    print('Cached {} at {}').format(quandl_code,cache_path)
  return df


# In[11]:


btc_usd_kraken = get_quandl_data('BCHARTS/KRAKENUSD')


# In[12]:


btc_usd_kraken.head()


# In[13]:


btc_trace = go.Scatter(x=btc_usd_kraken.index,y=btc_usd_kraken['Weighted Price'])
py.iplot([btc_trace])


# In[18]:


exchanges = ['COINBASE','BITSTAMP','ITBIT']
exchange_data = {}
exchange_data['KRAKEN'] = btc_usd_kraken
for exchange in exchanges:
    exchange_code = 'BCHARTS/{}USD'.format(exchange)
    btc_exchange_df = get_quandl_data(exchange_code)
    exchange_data[exchange] = btc_exchange_df


# In[19]:


exchange_data


# In[20]:


def merge_dfs(dataframes, labels,col):
    series_dict = {}
    
    for index in range(len(dataframes)):
        series_dict[labels[index]] = dataframes[index][col]
    return pd.DataFrame(series_dict)


# In[21]:


btc_usd_df = merge_dfs(list(exchange_data.values()),list(exchange_data.keys()), 'Weighted Price')


# In[22]:


btc_usd_df.head()


# In[29]:


layout = go.Layout(
    title = 'Bitcoin Price By Exchange (USD)',
    legend = {'orientation':'h'},
    xaxis = {'type':'date'},
    yaxis = {'title':'Price in USD'}
)
trace_arr = []
labels = list(btc_usd_df)
for index,label in enumerate(labels):
    series = btc_usd_df[label]
    trace = go.Scatter(x=series.index, y=series, name=label)
    trace_arr.append(trace)

fig = go.Figure(data=trace_arr, layout=layout)
py.iplot(fig)


# In[30]:


btc_usd_df['avg_usd_price'] = btc_usd_df.mean(axis=1)
btc_trace = go.Scatter(x=btc_usd_df.index, y=btc_usd_df['avg_usd_price'])
py.iplot([btc_trace])

