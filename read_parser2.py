# -*- coding: sjis -*-
"""
Spyderエディタ

これは一時的なスクリプトファイルです
"""
import os, glob

T112_directly = 'C:\\Users\\j13-taniguchi\\Desktop\\01_PCAT0002'

os.chdir(T112_directly)

with open('TT112T0.001', 'r') as t112_file:
    t112_data = t112_file.read()

print(t112_data)
    