#!/usr/bin/python
#coding:utf-8

"""
@author: Elve.xu
@version: 1.1
"""

import shlex
import datetime
import subprocess
import time
"""
运行指定的shell脚本
@param cmdstring: 执行的命令
@type cmdstring: string
@param cwd: 执行shell时, 要进入的文件夹
@type cwd: string
@param timeout: 执行shell的超时时间
@type timeout: int
@param shell: 是否为shell
@type shell: boolean
@return: 执行结果状态码
@rtype: string
"""
def execute(cmdstring, cwd = None, timeout = None, shell = False):
	if shell:
		cmdstring_list = cmdstring
	else:
		cmdstring_list = shlex.split(cmdstring)

	if timeout:
		end_time = datetime.datetime.now() + datetime.timedelta(seconds = timeout)

	# 没有指定标准输入错误的管道, 因此会打印到屏幕上
	sub = subprocess.Popen(cmdstring_list, cwd = cwd, stdin = subprocess.PIPE, shell = shell, bufsize = 4096)

	while sub.poll() is None:
		time.sleep(0.1)
		if timeout:
			if end_time <= datetime.datetime.now():
				raise Exception('Timeout: %s' % cmdstring)

	return str(sub.returncode)