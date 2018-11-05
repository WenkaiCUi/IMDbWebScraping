
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from os import path
from PIL import Image
import matplotlib.image as mpimg
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from rescale_image import CreateMask


# In[2]:


df_imdb = pd.read_csv('IMDB.csv')
df_douban = pd.read_csv('douban.csv')


# In[3]:


df_imdb.head()


# The difference:
# Select different dataframe.

# In[4]:


title_both = set(df_imdb['Title'])&set(df_douban['Title'])
title_imdb = set(df_imdb['Title']) - set(df_douban['Title'])
title_douban = set(df_douban['Title']) - set(df_imdb['Title'])

mask_both = df_imdb['Title'].isin(title_both)
df_imdb_both = df_imdb[mask_both]

mask_imdb = df_imdb['Title'].isin(title_imdb)
df_imdb_only = df_imdb[mask_imdb]

mask_douban = df_imdb['Title'].isin(title_douban)
df_douban_only = df_imdb[mask_douban]


# What Genres are most popular in US and China?
# Have a look at the wordCloud!

# In[6]:


map_china = np.array(Image.open("images/China_map.png"))[:,:,3]
genres_douban = ' '.join(df_douban['Genres'].tolist()).replace(',', ' ')
mask = CreateMask(map_china)


# In[10]:


wc = WordCloud(background_color="white", max_words=1000, 
               contour_width=3, contour_color='black',collocations=False)

wc.generate(genres_douban)
plt.figure(figsize=[20,10])
plt.imshow(wc, interpolation='bilinear')
plt.axis("off")

