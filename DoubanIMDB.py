# -*- coding: utf-8 -*-
"""

@author: Wenkai Cui
@email: wkcui@bu.edu
Created on Fri Jul 13 16:14:18 2018

"""

import json
import os
import time
import requests
import urllib
import re
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import random
from download import myrequest
        
def GetHTML(url):
    res=myrequest.get(url,3)
    if res.status_code==200:        
        soup= BeautifulSoup(res.text,'lxml')
        print('Successfully Getting URL')
        return soup

    print(res.status_code)
    return None

   
def GetMovieInfo(suburl):
    subres=GetHTML(suburl)
    if subres is None:
        print('Response is None')
        return None
    movieinfo={'IMDBLink': subres.select('#content h1 span')[0].string,
     'Director': ','.join([i.string for i in subres.find_all(attrs={'rel':'v:directedBy'})]),#'screenwriter': ','.join([i.string for i in subres.find_all(attrs={'class':'attrs'})[1].select('a')]),
     'Genre': ','.join([i.string for i in subres.find_all(attrs={'property':'v:genre'})]),
     'Country': re.findall('制片国家/地区:</span>(.*?)<br/>',str(subres.find_all(attrs={'id':'info'})[0]),re.S)[0].strip(),
     'Language':re.findall('语言:</span>(.*?)<br/>',str(subres.find_all(attrs={'id':'info'})[0]),re.S)[0].strip(),
     'Rating': subres.find_all(attrs={'property':'v:average'})[0].string,
     'Runtime': subres.find_all(attrs={'property':'v:runtime'})[0].string
     }
    return movieinfo

def GetMovieURL(res):
    # get all movie url on a content page
    url=[res.select('#content .grid_view li .hd a')[i]['href'] for i in range(25)]
    return url



url='https://movie.douban.com/top250'

df=pd.DataFrame()
for i in range(10):
    print('Scrapping page %d'%i)
    url="https://movie.douban.com/top250?start={0}".format(i*25)
    res=getHTML(url)
    urls=GetMovieURL(res)
    for j in range(len(urls)):
        print('j = %d'%j)
        MovieInfo=GetMovieInfo(urls[j])
        if MovieInfo is None:
            continue
        print(MovieInfo)
        df=df.append(MovieInfo,ignore_index=True)

df.to_csv('Douban.csv',index=False,encoding='utf-8')






















