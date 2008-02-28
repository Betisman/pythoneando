# coding=ISO-8859-1

class Partido:
	def __init__(self, local, goleslocal, golesvisitante, visitante, minuto):
		self.local = local
		self.goleslocal = goleslocal
		self.golesvisitante = golesvisitantes
		self.visitante = visitante
		self.minuto = minuto

class Equipo:
	def __init__(self, id, nombre, pj, g, e, p, gf, gc, avg, ptos, grupo):
		self.id = id
		self.nombre = nombre
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