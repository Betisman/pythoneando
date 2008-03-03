# coding=UTF-8

class Partido:
	def __init__(self, local, goleslocal, golesvisitante, visitante, minuto):
		self.local = local
		self.goleslocal = goleslocal
		self.golesvisitante = golesvisitante
		self.visitante = visitante
		self.minuto = minuto

class Equipo:
	def __init__(self, id, nombre, nombrecorto, pj, g, e, p, gf, gc, avg, ptos, grupo):
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