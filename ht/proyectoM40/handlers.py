# coding=UTF-8
from model import Equipo, Partido
import model
import Config
from pysqlite2 import dbapi2 as sqlite
import xml.dom.minidom as minidom

class EquipoHandler:
	def __init__(self, equipo):
		self.config = Config.Config()
		self.equipo = equipo
		self.conn = sqlite.connect(self.config.get('path.bd'))
	
	def actualizarEquipo(self):
		equipo = self.equipo
		self.actualizarEquipo2(equipo.id, equipo.pj, equipo.g, equipo.e, equipo.p, equipo.gf, equipo.gc, equipo.avg, equipo.ptos)
	
	def actualizarEquipo2(self, id, pj, g, e, p, gf, gc, avg, ptos):
		sql = "update equipos set pj = "+str(pj)+", g = "+str(g)+", e = "+str(e)+", p = "+str(p)+", gf = "+str(gf)+", gc = "+str(gc)+", avg = "+str(avg)+", ptos = "+str(ptos)+" where id = "+str(id)
		#print sql
		cur = self.conn.cursor()
		cur.execute(sql)
		self.conn.commit()
	
	def actualizarEquipoTemp(self):
		equipo = self.equipo
		self.actualizarEquipoTemp2(equipo.id, equipo.pj, equipo.g, equipo.e, equipo.p, equipo.gf, equipo.gc, equipo.avg, equipo.ptos)
	
	def actualizarEquipoTemp2(self, id, pj, g, e, p, gf, gc, avg, ptos):
		sql = "update equipostemp set pj = "+str(pj)+", g = "+str(g)+", e = "+str(e)+", p = "+str(p)+", gf = "+str(gf)+", gc = "+str(gc)+", avg = "+str(avg)+", ptos = "+str(ptos)+" where id = "+str(id)
		#print sql
		cur = self.conn.cursor()
		cur.execute(sql)
		self.conn.commit()

	def insertarEquipo(self):
		equipo = self.equipo
		self.insertarEquipo2(equipo.id, equipo.pj, equipo.g, equipo.e, equipo.p, equipo.gf, equipo.gc, equipo.avg, equipo.ptos, equipo.grupo)
	
	def insertarEquipo2(self, id, pj, g, e, p, gf, gc, avg, ptos, grupo):
		sql = "insert into 'equipos' values ("+str(id)+","+str(pj)+","+str(g)+","+str(e)+","+str(p)+","+str(gf)+","+str(gc)+","+str(avg)+","+str(ptos)+",'"+str(grupo)+"')"
		print sql
		cur = self.conn.cursor()
		cur.execute(sql)
		self.conn.commit()
class PartidoHandler:
	def __init__(self, partido):
		self.partido = partido
	
	def actualizarClasifTemp(self):
		local, visitante = self.getEquiposActualizados()
		#local
		l = EquipoHandler(local)
		l.actualizarEquipoTemp()
		#visitante
		v = EquipoHandler(visitante)
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
		eqlocal.gf = eqlocal.gf + int(self.partido.goleslocal)
		eqlocal.gc = eqlocal.gc + int(self.partido.golesvisitante)
		eqlocal.avg = eqlocal.gf - eqlocal.gc
		eqvisitante.pj = eqvisitante.pj + 1
		eqvisitante.gf = eqvisitante.gf + int(self.partido.golesvisitante)
		eqvisitante.gc = eqvisitante.gc + int(self.partido.goleslocal)
		eqvisitante.avg = eqvisitante.gf - eqvisitante.gc
		return eqlocal, eqvisitante

