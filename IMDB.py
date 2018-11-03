# -*- coding: utf-8 -*-
"""

@author: Wenkai Cui
@email: wkcui@bu.edu
Created on Fri Jul 13 16:14:18 2018

"""

import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from download import myrequest
import DoubanIMDB as D

def GetIMDBURL(res):
    urls = ['https://www.imdb.com' + i.attrs['href'] for i in res.select('.lister-list .titleColumn a')]
    return urls

def GetIMDBInfo(url_movie):
    res_IMDB=D.GetHTML(url_movie)
    url_rating_page = 'https://www.imdb.com'+res_IMDB.select('.ratings_wrapper .imdbRating a')[0].attrs['href']
    res_rating_page = D.GetHTML(url_rating_page)
    
    def _rating_per_IMDB(res_rating_page): 
        select = res_rating_page.select('.title-ratings-sub-page table[cellpadding="0"] .allText .topAligned')
        return ','.join([i.string.strip() for i in select])
    
    movieinfo={'Title' : list(res_IMDB.select('.title_wrapper h1')[0].children)[0].rstrip('\xa0'), 
        'ReleaseYear': int(res_IMDB.find_all(attrs={'class':'title_wrapper'})[0].h1.span.a.string),
        'Director': D._Director(res_IMDB),
        'Stars':D._Stars(res_IMDB),
        'Genres': D._Genres(res_IMDB),
        'Countries':D._Countries(res_IMDB),
        'Runtime': D._Runtime(res_IMDB),
        'Rating': res_IMDB.select('.ratings_wrapper .ratingValue strong span')[0].string,
        'Rating_Per': _rating_per_IMDB(res_rating_page),
        'Budget($)': D._Budget(res_IMDB),
        'BoxOffice($)': D._Boxoffice(res_IMDB)
    }
    return movieinfo

if __name__ == '__main__':
    
    InfoLst = []
    url="https://www.imdb.com/chart/top?ref_=nv_mv_250"
    res=D.GetHTML(url)
    urls=GetIMDBURL(res)
    for i in range(len(urls)):
        time.sleep(np.random.uniform(1,2))
        print('Number %d in the page'%i)
        MovieInfo=GetIMDBInfo(urls[i])
        print(MovieInfo)
        InfoLst.append(MovieInfo)

    df = pd.DataFrame(InfoLst)
    df.to_csv('IMDB.csv',index=False,encoding='utf-8')


