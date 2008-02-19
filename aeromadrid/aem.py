import urllib, httplib2, os
debug = 0	#debug=1 -> modifica el archivo donde se guarda el last-modified para que siempre crea que hay una nueva version de la programacion

headers = {'Content-type': 'application/x-www-form-urlencoded'}
http = httplib2.Http()
url = 'http://www.aeromadrid.com/estatico/vuelos/flight.zip'
fich = 'aem.txt'

response, content = http.request(url, 'POST')
lastmod = response['last-modified']
zipfile = 'flight.zip'
htmlfile = 'flight.htm'

def downloadZip(url, zipfile):
	urllib.urlretrieve(url, zipfile)

def descomprimirZip(zipfile):
	os.system('unzip -xoq ' + zipfile)

def estaAna(htmlfile):
	if open(htmlfile, "r").read().find('BENEITEZ AN') != -1:
		return 1
	else:
		return 0

if debug == 1:
	open(fich, "w").write('debugging')
		
try:
	f = open(fich, "r")
except IOError:
	print 'No existe el fichero ' + fich + ', se crea.'
	f = open(fich, "w")
	f.write('None')
	f.close()
	f = open(fich, 'r')
flast = f.readlines()
f.close()
flast = flast[0]
if flast != lastmod:
	print 'Version diferente (' + lastmod + ' vs ' + flast + ')'
	f = open(fich, "w")
	f.write(lastmod)
	f.close()
	downloadZip(url, zipfile)
	descomprimirZip(zipfile)
	if estaAna(htmlfile):
		print 'Anina sale en la nueva programacion'
	else:
		print 'NO sale Anina en la nueva programacion'
else:
	print 'Sin cambios en el last-modified (' + flast + ")"