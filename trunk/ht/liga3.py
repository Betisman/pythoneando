# coding=ISO-8859-1
import carr
import sendgmail
import gcalendar #implica instalar la libreria gdata (de Google)!!!
import xml.dom.minidom as minidom
import urllib, httplib2
import sys
import time, datetime

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
    url = 'http://www.marca.com/marcador/futbol/2010_11/segunda/jornada_2/'
    http = httplib2.Http()
    headers = {}
    response, content = http.request(url, 'GET', headers=headers)
    #open('marca.txt', 'w').write(content)
    #content = open('marca.txt', 'r').read()

    partidos = {}

    #ini = content.find('<!-- = Modulo Todos los partidos de segunda = -->')
    #fin = content.find('<!-- = Fin Modulo Todos los partidos de segunda = -->', ini)
    print 'url:', url
    ini = content.find('<div class="tabcontenedor_jornada" title="Jornada 2">')
    fin = content.find('<table class="pichichi">', ini)
    pos = ini + 1
    eqpartido = 1
    part = 1

    tr = content[ini:fin]
    tr = tr.split('\n')
    part = 1
    local = True
    partido = {}
    for i in tr:

        if i.find('class="equipo"') > 0:
            equipo = i[i.find('>') + 1:i.find('</td>')]
            equipo = equipo[equipo.find('>')+1:equipo.find('</a>')]
            if local:
                partido['local'] = equipo
            else:
                partido['visitante'] = equipo
        if i.find('class="resultado"') > 0:
            resultado = i[i.find('>') + 1:i.find('</td>')]
            resultado = resultado[resultado.find('>')+1:resultado.find('</a>')]
            if local:
                partido['reslocal'] = resultado
                local = False
            else:
                partido['resvisitante'] = resultado
        if i.find('class="estado') > 0:
            if i.find('inalizado') > 0:
                partido['finalizado'] = '*'
            else:
                partido['finalizado'] = ''
        if i.find('</tbody>') > -1:
            partidos[part] = partido
            partido = {}
            local = True
            part = part + + 1

    for i in partidos:
        print i, partidos[i]['local'], partidos[i]['reslocal'], '-', partidos[i]['resvisitante'], partidos[i]['visitante']

    txt = ''
    # for i in (1, 2, 3, 4):
        # txt += '%s%s-%s%s%s; ' %(partidos[i]['local'][:2], partidos[i]['reslocal'], partidos[i]['resvisitante'], partidos[i]['visitante'][:2], partidos[i]['finalizado'])
    # print i, txt

    for i in partidos:
        #if partidos[i]['local'].find('Betis') > -1 or partidos[i]['visitante'].find('Betis') > -1:
        if partidos[i]['local'].find('Betis') > -1 or partidos[i]['visitante'].find('Betis') > -1 or partidos[i]['local'].find('Cartagena') > -1 or partidos[i]['visitante'].find('Cartagena') > -1:
            txt += '%s%s-%s%s; ' % (partidos[i]['local'], partidos[i]['reslocal'], partidos[i]['resvisitante'], partidos[i]['visitante'])
            txt = txt.replace('&aacute;', 'a')
            txt = txt.replace('&eacute;', 'e')
            txt = txt.replace('&iacute;', 'i')
            txt = txt.replace('&oacute;', 'o')
            txt = txt.replace('&uacute;', 'u')

    print txt

    msg = txt
    log.info(txt)

    ant = open('liga.txt', 'r').read()
    if msg != ant:
        mgc = gcalendar.MyGCalendar('betisman@gmail.com', 'logaritmo')
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
        