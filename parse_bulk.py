# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 11:46:56 2017

@author: j13-taniguchi
"""

import os
import numpy as np
import pandas as pd


#T112_directly = 'C:/Users/j13-taniguchi/Desktop/git/edit_parser'
T112_directly = 'C:/Users/JunTaniguchi/Desktop/git/edit_parser'

os.chdir(T112_directly)

def parse_bulk(T112_data, idx):
    import sqlite3
    # 読み込んだレコードの内容をDictionaryへ格納
    record = {}

    # Bitmap Primary 及び　DE001についてを解析
    hexmap = T112_data[idx+4:idx+20].encode('hex')
    bitmap = "0"
    for hex in hexmap:
        # hexを16進数へ変換し、bitへさらに変換する。
        bit = bin(int(hex, 16))
        # bit変換により先頭2桁へ邪魔な文字がつくため、切り捨てる。
        bit = bit[2:]
        bit = bit.rjust(4,'0')
        bitmap+=bit
    
    # bitmap_primary と bitmap_secondaryをrecordへ格納
    record["bitmap_primary"] = bitmap[:64]
    record["DE001"] = bitmap[64:]
    
    # bitmap上で1が立っているもののみを抽出。
    element_list = []
    for i, element in enumerate(bitmap):
        if element == '1':
            element_list.append(i)

    idx+=20

    # sqlite3を起動する
    dbname = './sqlite3/transaction.sqlite3'
    #database=sqlite3.connect(dbname,isolation_level=None)		# オートコミットを有効に指定
    
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    sql = 'select LENGTH from DATA_ELEMENT_LIST where DATA_ELEMENT = (?)'
    
    defined_de_name_list = ["DE" + str(i).rjust(3, '0') for i in element_list]
    for defined_de_name in defined_de_name_list:
        if defined_de_name == 'DE001':
            continue

        # SQLを発行して各elementのレンジを取得
        query = c.execute(sql, (defined_de_name ,))
        for row in query:
            element_length = row[0]
        
        if defined_de_name in ['DE048', 'DE062', 'DE123', 'DE124', 'DE125']:
            tag = 0
            while T112_data[idx:idx+4] > tag:
                # PDSの解析 tag、length、dataを取得
                tag = T112_data[idx:idx+4]
                idx+=4
                length = T112_data[idx:idx+2]
                idx+=2
                data = T112_data[idx:idx+len(length)]
                idx+=len(length)
                record["PDS" + tag] = data
        else:
            data = T112_data[idx:idx+element_length]
            idx+=element_length
            if element_length > 0:
                record[defined_de_name] = data
    
    return idx, record