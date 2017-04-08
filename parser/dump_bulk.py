# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 11:46:56 2017

@author: j13-taniguchi
"""

import os
import numpy as np
import pandas as pd


T112_directly = 'C:/Users/j13-taniguchi/Desktop/git/edit_parser/parser'

os.chdir(T112_directly)

def dump_bulk(record_dict):
    '''T112のデータを受け取り、１レコード分を読み込むまで解析し、Dict型へ変換する。
    引数
       record_dict(Dict型)
         1レコードを解析した結果の下記のようなDict型
           {
              "DE002"   : 9999999999999999,
              "DE003"   : 000000,
              "DE048"   : {
                              PDS0025   : 1111,
                              PDS0158   : "   75"
                          }
              "DE57"    : 000
              
           }
    返り値
       record_str(str型)
        辞書の内容を元にbulk変換した文字列
         
    '''
    
    import sqlite3
    # 読み込んだDictionaryの内容を格納するためのrecordを宣言
    record_str = ""
    # デバック用
    #idx = 4
    
    record_str+=record_dict["MTI"]
    
    # bitmapを構築
    bitmap_primary = record_dict["bitmap_primary"]
    DE001 = record_dict["DE001"]
    str_bitmap = bitmap_primary + DE001
    
    bit_list      = [str(int(str_bitmap[i:i+4], 2)) for i in range(0,len(str_bitmap),4)]
    hex_bit_list  = ["".join(bit_list[i:i+2]).decode('hex') for i in range(0, len(bit_list), 2)]
    str_bitmap    = "".join(hex_bit_list)
    
    record_str+=str_bitmap
    
    # ビットマップをデータフレームへ展開
    #bitmap_df = pd.DataFrame(list(bitmap))
       
    # Dictionaryに登録されているキーより、DEとして登録されているもののみを取得し、リスト化
    defined_de_name_list  = [element for element in record_dict.iterkeys() if element[:2] == "DE"]

    # sqlite3を起動する
    dbname = './../sqlite3/transaction.sqlite3'
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    
    # bitmap上フラグが立っていたdata elementを1項目ずつ解析
    for defined_de_name in defined_de_name_list:
        # DE001についてはパスする。
        if defined_de_name == 'DE001':
            continue

        # SQLを発行して各data elementのバイト数、T112上にある可変長項目のバイト数指定位置を取得
        query = c.execute('select LENGTH, LENGTH_BYTE from DATA_ELEMENT_LIST where DATA_ELEMENT = (?)', (defined_de_name ,))
        for row in query:
            element_length = row[0]
            element_byte = row[1]
        # デバック
        #print('%s length : %s' % (defined_de_name, element_length))
        
        # PDS項目の解析
        if defined_de_name in ['DE048', 'DE062', 'DE123', 'DE124', 'DE125']:
            # Dictionaryに登録されているキーより、PDSとして登録されているもののみを取得し、リスト化
            defined_pds_name_list = [element for element in record_dict[defined_de_name].iterkeys()]

            #　辞書に登録されているPDSを1つずつ取り出す
            PDS_field = ""
            for idx, PDS in enumerate(defined_pds_name_list):
                # 登録されている情報よりtag、length、data情報を取得する。
                tag    = PDS[3:]
                length = str(len(record_dict[defined_de_name][PDS])).rjust(3, '0')
                data   = record_dict[defined_de_name][PDS]
                PDS_element = tag + length + data
                PDS_field+=PDS_element
                
                # デバック
                print('PDS%s length: %s data: %s' % (tag, length, data))

            # PDS fieldの頭へ設定するためのPDS_fieldの総lengthを算出
            PDS_total_length = str(len(PDS_field)).rjust(3, '0')
            PDS_total_field = PDS_total_length + PDS_field
            record_str+=PDS_total_field
                

        else:
            # DEの項目の解析
            if element_byte > 0:
                # byte数を取得 (SQLで取得したbyte数の指定位置で判断)
                moving_length = str(element_byte).rjust(element_byte, '0')
                record_str+=moving_length
            # 未定義項目以外を解析
            if element_length > 0:
                record_str+=record_dict[defined_de_name]
                # デバック
                print('%s data: %s' % (defined_de_name, record_dict[defined_de_name]))
    
    
    return record_str