#!/usr/bin/env python
# coding=UTF-8

class Config:
	def __init__(self):
		print 'carga de config'
		self.fich = "m40.conf"
		self.config = {}
		lines = open(self.fich, 'r').readlines()
		for line in lines:
			spl = line.split('=')
			key = spl[0].strip()
			value = spl[1].replace('"', '').strip()
			self.config[key] = value
			
	def get(self, key):
		return self.config[key]		