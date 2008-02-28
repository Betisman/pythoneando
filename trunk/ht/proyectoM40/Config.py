#!/usr/bin/env python
# coding=ISO-8859-1

class Config:
	file = "m40.conf"
	config = {}

	def __init__(self):
		lines = open(file, 'r').readlines()
		for line in lines:
			spl = line.split('=')
			key = spl[0].strip()
			value = spl[1].replace('"', '').strip()
			config[key] = value
			
	def get(self, key):
		return config[key]		