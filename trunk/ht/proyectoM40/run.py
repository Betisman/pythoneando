# coding=UTF-8
#import carr
import sendgmail
import CarruselHandler
import Config
import sys
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
					sendgmail.sendEmail('betisman+carloos.com', 'logaritmo', 'betisman@carloos.com', 'betisman@gmail.com', '[Carrusel]', msg, None)
					print 'Mail enviado correctamente a la direccion ' + to
			except Exception, msg:
				print 'El mail (creo) no ha sido enviado a la direccion', to, '(',sys.exc_info(),')'
		# subirFicheroAFtp(ficheroMarcadorXml, ftpASubir)

if __name__ == "__main__":
	main()