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
    '''T112のデータを受け取り、１レコード分を読み込むまで解析し、Dict型へ変換する。
    引数
       T112_data(str型)
         T112のデータ
       idx(int型)
         T11の現在読み込んでいる位置を表すポインタ
    返り値
       parsed_dict(Dict型)
         1レコードを解析した結果の下記のようなDict型
           {
              "DE002"   : 9999999999999999,
              "DE003"   : 000000,
              "PDS0158" : XXXX75,
              "DE57"    : 000
              
           }
       idx(int型)
       　　現在のポイントの位置を返す
         
    '''
    
    import sqlite3
    # 読み込んだレコードの内容を格納するためのDictionaryを宣言
    parsed_dict = {}
    # デバック用
    idx = 4
    # Bitmap Primary 及び　DE001を解析
    parsed_dict["MTI"] = T112_data[idx:idx+4]
    print("MTI :%s" % T112_data[idx:idx+4])
    hexmap = T112_data[idx+4:idx+20].encode('hex')
    bitmap = ""
    for hex in hexmap:
        # hexを16進数へ変換し、bitへさらに変換する。
        bit = bin(int(hex, 16))
        # bit変換により先頭2桁へ邪魔な文字がつくため、切り捨てる。
        bit = bit[2:]
        bit = bit.rjust(4,'0')
        bitmap+=bit

    # ビットマップをデータフレームへ展開
    #bitmap_df = pd.DataFrame(list(bitmap))
    
    # bitmap_primary と bitmap_secondaryをparsed_dictへ格納
    parsed_dict["bitmap_primary"] = bitmap[:64]
    parsed_dict["DE001"] = bitmap[64:]
    
    # bitmap上で1が立っているもののみを抽出。
    # 要素とData Elementでは開始の番号が異なる（要素は0番、DEは1)ので、合わせるためにi+1でリストへ追加）
    element_list = []
    for i, element in enumerate(bitmap):
        if element == '1':
            element_list.append(i+1)
    defined_de_name_list = ["DE" + str(i).rjust(3, '0') for i in element_list]
    idx+=20

    # sqlite3を起動する
    dbname = './sqlite3/transaction.sqlite3'
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    
    
    # bitmap上フラグが立っていたdata elementを1項目ずつ解析
    for defined_de_name in defined_de_name_list:
        # DE001については解析済みのため、パスする。
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
            # PDS項目の解析
            # Additional Areaの最大byte数を取得
            PDS_field = T112_data[idx:idx+3]
            idx+=3
            # Additional Areaの現在位置を指定
            PDS_idx = 0
            # PDS_idxが最大byte数を超えるまで繰り返す
            while PDS_idx < int(PDS_field):
                # PDSの解析 tagを取得
                tag = T112_data[idx:idx+4]
                idx+=4
                PDS_idx+=4
                # PDSの解析 lengthを取得
                length = T112_data[idx:idx+3]
                idx+=3
                PDS_idx+=3
                # PDSの解析 dataを取得
                data = T112_data[idx:idx+int(length)]
                idx+=int(length)
                PDS_idx+=int(length)
                # parsed_dictへ解析された値を登録
                parsed_dict["PDS" + tag] = data
                # デバック
                print('PDS%s length: %s data: %s' % (tag, length, data))
                print('PDS_idx = %s' % PDS_idx)

        else:
            # DEの項目の解析
            if element_byte > 0:
                # byte数を取得 (SQLで取得したbyte数の指定位置で判断)
                element_length_str = T112_data[idx:idx+element_byte]
                element_length = int(element_length_str)
                idx+=element_byte

            # 未定義項目以外を解析
            if element_length > 0:
                data = T112_data[idx:idx+element_length]
                idx+=element_length
                parsed_dict[defined_de_name] = data
                # デバック
                print('%s length : %s data: %s' % (defined_de_name, element_length, data))
    
    
    
    
    return idx, parsed_dict