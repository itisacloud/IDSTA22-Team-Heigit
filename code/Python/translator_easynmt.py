#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  2 20:06:00 2023

@author: dabanto
"""
import os
import pyreadr
import re
import nltk
nltk.download('omw-1.4')
import nltk.data
from easynmt import util, EasyNMT
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()
import pandas as pd
import numpy as np

#read rdata as a pandas dataframe
def rdata_to_df(file):
    
    result = pyreadr.read_r(file)
    df = result['df_merge']
    
    return df

file = "/pfs/data5/home/hd/hd_hd/hd_wn192/trans_inf/tweets_with_coords.RData"
df = rdata_to_df(file)
df = pd.DataFrame(df)

#preprocess tweets

def preprocess(sentence):
    sentence=str(sentence)
    sentence = sentence.lower()
    sentence=sentence.replace('{html}',"") 
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', sentence)
    rem_url=re.sub(r'http\S+', '',cleantext)
    rem_use=re.sub(r'@\w+', '', rem_url)
    rem_num = re.sub('[0-9]+', '', rem_use)
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(rem_num)  
    sent =  " ".join(tokens)
    return sent 

df['cleanText']=df.apply(lambda s:preprocess(s['text']), axis=1) 

#remove empty text cells
df['cleanText'] = df['cleanText'].replace('', np.nan)
df = df.dropna(axis=0, subset=['cleanText'])

#list languages
lst = df['lang'].value_counts()

#select tweets in a specific language (e.g. tweets in german)
res = df.loc[df['lang'] == "de"]

#convert text to list to pass it to the translator
sentences = res['cleanText'].to_list()
sentences = list(sentences)
len(sentences)


#start neural machine translation model

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

model = EasyNMT('m2m_100_418M')

#start process pool to work with the gpu
process_pool = model.start_multi_process_pool()


#define from which language you want to translate the sentences, begin with translation
translations_multi = model.translate_multi_process(process_pool, sentences, source_lang = 'de', target_lang='en', show_progress_bar=True)

#stop model
model.stop_multi_process_pool(process_pool)

#bind translated sentences to our previous dataframe
res['trans'] = pd.Series(translations_multi).values 


#save dataframe with translation as json
path_json = '/pfs/data5/home/hd/hd_hd/hd_wn192/trans_inf/tweets_de.json'
res.to_json(path_json, orient="index")




















