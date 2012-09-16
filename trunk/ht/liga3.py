# coding=ISO-8859-1
import sendgmail
print 'cagao'
import gcalendar #implica instalar la libreria gdata (de Google)!!!
import xml.dom.minidom as minidom
import urllib, httplib2
import sys
import time, datetime
import security

def leerFichero(file):
	return open(file, 'r').read()

def afichero(content, fichero):
	f = open(fichero, 'w')
	f.write(content.encode("utf-8"))
	f.close()
	return 'Generado fichero ' + fichero

def getMatches(path):
	doc = minidom.parse(path)
	matchids = doc.getElementsByTagName('matchid')
	ret = []
	for matchid in matchids:
		ret.append(matchid.firstChild.nodeValue)
	return ret

def asciizacion(cadena):
	#primero limpiamos las tildes
	tildes = {u'á':'a', u'é':'e', u'í':'i', u'ó':'o', u'ú':'u'}
	keys = tildes.keys()
	try:
		for i in tildes:
			abuscar = keys.pop()
			while cadena.find(abuscar) > -1:
				cadena = cadena.replace(abuscar, tildes[abuscar])
	except IndexError:
		pass
	# ahora limpiamos el resto de caracteres no ISO-8859-1
	charsmalos = []
	try:
		cadena.decode('iso-8859-1')
	except UnicodeEncodeError, message:
		for i in cadena:
			try:
				i.decode('iso-8859-1')
			except UnicodeEncodeError, message:
				charsmalos.append(i)
		if len(charsmalos) > 0:
			for c in charsmalos:
				cadena = cadena.replace(c, '?')

	# return cadena
	return cadena.encode('utf-8')

def liga(log):
    log.info('ejecucion ----------------------------------------------')
    #url = 'http://www.marca.com/'
    url = 'http://www.marca.com/eventos/marcador/futbol/2012_13/primera/jornada_2/'
    http = httplib2.Http()
    headers = {}
    response, content = http.request(url, 'GET', headers=headers)
    #open('marca.txt', 'w').write(content)
    #content = open('marca.txt', 'r').read()

    ini = content.find('<div class="col_izq">')
    fin = content.find('<div class="col_der">')
	# ÑAPA por los problemas de Unicode y ese calvario
    trozo = content[ini:fin];
    trozo = trozo.replace('&aacute;', 'a').replace('&eacute;', 'e').replace('&iacute;', 'i').replace('&oacute;', 'o').replace('&uacute;', 'u')
    trozo = trozo.replace('&Aacute;', 'A').replace('&Eacute;', 'E').replace('&Iacute;', 'I').replace('&Oacute;', 'O').replace('&Uacute;', 'U')
    trozo = trozo.replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')
    trozo = trozo.replace('&ntilde;', 'n').replace('&Ntilde;', 'N')
    trozo = trozo.replace('Á', 'A').replace('É', 'E').replace('Í', 'I').replace('Ó', 'O').replace('Ú', 'U')
    trozo = trozo.replace('ñ', 'n').replace('Ñ', 'N')
    html = ''
    for linea in trozo.split('\n'):
        if linea.find('select') > -1 or linea.find('option') > -1:
            pass
        else:
            html = html + linea + '\n'

    #html = trozo
    htmlsindoctype = html[html.find('>')+1:]

    import xml.parsers.expat
    parsingok = False
    while (parsingok == False) :
        try:
            text = '<?xml version="1.0" encoding="iso-8859-1"?>'
            html = text + html;print html[7380:7392]
            afichero(html, 'docxml.xml')
            doc = minidom.parseString(html)
            parsingok = True
        except xml.parsers.expat.ExpatError, excmsg:
            print excmsg
		

    partidos = {}
    i = 0
    for div in doc.getElementsByTagName('div') :
        if div.getAttribute('class').find('equipos') > -1 :
            partido = {}
            elems = div.getElementsByTagName('div')
            partido['local'] 		= elems[1].firstChild.data
            partido['reslocal']  	= elems[2].firstChild.data
            partido['resvisitante']	= elems[3].firstChild.data
            partido['visitante'] 	= elems[4].firstChild.data
            partidos[i] = partido
            i = i + 1
			
	
    for i in partidos:
        print i, partidos[i]['local'], partidos[i]['reslocal'], '-', partidos[i]['resvisitante'], partidos[i]['visitante']			

    txt = ''
    # for i in (1, 2, 3, 4):
        # txt += '%s%s-%s%s%s; ' %(partidos[i]['local'][:2], partidos[i]['reslocal'], partidos[i]['resvisitante'], partidos[i]['visitante'][:2], partidos[i]['finalizado'])
    # print i, txt

    for i in partidos:
        #if partidos[i]['local'].find('Betis') > -1 or partidos[i]['visitante'].find('Betis') > -1:
        if partidos[i]['local'].find('Betis') > -1 or partidos[i]['visitante'].find('Betis') > -1 or partidos[i]['local'].find('Malaga') > -1 or partidos[i]['visitante'].find('Malaga') > -1:
        #if partidos[i]['local'].find('Deportivo') > -1 or partidos[i]['visitante'].find('Deportivo') > -1 or partidos[i]['local'].find('Rayo') > -1 or partidos[i]['visitante'].find('Rayo') > -1:
            txt += '%s%s-%s%s; ' % (partidos[i]['local'], partidos[i]['reslocal'], partidos[i]['resvisitante'], partidos[i]['visitante'])
            txt = txt.replace('&aacute;', 'a')
            txt = txt.replace('&eacute;', 'e')
            txt = txt.replace('&iacute;', 'i')
            txt = txt.replace('&oacute;', 'o')
            txt = txt.replace('&uacute;', 'u')

    print txt

    msg = txt
    log.info(txt)

    user='betisman@gmail.com'
    password=security.getPassword(user)
    ant = open('liga.txt', 'r').read()
    if msg != ant:
        mgc = gcalendar.MyGCalendar(user, password)
        mgc.login()
        mgc.enviarSms(msg)
        print 'envío', '\n', txt
        log.info('envio')
    else:
        print 'no envío'
        log.info('no envio')
    open('liga.txt', 'w').write(msg)
    log.info('fin ejecucion ------------------------------------------')

if __name__ == "__main__":
	open('ligalog.log', 'w').write('')
	import logging
	logger = logging.getLogger('ligalog')
	hdlr = logging.FileHandler('ligalog.log')
	formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
	hdlr.setFormatter(formatter)
	logger.addHandler(hdlr)
	logger.setLevel(logging.INFO)

	liga(logger)
        
