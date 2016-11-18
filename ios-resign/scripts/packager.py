#!/usr/bin/python
#coding:utf-8

"""
@author: Elve.xu
@version: 1.1
@note: 重签主类
"""

from kit import logger, shell
import os, shutil
import uuid

cwd = os.path.dirname(os.getcwd())

def start(imei, sourceipa, developer, mobileprov, target = None):
	pck = packager(imei, sourceipa, developer, mobileprov, target)
	pck.run()

class packager:
	def __init__(self, imei, sourceipa, developer, mobileprov, target):
		self.imei = imei
		self.sourceipa = sourceipa
		self.developer = developer
		self.mobileprov = mobileprov
		self.target = target
		''' 创建常用变量 '''
		self.work_dir = cwd + '/work'
		self.imei_dir = self.work_dir + '/' + self.imei
		self.extracted = self.imei_dir + '/' + str(uuid.uuid1())

	def run(self):
		logger.info('IMEI = %s' % self.imei)
		logger.info('SOURCEIPA = %s' % self.sourceipa)
		logger.info('DEVELOPER = %s' % self.developer)
		logger.info('MOBILEPROV = %s' % self.mobileprov)
		logger.info('TARGET = %s' % self.target)

		'''创建解压后的文件夹'''
		if os.path.exists(self.extracted):
			shutil.rmtree(self.extracted)
		os.makedirs(self.extracted)

		'''unlock'''
		'''
		self.unlock()
		'''

		'''解压ipa文件'''
		self.unzip()

		'''复制mobileprov文件'''
		self.copy_mobileprov()

		'''生成plist文件'''
		self.generate_plist()

		'''签名'''
		self.sign()

		'''压缩'''
		self.zip()

		'''清理工程'''
		self.clean()

	'''
	unlock
	'''
	def unlock(self):
		cmdstring = 'sudo security unlock-keychain -p "password"'
		logger.info(cmdstring)
		shell.execute(cmdstring, shell=True)

	"""
	解压
	"""
	def unzip(self):
		cmdstring = 'unzip -qo %s -d %s' % (self.sourceipa, self.extracted)
		logger.info(cmdstring)
		shell.execute(cmdstring)

	"""
	复制mobileprov文件
	"""
	def copy_mobileprov(self):
		''' 复制mobileprovision文件 '''
		for filename in os.listdir(self.extracted + '/Payload/'):
			f = os.path.splitext(self.extracted + '/Payload/' + filename)
			if len(f) != 2 or f[1] != '.app':
				continue
			'''设置解压后的.app文件夹路径'''
			self.payload_app_dir = self.extracted + '/Payload/' + filename
			self.mobileprov_to_dir = self.payload_app_dir + '/embedded.mobileprovision'

		cmdstring = 'cp %s %s' % (self.mobileprov, self.mobileprov_to_dir)
		logger.info(cmdstring)
		shell.execute(cmdstring)

	"""
	生成plist文件
	"""
	def generate_plist(self):
		self.full_plist_file = self.extracted + '/t_entitlements_full.plist'
		self.plist_file = self.extracted + '/t_entitlements.plist'
		cmdstring = 'sudo security cms -D -i %s > %s' % (self.mobileprov_to_dir, self.full_plist_file)
		logger.info(cmdstring)
		shell.execute(cmdstring, shell=True)

		cmdstring = '/usr/libexec/PlistBuddy -x -c "Print:Entitlements" %s > %s' % (self.full_plist_file, self.plist_file)
		logger.info(cmdstring)
		shell.execute(cmdstring, shell=True)

	"""
	签名
	"""
	def sign(self):
		for parent, dirnames, filenames in os.walk(self.payload_app_dir):
			for dirname in dirnames: # 循环所有文件夹
				d = os.path.splitext(parent + '/' + dirname)
				if len(d) != 2:
					continue
				if d[1] != '.app' and d[1] != '.appex' and d[1] != '.framework' and d[1] != '.dylib':
					continue
				cmdstring = '/usr/bin/codesign --continue -f -s "%s" --entitlements %s  %s' % (self.developer, self.plist_file, parent + '/' + dirname)
				logger.info(cmdstring)
				shell.execute(cmdstring, shell=True)
		'''签名app'''
		cmdstring = '/usr/bin/codesign --continue -f -s "%s" --entitlements %s  %s' % (self.developer, self.plist_file, self.payload_app_dir)
		logger.info(cmdstring)
		shell.execute(cmdstring, shell=True)
		os.remove(self.extracted + '/t_entitlements_full.plist')
		os.remove(self.extracted + '/t_entitlements.plist')

	"""
	压缩
	"""
	def zip(self):
		cmdstring = 'cd %s && ' % self.extracted
		cmdstring += 'zip -qry %s *' % (self.target)
		logger.info(cmdstring)
		shell.execute(cmdstring, shell=True)

	"""
	清理工程
	"""
	def clean(self):
		logger.info('clean temp')
		shutil.rmtree(self.extracted)