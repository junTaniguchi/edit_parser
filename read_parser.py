# -*- coding: sjis -*-
"""
Spyder�G�f�B�^

����͈ꎞ�I�ȃX�N���v�g�t�@�C���ł�
"""
import os, glob

T112_directly = 'C:\Users\j13-taniguchi\Desktop\01_PCAT0002'

os.chdir(T112_directly)

with open('TT112T0.001', 'rb') as t112_file:
    t112_data = read(t112_file)
    