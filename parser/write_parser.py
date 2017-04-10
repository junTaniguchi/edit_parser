# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 11:46:56 2017

@author: j13-taniguchi
"""

import os, glob
import datetime
import json
import pickle
from dump_bulk import dump_bulk

#T112_directly = 'C:/Users/j13-taniguchi/Desktop/git/edit_parser/parser'
#os.chdir(T112_directly)

from parse_bulk import parse_bulk

# ジェネレータ作成
def generator():
    i = 1
    while True:
        yield i
        i+=1
gen = generator()

# inputファイルディレクトリへ格納されているT112ファイルすべてを取得
json_path_list = glob.glob("./../input/JSON/*.*")

# T112データを1ファイルずつ解析し、JSONファイルからDict型へ変換する
input_dict_list = []
for json_no, json_path in enumerate(json_path_list):
    with open(json_path, 'r') as json_file:
        json_data   = json.load(json_file)
        record_dict = json.loads(json_data)
        input_dict_list.append(record_dict)

    # 出力用のｓｔｒ型用意
    output_str = "0\x00\x00|\x00\x00\x00\x00"
    
    # 処理時刻をシステム日付より取得
    now = datetime.datetime.now()
    timestamp = now.strftime("%y%m%d%H%M%S") + "%02d" % (now.microsecond // 1000)
    # timestampを2回追記する
    output_str+=timestamp
    output_str+=timestamp
    
    # 後続ヘッダー部分を追記
    output_str+="\x00>00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x7F\xF4\x00\x00\x00\x17\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x58\x01\x39\x8100\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x40\x00\x00"
        
    for i in range(len(record_dict)):
        dict_idx = str(i)
        record_str = dump_bulk(record_dict)
        output_str+=record_str

    # ファイルへoutput_strを出力
    with open("./output/parse_json_%s.pickle" % str(json_no+1), 'wb') as str_file:
        str_file.write(output_str)
