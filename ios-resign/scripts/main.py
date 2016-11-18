#!/usr/bin/python
#coding:utf-8

"""
@author: Elve.xu
@version: 1.1
"""

import sys

import packager

context = {}

"""
显示工具使用方法
"""
def dumpUsage():
	print ('Usage:')
	print ('	python3 main.py IMEI SOURCEIPA DEVELOPER MOBILEPROV TARGET')

if __name__ == '__main__':
	if len(sys.argv) != 6:
		dumpUsage()
	else:
		packager.start(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
