# -*- coding: utf-8 -*-
"""
Spyderエディタ

これは一時的なスクリプトファイルです
"""

import os
import numpy as np
import pandas as pd

T112_directly = u'C:\\Users\\j13-taniguchi\\Desktop\\git\\edit_parser'

os.chdir(T112_directly)

# レイアウト情報ファイルの内容をロード
df_transaction_category = pd.read_csv('M_LAYOUT_INFO_No1.csv', 
                                      encoding='Shift_JIS')

df_layout_category = pd.read_csv('M_LAYOUT_INFO_No2.csv', 
                                 encoding='Shift_JIS')

# T112のデータの取り込み
with open('TT112T0.001', 'r') as T112_file:
    T112_data = T112_file.read()

transaction_MTI = ['1644','1740','1240','1442']
for idx, t in enumerate(T112_data):
    # 現在の添え字番号から4桁がMTIの値になっているかを確認
    MTI = T112_data[idx:idx+4]
    if MTI in transaction_MTI:
        # ビットマップを解析
        hexmap = T112_data[idx+4:idx+20].encode('hex')
        bitmap = ""
        for hex in hexmap:
            bit = bin(int(hex))
            bit = bit[2:]
            bit = bit.rjust(4,'0')
            bitmap+=bit
        # ビットマップをデータフレームへ展開
        pd.DataFrame(list(bitmap))
        # トランザクション毎に処理を分ける
        if MTI == '1644':
            df_transaction1644 = df_transaction_category[df_transaction_category['FORMAT-MTI'] == 1644]
  
            # 1644-697の確認
            DE24 = T112_data[idx+20:idx+23]
            if DE24 == '697':
                df_transaction1644_697 = df_transaction1644[df_transaction1644['FORMAT-FC'] == 697]
                # 編集処理
                
            # 1644-603の確認
            DE24 = T112_data[idx+64:idx+67]
            if DE24 == '603':
                df_transaction1644_603 = df_transaction1644[df_transaction1644['FORMAT-FC'] == 603]
                # 編集処理
             
            # 1644-685の確認
            DE24 = T112_data[idx+20:idx+23]
            if DE24 == '685':
                df_transaction1644_685 = df_transaction1644[df_transaction1644['FORMAT-FC'] == 685]
                # 編集処理

            # 1644-695の確認
            DE24 = T112_data[idx+20:idx+23]
            if DE24 == '695':
                df_transaction1644_695 = df_transaction1644[df_transaction1644['FORMAT-FC'] == 695]
                # 編集処理

        elif MTI == '1740':
            df_transaction1740 = df_transaction_category[df_transaction_category['FORMAT-MTI'] == 1740]
            
            # 1740-700の確認
            DE24 = T112_data[idx+84:idx+87]
            if DE24 == '700':
                df_transaction1740_700 = df_transaction1740[df_transaction1740['FORMAT-FC'] == 700]
                # 編集処理

            # 1740-780の確認
            DE24 = T112_data[idx+77:idx+80]
            if DE24 == '780':
                df_transaction1740_780 = df_transaction1740[df_transaction1740['FORMAT-FC'] == 780]
                # 編集処理

            # 1740-781の確認
            DE24 = T112_data[idx+77:idx+80]
            if DE24 == '781':
                df_transaction1740_781 = df_transaction1740[df_transaction1740['FORMAT-FC'] == 781]
                # 編集処理

            # 1740-782の確認
            DE24 = T112_data[idx+77:idx+80]
            if DE24 == '782':
                df_transaction1740_782 = df_transaction1740[df_transaction1740['FORMAT-FC'] == 782]
                # 編集処理

            # 1740-783の確認
            DE24 = T112_data[idx+77:idx+80]
            if DE24 == '783':
                df_transaction1740_783 = df_transaction1740[df_transaction1740['FORMAT-FC'] == 783]
                # 編集処理

        elif MTI == '1240':
            df_transaction1240 = df_transaction_category[df_transaction_category['FORMAT-MTI'] == 1240]
            
            # 1240-200の確認
            DE24 = T112_data[idx+80:idx+83]
            print("DE24 :%s" % DE24)
            if DE24 == '200':
                df_transaction1240_200 = df_transaction1240[df_transaction1240['FORMAT-FC'] == 200]
                # 編集処理

            # 1240-205の確認
            DE24 = T112_data[idx+80:idx+83]
            print("DE24 :%s" % DE24)
            if DE24 == '205':
                df_transaction1240_205 = df_transaction1240[df_transaction1240['FORMAT-FC'] == 205]
                # 編集処理

            # 1240-280の確認
            DE24 = T112_data[idx+80:idx+83]
            print("DE24 :%s" % DE24)
            if DE24 == '280':
                df_transaction1240_280 = df_transaction1240[df_transaction1240['FORMAT-FC'] == 205]
                # 編集処理

