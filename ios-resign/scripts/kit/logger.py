#!/usr/bin/python
#coding:utf-8

"""
@author: Zero.zhao
@version: 1.0
@date: 2016-10-27 01:38:53
@note: 日志
"""

import os
import logging, logging.config

cwd = os.path.dirname(os.getcwd())
if not os.path.exists(cwd + '/logs'):
	os.makedirs(cwd + '/logs')

logging.config.fileConfig(cwd + '/conf/log.properties')
logger = logging.getLogger()

def error(msg):
	logger.error(msg)

def debug(msg):
	logger.debug(msg)

def warning(msg):
	logger.warning(msg)


def info(msg):
	logger.info(msg)