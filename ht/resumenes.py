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

mapNombres = {'Betisman':'RBB', 'Roscuro':'Ros', 'PITERMAN':'ADP', 'Jumfrys':'Jum', 'ThePiso':'ThP', 'Cordoba':'Cor', 'Dogt':'Dog', 'C.C.F':'CCF', 'Capitan':'RGC', 'CONGRIO':'CON', 'Fantasma': 'Fan'}
infoEquipos = {}

#class Equipo(self, _nombre, _id=0, _pj=0, _pg=0, _pe=0, _pp=0, _gf=0, _gc=0, _ptos=0):
#  self.nombre = _nombre
#  self.id = _id
#  self.pj = _pj
#  self.pg = _pg
#  self.pe = _pe
#  self.pp = _pp
#  self.gf = _gf
#  self.gc = _gc
#  self.ptos = _ptos
#  
#  def actualizar(self, _nombre, _id, _pj, _pg, _pe, _pp, _gf, _gc, _ptos):
  

def resultadoAInfoEquipos(strResultado):
  lados = strResultado.split(' - ')
  #LOCAL
  local = lados[0]
  golesLocal = local[local.rfind(' '):].strip()
  equipoLocal = local[:local.rfind(' ')].strip()
  equipoLocal = mapNombres[equipoLocal]
  
  #VISITANTE
  visitante = lados[1]
  golesVisitante = visitante[:visitante.find(' ')].strip()
  equipoVisitante = visitante[visitante.find(' '):].strip()
  equipoVisitante = mapNombres[equipoVisitante]
  
  try:
    equipo = infoEquipos[equipoLocal]
    infoEquipos[equipoLocal]['pj'] = infoEquipos[equipoLocal]['pj'] + 1
    infoEquipos[equipoLocal]['gf'] = infoEquipos[equipoLocal]['gf'] + int(golesLocal)
    infoEquipos[equipoLocal]['gc'] = infoEquipos[equipoLocal]['gc'] + int(golesVisitante)
  except KeyError:
    equipo = {}
    equipo['pj'] = 1
    equipo['gf'] = int(golesLocal)
    equipo['gc'] = int(golesVisitante)
    infoEquipos[equipoLocal] = equipo
    
  try:
    equipo = infoEquipos[equipoVisitante]
    infoEquipos[equipoVisitante]['pj'] = infoEquipos[equipoVisitante]['pj'] + 1
    infoEquipos[equipoVisitante]['gf'] = infoEquipos[equipoVisitante]['gf'] + int(golesVisitante)
    infoEquipos[equipoVisitante]['gc'] = infoEquipos[equipoVisitante]['gc'] + int(golesLocal)
  except KeyError:
    equipo = {}
    equipo['pj'] = 1
    equipo['gf'] = int(golesVisitante)
    equipo['gc'] = int(golesLocal)
    infoEquipos[equipoVisitante] = equipo
    
def equiposMasGoleadores():
  ret = ''
  dictgoles = {}
  for equipo in infoEquipos:
    dictgoles[equipo] = infoEquipos[equipo]['gf']
  
  # -- Ordenar por gf
  sorted_dictgoles = [(v, k) for k, v in dictgoles.items()]
  sorted_dictgoles.sort()
  sorted_dictgoles.reverse()             # so largest is first
  sorted_dictgoles = [(k, v) for v, k in sorted_dictgoles]
  
  for equipo in sorted_dictgoles:
    #print equipo, sorted_dictgoles
    ret = '%s\n%s   %2d goles' %(ret, equipo[0], int(equipo[1]))
  
  return ret

def equiposMenosGoleados():
  ret = ''
  dictgoles = {}
  for equipo in infoEquipos:
    dictgoles[equipo] = float(float(infoEquipos[equipo]['gc']) / float(infoEquipos[equipo]['pj']))
  
  # -- Ordenar por gc
  sorted_dictgoles = [(v, k) for k, v in dictgoles.items()]
  sorted_dictgoles.sort()
  #sorted_dictgoles.reverse()             # so largest is first
  sorted_dictgoles = [(k, v) for v, k in sorted_dictgoles]
  
  for equipo in sorted_dictgoles:
    #print equipo, sorted_dictgoles
    ret = '%s\n%s   %2.2f goles/partido (%2d goles encajados en %d partidos)' %(ret, equipo[0], float(equipo[1]), infoEquipos[equipo[0]]['gc'], infoEquipos[equipo[0]]['pj'])
  
  return ret
  
