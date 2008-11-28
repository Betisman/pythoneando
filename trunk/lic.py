# coding=utf-8
import httplib2, urllib, getpass, codecs
#httplib2.debuglevel = 1

headers = {'Content-type': 'application/x-www-form-urlencoded'}
http = httplib2.Http()

def afichero(content, fichero):
		#f = open(fichero, 'w')
#		f = codecs.open(fichero, encoding='utf-8', mode='w')
		f = codecs.open(fichero, mode='w')
		f.write(content)
		f.close()
		return 'Generado fichero ' + fichero

def obtenerPagina(licencia):
	url = "http://www.fga.org/handicaps.asp?licencia=%s&tipobus=codigo&id=1&estilo=green" % (licencia)
	response, content = http.request(url, 'GET', headers=headers)
	return content

def encontrado(content):
	if content.find("digo no encontrado") > -1:
		return False
	else:
		return True

class Jugador:
		def __init__(self, licencia, federado, handicap, sexo, nivel):
			self.licencia = licencia
			self.federado = federado
			self.handicap = handicap
			self.sexo = sexo
			self.nivel = nivel

		def __str__(self):
			return "licencia: %s\nfederado: %s\nhandicap: %s\nsexo: %s\nnivel: %s\n" %(self.licencia, self.federado, self.handicap, self.sexo, self.nivel)
			
def obtenerJugador(content):
	ini = content.find("Licencia:</td><td width=60% align=left>")
	pos = content.find("align=left>", ini) + len("align=left>")
	licencia = content[pos:pos+10]
	pos = content.find("align=left>", pos+10) + len("align=left>")
	federado = content[pos:content.find("</td>", pos)]
	pos = content.find("align=left>", pos+10) + len("align=left>")
	handicap = content[pos:content.find("</td>", pos)]
	pos = content.find("align=left>", pos+10) + len("align=left>")
	sexo = content[pos:content.find("</td>", pos)]
	pos = content.find("align=left>", pos+10) + len("align=left>")
	nivel = content[pos:content.find("</td>", pos)]
	return Jugador(licencia, federado, handicap, sexo, nivel)

# pag = obtenerPagina(75106210)
# if encontrado(pag):
	# print "true"
	# j = obtenerJugador(pag)
	# print j

licini = 75107000
lic = licini
result = ""
while lic < 75110000:
	pag = obtenerPagina(lic)
	if encontrado(pag):
		j = obtenerJugador(pag)
		result += "%s: %s(%s)\n" %(j.licencia, j.federado, j.handicap)
	else:
		result += "AM%s: --\n" %(lic)
	if lic%100 == 0:
		print "AM%s" %(lic)
	lic += 1
fich = "lics-%s-%s.txt" %(licini, lic)
afichero(result, fich)