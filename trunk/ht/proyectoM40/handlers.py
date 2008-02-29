# coding=UTF-8
from model import Equipo, Partido
import Config
from pysqlite2 import dbapi2 as sqlite

class EquipoHandler:
	def __init__(self, equipo):
		self.config = Config.Config()
		self.equipo = equipo
		self.conn = sqlite.connect(self.config.get('path.bd'))
	
	def actualizarEquipo(self):
		equipo = self.equipo
		actualizarEquipo(equipo.nombre, equipo.pj, equipo.g, equipo.e, equipo.p, equipo.gf, equipo.gc, equipo.avg, equipo.ptos)
	
	def actualizarEquipo(self, nombre, pj, g, e, p, gf, gc, avg, ptos):
		sql = "update equipos set pj = "+str(pj)+", g = "+str(g)+", e = "+str(e)+", p = "+str(p)+", gf = "+str(gf)+", gc = "+str(gc)+", avg = "+str(avg)+", ptos = "+str(ptos)+" where nombre = '"+nombre+"'"
		#print sql
		cur = self.con.cursor()
		cur.execute(sql)
		self.conn.commit()

	def actualizarEquipoTemp(self):
		equipo = self.equipo
		actualizarEquipoTemp(equipo.nombre, equipo.pj, equipo.g, equipo.e, equipo.p, equipo.gf, equipo.gc, equipo.avg, equipo.ptos)
	
	def actualizarEquipoTemp(self, nombre, pj, g, e, p, gf, gc, avg, ptos):
		sql = "update equipostemp set pj = "+str(pj)+", g = "+str(g)+", e = "+str(e)+", p = "+str(p)+", gf = "+str(gf)+", gc = "+str(gc)+", avg = "+str(avg)+", ptos = "+str(ptos)+" where nombre = '"+nombre+"'"
		#print sql
		cur = self.conn.cursor()
		cur.execute(sql)
		self.conn.commit()

class PartidoHandler:
	def __init__(self, partido):
		self.partido = partido
	
	def actualizarClasifTemp(self):
		local, visitante = getEquiposActualizados()
		#local
		l = EquipoHandler(local)
		l.actualizarEquipoTemp()
		#visitante
		v = EquipoHandler(local)
		v.actualizarEquipoTemp()
	
	def getEquiposActualizados(self):
		eqlocal = self.partido.local
		eqvisitante = self.partido.visitante
		
		if self.partido.goleslocal == self.partido.golesvisitante:
			#empatan
			eqlocal.ptos = eqlocal.ptos + 1
			eqlocal.e = eqlocal.e + 1
			eqvisitante.ptos = eqvisitante.ptos + 1
			eqvisitante.e = eqvisitante.e + 1
		else:
			if self.partido.goleslocal > self.partido.golesvisitante:
				#gana el equipo local
				eqlocal.ptos = eqlocal.ptos + 3
				eqlocal.g = eqlocal.g + 1
				eqvisitante.ptos = eqvisitante.ptos + 0
				eqvisitante.p = eqvisitante.p + 1
			else:
				#gana el visitante
				eqlocal.ptos = eqlocal.ptos + 0
				eqlocal.p = eqlocal.p + 1
				eqvisitante.ptos = eqvisitante.ptos + 3
				eqvisitante.g = eqvisitante.g + 1
		eqlocal.pj = eqlocal.pj + 1
		eqlocal.gf = eqlocal.gf + self.partido.goleslocal
		eqlocal.gc = eqlocal.gc + self.partido.golesvisitante
		eqlocal.avg = eqlocal.gf - eqlocal.gc
		return eqlocal, eqvisitante

class ClasifHandler:
	def __init__(self):
		self.config = Config.Config()
		self.conn = sqlite.connect(self.config.get('path.bd'))
	
	def actualizarClasifPartido(self, partido):
		ph = PartidoHandler(partido)
		ph.actualizarClasifTEmp()
	
	def getStrClasifTemp(self, grupo):
		ret = ""
		sql = "select * from equipostemp where grupo = '"+grupo+"' order by ptos desc, avg desc, gf desc"
		cur = self.conn.cursor()
		print sql
		cur.execute(sql)
		for row in cur:
			ret = ret + row.toString() + "\n"
		return ret

class DBHandler:
	def __init__(self):
		self.config = Config.Config()
		self.conn = sqlite.connect(self.config.get('path.bd'))
		
	def getEquipoTemp(self, nombre):
		sql = "SELECT * FROM equipostemp WHERE nombre = '"+nombre+"'"
		return self.getEquipoFromDB(sql)
	
	#devuelve el equipo nombre recogido de la tabla equipos de la DB
	def getEquipoIni(self, nombre):
		sql = "SELECT * FROM equipos WHERE nombre = '"+nombre+"'"
		return self.getEquipoFromDB(sql)

	def getEquipoFromDB(self, sql):
		#print sql
		cur = self.conn.cursor()
		cur.execute(sql)
		self.conn.commit()
		#ret = Equipo(cur[0] id, cur[1] nombre, cur[2] pj, cur[3] g, cur[4] e, cur[5] p, cur[6] gf, cur[7] gc, cur[8] avg, cur[9] ptos, cur[10] grupo)
		i=0
		while i < 11:
			print cur[i]
		#ret = Equipo(cur[0], cur[1], cur[2], cur[3], cur[4], cur[5], cur[6], cur[7], cur[8], cur[9], cur[10])
		#return ret