#!/usr/bin/env python
# -?- coding: UTF-8 -*-
import time, re
import httplib2
import logging
import sys

log = logging.getLogger("RESUMENES")

  
def inicializar(nivelLog, log):
	if nivelLog == 'DEBUG' or nivelLog == 'debug':
		logLevel = logging.DEBUG
	else:
		logLevel = logging.INFO
	log.setLevel(logLevel)
	fh = logging.FileHandler("resumenes.txt")
	fh.setLevel(logLevel)
	formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
	fh.setFormatter(formatter)
	log.addHandler(fh)
  
host = 'http://www.hattrick.org/Club/Matches/Match.aspx?matchID='
# XII Liga M40
#jornada01 = {'Jornada 1': []}
#jornada02 = {'Jornada 2': []}
#jornada03 = {'Jornada 3': ['346204554']}
#jornada04 = {'Jornada 4': ['346342481', '346417469', '346362799']}
#jornada05 = {'Jornada 5': ['346597156', '346638523', '346591082']}
#jornada06 = {'Jornada 6': ['346802991', '346832036', '346876103', '346708744']}
#jornada07 = {'Jornada 7': ['347040320', '347089249', '347071306', '347023394']}
#jornada08 = {'Jornada 8': ['347275944', '347247890', '347268156', '347107130', '347301359']}
#jornada09 = {'Jornada 9': ['347450518', '347422977', '347316790', '347394123']}
#jornada10 = {'Jornada 10':['347611486', '347689213', '347588528', '347689337']}
#jornada11 = {'Jornada 11':['347865162', '347767353', '347869534', '347801894']}
#jornadas = [jornada01, jornada02, jornada03, jornada04, jornada05, jornada06, jornada07, jornada08, jornada09, jornada10, jornada11]

# XII Copa M40
jornada01 = {'Octavos de Final': ['348005753', '348093546', '348028643', '348072649', '348087926']}
jornada02 = {'Cuartos de Final': []}
jornada03 = {'Semifinales': []}
jornada04 = {'Final': []}
jornadas = [jornada01, jornada02, jornada03, jornada04]

def lanzar2(nivelLog, segundos):
  inicializar(nivelLog, log)
  log.info('Lanzamos el pollico Piticli... Ay Piticli bonico, aaaaay Piticli!!!');
  #try:
  i = 0
  
  headers = {}
  http = httplib2.Http()

  host = 'http://www.hattrick.org/Club/Matches/Match.aspx?matchID='
  content = {}
  respuesta = {}
  goleadores = {}
  for jornada in jornadas:
    strJornada = jornada.keys()[0]
    print '----------------------', strJornada, '----------------------'
    idpartidos = jornada[jornada.keys()[0]]
    urls = []
    for idpartido in idpartidos:
      urls.append(host + idpartido)
      
    for url in urls:
      inicio = time.time()
      #print url
      response, content = http.request(url, 'GET', headers=headers)
      i += 1
      content = content.decode('utf-8')
      #print content

      #import pdb; pdb.set_trace()
      ini = content.find('<h1')
      fin = content.find('</h1>', ini)
      
      #print ini, fin
      resultado = content[ini:fin]
      ini = resultado.find('</span>') + len('</span>') 
      fin = resultado.find('</span>', ini)
      #print ini, fin
      resultado = resultado[ini:fin].replace('<span>', '').strip()
      parentesis = resultado.find('(')
      #print parentesis
      idp = resultado[parentesis+1:resultado.find(')',parentesis)]
      resultado = resultado[:parentesis].strip()
      
      print ''
      print resultado, '->', idp
      
      ini = content.find('>Resumen</h2>')
      if ini == -1:
        ini = content.find('>Highlights</h2>')
      
      ini = content.find('<table>', ini)
      fin = content.find('</table>', ini)
      tabla = content[ini:fin]
      
      eventos = tabla.split('<tr')
      #print len(eventos)
      
      eventos = eventos[1:-1]
      
      ev = 0
      for evento in eventos:
        evento = evento[evento.find('<td'):]
        if evento.find('<img') < 0:
          #print "evento", ev, evento
          datos = evento.split('<td')
          #print evento
          #print len(datos)
          if len(datos) == 4:
            resultado = datos[1]
            goleador = datos[2]
            minuto = datos[3]
            #print "*res", resultado, "*"
            #print "*gol", goleador, "*"
            #print "*min", minuto, "*"
            strResultado = resultado[resultado.find('>')+1:resultado.find('</td>')].replace('&nbsp;', '').strip()
            link = goleador[goleador.find('<a'):goleador.find('</a>')]
            strJugador = link[link.find('>')+1:]
            idJugador = link[link.find('playerId=')+len('playerId='):link.find('"', link.find('playerId="')+len('playerId="')):]
            info = '%s %s (%s)' %(strResultado, strJugador, idJugador)
            while True:
              try:
                print info
                break
              except UnicodeEncodeError, e:
                message = '%s' %(e)
                #import pdb; pdb.set_trace()
                position = message[message.find('position')+len('position '):message.find(':')]
                pos = int(position)
                info = info[:pos] + '?' + info[pos+1:]
                
              
            try:
              goleadores[strJugador + ' (' + idJugador + ')'] = goleadores[strJugador + ' (' + idJugador + ')'] + 1
            except KeyError:
              goleadores[strJugador + ' (' + idJugador + ')'] = 1
            
        ev = ev + 1  
    
    #info = '%d - %s %7d %f %s %s' %(i, url, len(content), tiempoPeticion, status, indica)
    infor = ""
    print infor
  #except Exception:
  #  print Exception
  
  sorted_goleadores = [(v, k) for k, v in goleadores.items()]
  sorted_goleadores.sort()
  sorted_goleadores.reverse()             # so largest is first
  sorted_goleadores = [(k, v) for v, k in sorted_goleadores]
        
        
  headers = {}
  http = httplib2.Http()
  host = 'http://www.hattrick.org/Club/Players/Player.aspx?PlayerID='
  for goleador in sorted_goleadores:
    idjugador = goleador[0][goleador[0].find('(')+1:-1]
    url = host + idjugador
    response, content = http.request(url, 'GET', headers=headers)
    content = content.decode('utf-8')
    ini = content.find('ctl00_ctl00_CPContent_CPMain_pnlplayerInfo')
    ini = content.find('<table', ini)
    fin = content.find('</table>', ini)
    tabla = content[ini:fin]
    trs = tabla.split('<tr')
    fila = trs[1]
    tds = fila.split('<td')
    celda = tds[2]
    link = celda[celda.find('<a'):celda.find('</a')]
    strEquipo = link[link.find('>')+1:]
    info = '%2d %s --- %s' %(goleador[1], goleador[0], strEquipo)
    while True:
            try:
              print info
              break
            except UnicodeEncodeError, e:
              message = '%s' %(e)
              #import pdb; pdb.set_trace()
              position = message[message.find('position')+len('position '):message.find(':')]
              pos = int(position)
              info = info[:pos] + '?' + info[pos+1:]
             

if __name__ == "__main__":

	try:
		nivelLog = sys.argv[1]
	except IndexError:
		nivelLog = 'INFO'
	try:
		tiempoSegundos = int(sys.argv[2])
	except IndexError:
		tiempoSegundos = 120

	lanzar2(nivelLog, tiempoSegundos)