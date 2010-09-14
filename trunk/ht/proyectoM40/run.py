# coding=UTF-8
#import carr
import sendgmail
import CarruselHandler
import Config
import sys
import os
import timeimport security
#from pysqlite2 import dbapi2 as sqlite

def leerFichero(file):
	return open(file, 'r').read()

# def problemaTildes(config):
	# sqlRBB = 'update equipos set nombre = "Real Betisman Balompié" where id = 487829;'
	# sqlInfra = 'update equipos set nombre = "Inframundo CD Drogadictos anónimos" where id = 1457502;'
	# sqlRBBTemp = 'update equipostemp set nombre = "Real Betisman Balompié" where id = 487829;'
	# sqlInfraTemp = 'update equipostemp set nombre = "Inframundo CD Drogadictos anónimos" where id = 1457502;'
	# conn = sqlite.connect(config.get('path.bd'))
	# cur = conn.cursor()
	# cur.execute(sqlRBB)
	# cur.execute(sqlInfra)
	# cur.execute(sqlRBBTemp)
	# cur.execute(sqlInfraTemp)
	# conn.commit()
	
# Funcion que devuelve si existe bloqueo para la ejecucion del carrusel
def estaBloqueado():
	return os.path.isfile('misc/generando.lock')


def main():
	config = Config.Config()
	#problemaTildes(config);
	gmailuser = config.get('gmail.user')
	gmailpwd = config.get('gmail.password')
	subject = config.get('gmail.subject')
	ficheroCarrusel = config.get('file.carrusel')
	ficheroEmails = config.get('file.emails')
	# ficheroMarcadorXml = config.get('file.marcadorXml')
	# ftpASubir = config.get('ftp.molinete')

	#Generamos fichero lock
	segundos = 5
	acumulados = 0
	totalespera = 90 # 1 minutos 30 segundos
	while (estaBloqueado()):
		print 'esta bloqueado. espero', segundos, "segundos"
		time.sleep(segundos)
		acumulados = acumulados + segundos
		if acumulados >= totalespera:
			os.remove('misc/generando.lock')
			print 'Fichero de bloqueo eliminado de forma forzada tras', totalespera, ' segundos esperando que se desbloquee'
	open('misc/generando.lock', 'w')
	print 'Fichero de bloqueo creado.'
	
	ch = CarruselHandler.CarruselHandler()
	ch.generarFicheroCarrusel(ficheroCarrusel)
	msg = leerFichero(ficheroCarrusel)
	try:
		if sys.argv[1] == 'debug':
			print msg
	except Exception:
	#no hay sys.argv[]
		print msg
		emails = open(ficheroEmails, 'r').readlines()
		for to in emails:
			try:
				if not to.startswith('#'):
					#sendgmail.sendGmail(gmailuser, gmailpwd, to, subject, msg, None)
					sendgmail.sendEmail('betisman+carloos.com', security.getPassword('betisman@gmail.com'), 'betisman@carloos.com', 'm40htnews@googlegroups.com', '[Carrusel]', msg, None)
					print 'Mail enviado correctamente a la direccion ' + to
			except Exception, msg:
				print 'El mail (creo) no ha sido enviado a la direccion', to, '(',sys.exc_info(),')'
		# subirFicheroAFtp(ficheroMarcadorXml, ftpASubir)
		
	os.remove('misc/generando.lock')
	print 'Fichero de bloqueo eliminado'

if __name__ == "__main__":
	main()