host = 'http://www.hattrick.org/Club/Matches/Match.aspx?matchID='
jornadas = []
# XIV Liga M40
#jornadas.append({'Jornada 1': ['393178767', 'partidosinjugar_Capitan 3 - 0 PITERMAN']})
#jornadas.append({'Jornada 2': ['393367432', '393369812', '393257368']})
#jornadas.append({'Jornada 3': ['393570234', '393515400']})
#jornadas.append({'Jornada 4': ['393717060', '393652590']})
#jornadas.append({'Jornada 5': ['393912729', 'partidosinjugar_Roscuro 3 - 0 CONGRIO', 'partidosinjugar_Betisman 3 - 0 Capitan']})
#jornadas.append({'Jornada 6': ['394062321', '394124632', 'partidosinjugar_Capitan 3 - 0 CONGRIO']})
#jornadas.append({'Jornada 7': ['394320798', 'partidosinjugar_Capitan 3 - 0 Cordoba', '394243013']})
#jornadas.append({'Jornada 8': ['363373735', '363353881', '363340722', '363362061', 'partidosinjugar_Capitan 3 - 0 Jumfrys']})
#jornadas.append({'Jornada 9': ['363539272', '363524345', '363490686', 'partidosinjugar_C.C.F 0 - 3 Roscuro', 'partidosinjugar_Dogt 3 - 0 Jumfrys']})

# XIII Copa M40
#jornadas.append({'Octavos de Final': ['partidosinjugar_CONGRIO 3 - 0 Fantasma', 'partidosinjugar_ThePiso 3 - 0 Cordoba', '379235790', '379324963', '363770697']})
jornadas.append({'Cuartos de Final': ['partidosinjugar_ThePiso 3 - 0 Fantasma', 'partidosinjugar_PITERMAN 3 - 0 Roscuro', '394407592', '394436966']})
#jornadas.append({'Semifinales': ['379493907', '379477859']})
#jornadas.append({'Final': ['379715186']})


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
  infoEquipos = {}
  for jornada in jornadas:
    strJornada = jornada.keys()[0]
    print '----------------------', strJornada, '----------------------'
    idpartidos = jornada[jornada.keys()[0]]
    urls = []
    partidosSinJugar = []
    for idpartido in idpartidos:
      if idpartido.startswith('partidosinjugar_'):
		partidosSinJugar.append(idpartido.replace('partidosinjugar_', ''))
      else:
		urls.append(host + idpartido)
      
    for url in urls:
      inicio = time.time()
      #print url
      response, content = http.request(url, 'GET', headers=headers)
      open('content.txt', 'w').write(url + content)
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
      
      resultadoAInfoEquipos(resultado)
      
      ini = content.find('>Resumen</h2>')
      if ini == -1:
        ini = content.find('>Highlights</h2>')
      
      ini = content.find('<table class="tblHighlights">', ini)
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
            casa = resultado.split('</span>')[0]; casa = casa[casa.rfind('>')+1:]
            fuera = resultado.split('</span>')[1]; fuera = fuera[fuera.rfind('>')+1:]
            #strResultado = resultado[resultado.find('>')+1:resultado.find('</td>')].replace('&nbsp;', '').strip()
            strResultado = casa + '-' + fuera
            link = goleador[goleador.find('<a'):goleador.find('</a>')]
            strJugador = link[link.find('>')+1:]
            #idJugador = link[link.find('PlayerID=')+len('PlayerID='):link.find('"', link.find('PlayerID="')+len('PlayerID="')):]
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
		
    for psj in partidosSinJugar:
      print ''
      print psj, '->', '-1'
      resultadoAInfoEquipos(psj)

    #info = '%d - %s %7d %f %s %s' %(i, url, len(content), tiempoPeticion, status, indica)
    infor = ""
    print infor
  #except Exception:
  #  print Exception
  
  
  print 'Equipos más goleadores'
  print '----------------------'
  print equiposMasGoleadores()
  print ''
  print 'Equipos menos goleados'
  print '----------------------'
  print equiposMenosGoleados()
  
  print ''
  print 'Pichichi'
  print '--------'
  
  # -- Tratamos los goleadores para poder decir de qué equipo son.
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
    if len(trs) > 1 :
      fila = trs[1]
      tds = fila.split('<td')
      celda = tds[2]
      link = celda[celda.find('<a'):celda.find('</a')]
      strEquipo = link[link.find('>')+1:]
      info = '%2d %s --- %s' %(goleador[1], goleador[0], strEquipo)
    else:
      info = '%2d %s --- %s' %(goleador[1], goleador[0], '----------')
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
