import pandas as pd
from pytrends.request import TrendReq

#create model
pytrend = TrendReq()

#provide your search terms
kw_list=['Nike', 'Adidas']

#set timeframe to last year in 1-week intervals
timeframe = 'now 1-y'

#get interest by region for your search terms
pytrend.build_payload(kw_list=kw_list, timeframe=timeframe, geo='', gprop='')
df = pytrend.interest_over_time()

df.head(10)
