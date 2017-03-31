# -*- coding: sjis -*-
"""
Created on Fri Mar 31 11:46:56 2017

@author: j13-taniguchi
"""

import os
import numpy as np
import pandas as pd
import sqlite3

dbname = './sqlite3/transaction.sqlite3'

conn = sqlite3.connect(dbname)
c = conn.cursor()

T112_directly = u'C:\\Users\\j13-taniguchi\\Desktop\\git\\edit_parser'

os.chdir(T112_directly)

def parse_bulk(T112_data, idx, element_list):
    record = {}
    # sqlite3を起動する
    database=sqlite3.connect("test.sqlite3",isolation_level=None)		# オートコミットを有効に指定
    sql = 'select LENGTH, from DATA_ELEMENTS where DATA_ELEMENT = (?)'
    
    defined_de_name_list = ["DE" + str(i).rjust(3, '0') for i in element_list]
    for defined_de_name in defined_de_name_list:
        # SQLを発行して各elementのレンジを取得
        element_length = c.execute(sql, defined_de_name)
        
        element_object = T112_data[idx:idx+element_length]
        idx += element_length
        record[defined_de_name] = element_object
        