# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 13:44:40 2017

@author: j13-taniguchi
"""

import datetime

def create_header():
    """下記のマニュアルを元に編集
    『IPM Pre-edit and Utilities Workstation Plus』のP.214
    　　Appendix B Required Structure for Pre-edit Workstation Plus Input Files
    """
    # 1-4桁目　設定(固定値 :"\x30\x00\x00\x7C")
    output_str = "\x30\x00\x00\x7C"
    # 5-6桁目　設定(固定値 :Low-values2桁)
    output_str+="\x00\x00"
    # 7-8桁目　設定(固定値 :Low-values2桁)
    output_str+="\x00\x00"
    
    # 9-22桁目 処理時刻(YYMMDDHHMMSSCC)
    now = datetime.datetime.now()
    timestamp = now.strftime("%y%m%d%H%M%S") + "%02d" % (now.microsecond // 1000)
    output_str+=timestamp[:-1]

    # 23-36桁目 処理時刻(YYMMDDHHMMSSCC) <-本来は固定値Low-values14桁
    output_str+=timestamp[:-1]
    
    # 37-38桁目　設定(固定値 :"\x00\x3E")
    output_str+="\x00\x3E"
    
    # 39桁目　設定(固定値 :Low-values1桁)
    output_str+="\x00"

    # 40桁目　設定(固定値 :"\x01")
    output_str+="\x01"

    # 41桁目　設定(固定値 :Low-values1桁)
    output_str+="\x00"

    # 42桁目　設定(固定値 :Low-values1桁)
    output_str+="\x00"

    # 43桁目　設定(固定値 :Low-values1桁)
    output_str+="\x00"

    # 44桁目　設定(固定値 :Low-values1桁)
    output_str+="\x00"

    # 45-48桁目　設定(固定値 :Low-values4桁)
    output_str+="0".zfill(4*2).decode("hex")

    # 49桁目　設定(固定値 :"\x01")
    output_str+="\x01"

    # 50-54桁目　設定(固定値 :Low-values5桁)
    output_str+="0".zfill(5*2).decode("hex")

    # 55-58桁目　設定(固定値 :"\x00\x00\x7F\xF4")
    output_str+="\x00\x00\x7F\xF4"

    # 59-62桁目　設定(固定値 :"\x00\x00\x00\x01")
    output_str+="\x00\x00\x00\x01"

    # 63-108桁目　設定(固定値 :Low-values46桁)
    output_str+="0".zfill(46*2).decode("hex")

    # 109-112桁目　設定(固定値 :Low-values4桁)
    output_str+="\x58\x01\x39\x81"

    # 113-128桁目　設定(固定値 :Low-values16桁)
    output_str+="0".zfill(16*2).decode("hex")

    return output_str