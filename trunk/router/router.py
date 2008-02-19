#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import httplib2, urllib, getpass
#httplib2.debuglevel = 1

headers = {'Content-type': 'application/x-www-form-urlencoded'}
http = httplib2.Http()

password = 'feo'
urllogin = 'http://192.168.1.1/cgi-bin/login.exe'
urlrestart = 'http://192.168.1.1/cgi-bin/restart.exe'

def login(password):
	body = {'pws':password}
	response, content = http.request(urllogin, 'POST', headers=headers, body = urllib.urlencode(body))
	if content.find('http://192.168.1.1/index.stm') < 0:
		raise Exception, 'KeyError exception en restart()'

def restart():
	body = {'page':'tools_gateway','logout':''}
	response, content = http.request(urlrestart, 'POST', headers=headers, body = urllib.urlencode(body))
	if content.find('http://192.168.1.1/wait.stm') < 0:
		raise Exception, 'KeyError exception en restart()'

try:
	print 'RARP 1.0: Reseteador Automático del Router del Piso (by Betisman)'
	print 'version 1.0 - 2008.02.14'
	print '\n\n\n'
	
	print login(password)
	print 'Login correcto'
	print restart()
	print 'Reseteando. Puede tardar un ratillo. Tranqui, tronco.'
except Exception, e:
	print e.value