# coding=utf-8
import httplib2, urllib, getpass
#import xml.dom.minidom
from xml.dom import minidom
#httplib2.debuglevel = 1

strFotologDown = 'Fotolog se encuentra bajo mantenimiento programado'
headers = {'Content-type': 'application/x-www-form-urlencoded'}
http = httplib2.Http()

url = "http://www.segundamano.es/li?q=placa+base&ca=28_s&c=3&x=2&w=2&z="
host = "http://www.segundamano.es"
links = []

def getHtmlPlacaBase():
	html = urllib.urlopen(url).read()
	return html

def getTable(html):
	ini = html.find('<table class="listing"')
	fin = html.find('</table>', ini) + len('</table>')
	ret = '<?xml version="1.0" encoding="ISO-8859-1"?>' + html[ini:fin]
	#ret = ret.replace('class="j">', 'class="j"/>')
	#ret = ret.replace('class="i">', 'class="i"/>')
	finimg = ret.find('<img')
	while finimg > -1:
		cierre = ret.find('>', finimg)+1
		if ret[cierre-2] != '/':
			ret = ret.replace(ret[finimg:cierre],ret[finimg:cierre-1]+"/>")
		finimg = ret.find('<img', cierre)
	ret = ret.replace('&euro;', 'E')
	return ret

def mostrar(table):
	doc = minidom.parseString(table)
	#print "\n".join(dir(doc))
	rows = doc.getElementsByTagName('tr')
	i = 0
	for row in rows:
		tds = row.getElementsByTagName('td')
		#[0] = fecha
		fecha = tds[0].firstChild.nodeValue
		#[1] = hora
		hora = tds[1].firstChild.nodeValue
		#[2] = mas fotos
		#[3] = titulo y link
		linkElem = tds[3].getElementsByTagName('a')[0]
		titulo = linkElem.firstChild.nodeValue
		#print "\n".join(dir(linkElem))
		link = linkElem.getAttribute('href')
		links.insert(i, host + link)
		#[4] = precio
		try:
			precio = tds[4].firstChild.nodeValue
		except AttributeError:
			precio = ""
		#[5] = lugar
		try:
			lugar = tds[5].firstChild.nodeValue
		except AttributeError:
			lugar = ""
		#[6] = no se
		
		print i, '->', fecha, hora, precio, lugar, titulo
		i = i+1

def verItem(item):
	html = urllib.urlopen(links[item]).read()
	priceini = html.find('<!-- Price -->')+len('<!-- Price -->')
	priceini = html.find('</strong>', priceini)+len('</strong>')
	if priceini-len('</strong>') > -1:
		pricefin = html.find('&', priceini)
		precio = html[priceini:pricefin]
	else:
		precio = "indefinido"
	bodyini = html.find('<!-- Body -->') + len('<!-- Body -->')
	bodyfin = html.find('</span>', bodyini)
	body = html[bodyini:bodyfin].strip()
	body = body.replace('<br />', '\n')
	
	ret = "\nPrecio: " + precio + "E\n\n"
	ret = ret + body + "\n\n\n"
	return ret
	

html = getHtmlPlacaBase()
table = getTable(html)
mostrar(table)

try:
	l = 0
	while l == 0:
		opc = raw_input('Anuncio: ')
		print verItem(int(opc))
except KeyboardInterrupt:
	print 'Ok, adios!'

# lineas = table.split("\n")
# def linea(l, k):
	# print lineas[l]
	# print lineas[l][k]

#print 'fin'