class ClasifHandler:
	def __init__(self):
		self.config = Config.Config()
		self.conn = sqlite.connect(self.config.get('path.bd'))
		self.m40 = self.config.get('file.m40')
	
	def actualizarClasifPartido(self, partido):
		if partido.partidoliga:
			ph = PartidoHandler(partido)
			ph.actualizarClasifTemp()
		else:
			print "El partido ["+partido.local.nombre+" - "+partido.visitante.nombre+"] no pertenece a la liga, asi que no consta para la actualizacion de la clasificacion."
	
	def getStrClasifTemp(self, grupo):
		"""
			Devuelve el String con la clasfificacion lista para mostrar o guardar en fichero.
		"""
		clasif = []
		dbh = DBHandler()
		#traemos el resultado de la consulta a la BD
		cur = dbh.getClasifTemp(grupo)
		for row in cur:
			clasif.append(dbh.getEquipoFromRowCur(row))
		i = 1
		ret = "pos    Equipo"+" "*20+"pj g  e  p gf gc avg ptos\n"
		ret = ret + "-"*len(ret)+"\n"
		for eq in clasif:
			pos = "%2d.-" %(i)
			ret = ret + pos + self.equipoToClasifString(eq) + "\n"
			i = i + 1
		return ret
	
	def equipoToClasifString(self, equipo):
		"""
			Devuelve un String del tipo:
			Nombre pj g e p gf gc avg ptos
		"""
		ret = " %-26s %2d %2d %2d %2d %2d %2d %3d %4d" \
		%(equipo.nombre[:26], equipo.pj, equipo.g, equipo.e, equipo.p, equipo.gf, equipo.gc, \
		equipo.avg, equipo.ptos)
		return ret

	def setearTempComoPerm(self):
		# self.grupoTemp2Perm("A")
		#self.grupoTemp2Perm("B")
		cur = self.conn.cursor()
		cur.execute("DROP TABLE equipos")
		cur.execute("CREATE TABLE equipos AS SELECT * FROM equipostemp")
		self.conn.commit()

	def grupoTemp2Perm(self, grupo):
		"""
		Pasa la clasificaci�n temporal del grupo a que sea la clasificaci�n permanente.
		"""
		dbh = DBHandler()
		# cur = dbh.getClasifTemp(grupo)
		# for row in cur:
			# eq = dbh.getEquipoFromRowCur(row)
			# eqh = EquipoHandler(eq)
			# eqh.actualizarEquipo()
		# cura = dbh.getClasifTemp("A")
		# curb = dbh.getClasifTemp("B")
		# for row in cura:
			# eq = dbh.getEquipoFromRowCur(row)
			# eqh = EquipoHandler(eq)
			# eqh.actualizarEquipo()		
		# for row in curb:
			# eq = dbh.getEquipoFromRowCur(row)
			# eqh = EquipoHandler(eq)
			# eqh.actualizarEquipo()
	
	def getClasifTempNombresDict(self, grupo):
		"""
		Devuelve un diccionario con el nombre de los equipos ordenados seg�n la 
		clasificacion del grupo. key = puesto, value = nombre del equipo
		"""
		dbh = DBHandler()
		clasif = {}
		cur = dbh.getClasifTemp(grupo)
		i = 1
		for row in cur:
			nombre, nombrecorto = dbh.getNombres(row[0])
			clasif[i] = nombre
			i = i + 1
		return clasif

class DBHandler:
	def __init__(self):
		self.config = Config.Config()
		self.conn = sqlite.connect(self.config.get('path.bd'))
		self.m40 = self.config.get('file.m40')
	
	def getEquipoTemp(self, id):
		sql = "SELECT * FROM equipostemp WHERE id = " + id
		return self.getEquipoFromDB(sql)
	
	#devuelve el equipo nombre recogido de la tabla equipos de la DB
	def getEquipoIni(self, id):
		sql = "SELECT * FROM equipos WHERE id = " + id
		return self.getEquipoFromDB(sql)

	def getEquipoFromDB(self, sql):
		#print sql
		cur = self.conn.cursor()
		cur.execute(sql)
		self.conn.commit()
		for row in cur:
			eq = self.getEquipoFromRowCur(row)
		return eq
	
	def getNombres(self, teamid):
		team = None
		doc = minidom.parse(self.m40)
		#aqu� xpath vendr�a de perlas!!
		teams = doc.getElementsByTagName('equipo')
		for t in teams:
			if t.getAttribute('id') == str(teamid):
				team = t
				break
		nombre = team.getElementsByTagName('nombre')[0].firstChild.nodeValue
		nombrecorto = team.getElementsByTagName('nombrecorto')[0].firstChild.nodeValue
		return  nombre, nombrecorto
	
	def getEquipoFromRowCur(self, row):
		id = row[0]
		nombre, nombrecorto = self.getNombres(id)
		pj = row[1]
		g = row[2]
		e = row[3]
		p = row[4]
		gf = row[5]
		gc = row[6]
		avg = row[7]
		ptos = row[8]
		grupo = row[9]
		return Equipo(id, nombre, nombrecorto, pj, g, e, p, gf, gc, avg, ptos, grupo)
	
	def getClasifTemp(self, grupo):
		ret = ""
		sql = "select * from equipostemp where grupo = '"+grupo+"' order by ptos desc, avg desc, gf desc"
		cur = self.conn.cursor()
		#print sql
		cur.execute(sql)
		self.conn.commit()
		return cur

class M40XmlHandler:
	__metaclass__ = model.Singleton
	def __init__(self):
		print "M40XMLHANDLER"
		self.config = Config.Config()
		self.m40 = self.config.get('file.m40')
	
	def getXmlEquipo(self, id):
		team = None
		doc = minidom.parse(self.m40)
		teams = doc.getElementsByTagName('equipo')
		for t in teams:
			if t.getAttribute('id') == str(id):
				return t
		return None

	def getNombreFromXml(self, id):
		team = self.getXmlEquipo(id)
		try:
			return team.getElementsByTagName('nombre')[0].firstChild.nodeValue
		except AttributeError:
			raise Exception("No se encuentra el equipo con id", id, "en getNombreFromXml")

	def getNombreCortoFromXml(self, id):
		team = self.getXmlEquipo(id)
		return team.getElementsByTagName('nombrecorto')[0].firstChild.nodeValue

	def getMicroNombreFromXml(self, id):
		team = self.getXmlEquipo(id)
		return team.getElementsByTagName('micronombre')[0].firstChild.nodeValue