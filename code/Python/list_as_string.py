#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 14:41:22 2022

This script prepares a set of words so that it can be sent as a query to fetch tweets

@author: dabanto
"""

import pandas as pd

#fetch words from a list that has been already prepared
url = "https://raw.githubusercontent.com/echen102/ukraine-russia/master/keywords.txt"

#read url using pandas 
df = pd.read_csv(url, delim_whitespace=True, header=None)


#convert values to list
lst = df[0].values.tolist()

#convert list to string
s = str(lst)

#replace commas with OR
s = s.replace(',', ' OR')


#add double brackets
str(s).replace("'", '"')

#now we can pass the string to academictwitteR 