#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 18:38:36 2023

@author: dabanto
"""

import pyreadr
import pandas as pd


def rdata_to_df(file):
    
    result = pyreadr.read_r(file)
    df = result['newtweets']
    
    return df


file = "/Users/dabanto/Desktop/out_tweets_ukr/json_output/output.RData"

df = rdata_to_df(file)
