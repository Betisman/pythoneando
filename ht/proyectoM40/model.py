# coding=UTF-8

class Partido:
	def __init__(self, local, goleslocal, golesvisitante, visitante, minuto, partidoliga=True):
		self.local = local
		self.goleslocal = goleslocal
		self.golesvisitante = golesvisitante
		self.visitante = visitante
		self.minuto = minuto
		self.partidoliga = partidoliga

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