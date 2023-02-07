#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 18:38:36 2023

@author: dabanto
"""

import pyreadr
import pandas as pd
import os

def rdata_to_df(file):
    
    result = pyreadr.read_r(file)
    df = result['newtweets']
    
    return df



if __name__ == "__main__":
    print(os.getcwd())
    file = "../../files/tweets/output.RData"
    df = rdata_to_df(file)
    print(df.head())

    
    

