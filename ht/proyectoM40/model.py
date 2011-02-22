# coding=UTF-8

class Partido:
	def __init__(self, local, goleslocal, golesvisitante, visitante, minuto, partidoliga=True, jornada=None, grupo=None, eventos=None):
		self.local = local
		self.goleslocal = goleslocal
		self.golesvisitante = golesvisitante
		self.visitante = visitante
		self.minuto = minuto
		self.partidoliga = partidoliga
		self.jornada = jornada or None
		self.grupo = grupo or None
		self.eventos = eventos or None
		
class Evento:
	def __init__(self, eventKey=None, minute=None, subjectPlayerId=None, subjectTeamId=None, objectPlayerId=None, eventText=None):
		self.eventKey = eventKey
		self.minute = minute
		self.subjectPlayerId = subjectPlayerId
		self.subjectTeamId = subjectTeamId
		self.objectPlayerId = objectPlayerId
		self.eventText = eventText
		self.subjectPlayerName = self.getNombreJugador(self.subjectPlayerId)
		self.objectPlayerName = self.getNombreJugador(self.objectPlayerId)
		self.tipoEvento = self.setTipoEvento(self.eventKey)
	
	def getNombreJugador(self, playerId):
		text = self.eventText
		pos = text.find(playerId)
		if pos > -1: #está
			ini = text.find('title="', pos) + len('title="')
			fin = text.find('"', ini)
			return text[ini:fin]
		else:
			return ""
	
	def setTipoEvento(self, eventKey):
		clave = eventKey.split('_')[0]
		clave = int(clave)
		if clave >= 100 and clave < 200:
			return 'gol'
		elif clave >= 90 and clave < 100:
			return 'lesion'
		elif clave >= 500 and clave < 600:
			return 'amarilla'
		elif clave == 45:
			return 'descanso'
		else:
			return 'noContemplado'
		
class Equipo:
	def __init__(self, id, nombre, nombrecorto="nombrecorto", pj=-1, g=-1, e=-1, p=-1, gf=-1, gc=-1, avg=-1, ptos=-1, grupo=-1):
		self.id = id
		self.nombre = nombre
		self.nombrecorto = nombrecorto
		self.pj = pj
		self.g = g
		self.e = e
		self.p = p
		self.gf = gf
		self.gc = gc
		self.avg = avg
		self.ptos = ptos
		self.grupo = grupo
	
	def checkAvg(self):
		if self.gf - self.gc != self.avg:
			return False
		else:
			return True

class Grupo:
	def __init__(self, id, nombre, equipos, jornadas=None):
		self.id = id
		self.nombre = nombre
		self.equipos = equipos
		self.numEquipos = len(equipos)
		#self.clasificacion = self.clasificicacion(equipos)
		self.jornadas = jornadas or None
	
	def clasificacion(self, equipos):
		pass
	
	def ordenar(self):
		return cmp()
	
	def setJornadas(self, jornadas):
		self.jornadas = jornadas

class Jornada:
	def __init__(self, jornada, partidos):
		self.jornada = jornada
		self.partidos = partidos


class Singleton(type):
    def __init__(cls, name, bases, dct):
        cls.__instance = None
        type.__init__(cls, name, bases, dct)
 
    def __call__(cls, *args, **kw):
        if cls.__instance is None:
            cls.__instance = type.__call__(cls, *args,**kw)
        return cls.__instance

class Estadio:
	def __init__(self, id, nombre=None, capacidad=None):
		self.id = id
		self.nombre = nombre
		self.capacidad = capacidad