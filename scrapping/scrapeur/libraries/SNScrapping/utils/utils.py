#!/usr/bin/env python
#-*- coding: utf-8 -*-
from __future__ import absolute_import
import sys
import platform


def formater(str_text):
    str_text = str_text.replace('\n', ' ').strip()
    str_tab = str_text.split("  ")
    res = ""
    for s in str_tab:
        s = s.strip()
        if(s != ''):
            res = res +"\n"+ s
    return res

def ecriturePython2_Python3(file, myStr):
    if sys.version_info >= (3,0):
        file.write(myStr)
    else:
        file.write(myStr.encode('utf8'))