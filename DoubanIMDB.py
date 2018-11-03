# -*- coding: utf-8 -*-
"""

@author: Wenkai Cui
@email: wkcui@bu.edu
Created on Fri Jul 13 16:14:18 2018

"""


import time
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from download import myrequest
import re

def GetHTML(url):
    res=myrequest.get(url)
    if res.status_code==200:        
        soup= BeautifulSoup(res.text,'lxml')
        print('Successfully Getting URL')
        return soup

    print(res.status_code)
    print('Error!!!!!')
    return None

def _Director(res_IMDB):
    try:
        ind = [i for i,j in enumerate(res_IMDB.select('.credit_summary_item h4.inline')) if 'Director' in j.string][0]
        directors = res_IMDB.select('.credit_summary_item h4.inline')[ind].parent.select('a')
        return ','.join([i.string for i in directors])
    except ValueError:
        return np.nan
    
    # sub function to find first 3 stars:
def _Stars(res_IMDB):
    try:
        ind = [i.h4.string for i in res_IMDB.select('.credit_summary_item')].index('Stars:')
        stars = res_IMDB.select('.credit_summary_item')[ind].select('a')[:3]
        return ','.join([i.string for i in stars])
    except ValueError:
        return np.nan

def _Genres(res_IMDB):
    try:
        ind = [i.string for i in res_IMDB.select('.see-more.inline.canwrap h4.inline')].index('Genres:')
        genres= res_IMDB.select('.see-more.inline.canwrap h4.inline')[ind].parent.select('a')
        return ','.join([i.string for i in genres])
    except ValueError:
        return np.nan

def _Countries(res_IMDB):
    try:
        ind =[i for i,j in enumerate(res_IMDB.select('#titleDetails .txt-block h4.inline')) if 'Countr' in j.string][0]
        countries = res_IMDB.select('#titleDetails .txt-block h4.inline')[ind].parent.select('a')
        return ','.join([i.string for i in countries])
    except ValueError:
        return np.nan

def _Runtime(res_IMDB):
    try:
        ind =[i.string for i in res_IMDB.select('#titleDetails .txt-block h4.inline')].index('Runtime:')
        runtime = res_IMDB.select('#titleDetails .txt-block h4.inline')[ind].find_next('time').string
        return int(runtime.rstrip(' min'))
    except ValueError:
        return np.nan   

def _Budget(res_IMDB):
    try:
        ind = [i.string for i in res_IMDB.select('#titleDetails .txt-block h4.inline')].index('Budget:')
        strs = [i for i in res_IMDB.select('#titleDetails .txt-block h4.inline')[ind].parent.children if isinstance(i,str)]
        budget = [i for i in strs if re.search('[0-9]',i)][0].strip().replace(',','').replace('\xa0','')
        return budget
    except ValueError:
        return np.nan

def _Boxoffice(res_IMDB):
    try:
        ind = [i.string for i in res_IMDB.select('#titleDetails .txt-block h4.inline')].index('Cumulative Worldwide Gross:')
        strs = [i for i in res_IMDB.select('#titleDetails .txt-block h4.inline')[ind].parent.children if isinstance(i,str)]
        boxoffice = [i for i in strs if re.search('[0-9]',i)][0].strip().replace(',','').replace('\xa0','')
        return boxoffice
    except ValueError:
        return np.nan



def GetDoubanInfo(url_douban):
    res_douban=GetHTML(url_douban)
#    if res_douban is None:
#        print('Response is None')
#        return None
    
    url_IMDB= [i for i in res_douban.select('#info .pl') if 'IMDb' in i.string][0].find_next('a').attrs['href']
    res_IMDB = GetHTML(url_IMDB)
    # parsing and store info
    movieinfo={'Title' : list(res_IMDB.select('.title_wrapper h1')[0].children)[0].rstrip('\xa0'), 
        'ReleaseYear': int(res_IMDB.find_all(attrs={'class':'title_wrapper'})[0].h1.span.a.string),
        'Director': _Director(res_IMDB),
        'Stars':_Stars(res_IMDB),
        'Genres': _Genres(res_IMDB),
        'Countries':_Countries(res_IMDB),
        'Runtime': _Runtime(res_IMDB),
        'Rating': float(res_douban.find_all(attrs={'property':'v:average'})[0].string),
        'Rating_Per': ','.join([i.string for i in res_douban.find_all(attrs={'class':'rating_per'})]),
        'Budget($)': _Budget(res_IMDB),
        'BoxOffice($)': _Boxoffice(res_IMDB)
        }  # rating_per from 5 to 1  
    return movieinfo

def GetDoubanMovieURL(res):
    # get all movie url on a content page
    url=[res.select('#content .grid_view li .hd a')[i]['href'] for i in range(25)]
    return url


if __name__ == '__main__':

    InfoLst = []
    for i in range(10):
        print('Scrapping page %d'%i)
        url="https://movie.douban.com/top250?start={0}".format(i*25)
        res=GetHTML(url)
        urls=GetDoubanMovieURL(res)
        for j in range(len(urls)):
            time.sleep(np.random.uniform(1,2))
            print('Number %d in the page'%j)
            MovieInfo=GetDoubanInfo(urls[j])
            print(MovieInfo)
            InfoLst.append(MovieInfo)

    df = pd.DataFrame(InfoLst)
    df.to_csv('Douban.csv',index=False,encoding='utf-8')
