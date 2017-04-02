# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 11:46:56 2017

@author: j13-taniguchi
"""

import os, glob
import pickle

#T112_directly = 'C:/Users/j13-taniguchi/Desktop/git/edit_parser'
T112_directly = 'C:/Users/JunTaniguchi/Desktop/git/edit_parser'
os.chdir(T112_directly)

from parse_bulk import parse_bulk

# ジェネレータ作成
def generator():
    i = 1
    while True:
        yield i
        i+=1
gen = generator()

# 出力用のDict型用意
output_dict = {}

# inputファイルディレクトリへ格納されているT112ファイルすべてを取得
T112_path_list = glob.glob("./input/*.*")

# T112データを1ファイルずつ解析し、pickleファイルへDict型として出力する
for T112_no, T112_path in enumerate(T112_path_list):
    with open(T112_path, 'r') as T112_file:
        T112_data = T112_file.read()

    transaction_MTI = ['1644','1740','1240','1442']
    # T112のデータをパースする。
    idx = 0
    while idx > len(T112_data):
        # 現在の添え字番号から4桁がMTIの値になっているかを確認
        MTI = T112_data[idx:idx+4]
        if MTI in transaction_MTI:
            # T112の中の1レコードを解析する
            idx, parsed_dict = parse_bulk(T112_data, idx)
            # {record_no1 : {解析されたT112のデータ}}
            output_dict["record_no" + next(gen)] = parsed_dict

        else:
            idx+=1
    
    # T112ファイル1件ごとにdictファイルをpickleファイルへ変換
    with open("./output/parse_T112_%s.pickle" % T112_no+1, 'wb') as pickle_file:
        pickle.dump(output_dict, pickle_file)



'''
# T112のデータの取り込み
with open('./input/TT112T0.001', 'r') as T112_file:
    T112_data = T112_file.read()

transaction_MTI = ['1644','1740','1240','1442']
# T112のデータをパースする。
idx = 0
while idx > len(T112_data):
    # 現在の添え字番号から4桁がMTIの値になっているかを確認
    MTI = T112_data[idx:idx+4]
    if MTI in transaction_MTI:
        
        idx, record = parse_bulk(T112_data, idx)
        
        # ビットマップをデータフレームへ展開
        #DE1 = pd.DataFrame(list(bitmap))
    else:
        idx+=1
'''