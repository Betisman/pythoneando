# coding=ISO-8859-1
import carr
import sendgmail
import CarruselHandler
import Config

def leerFichero(file):
	return open(file, 'r').read()

def main():
	config = Config.Config()
	gmailuser = config.get('gmail.user')
	gmailpwd = config.get('gmail.password')
	subject = config.get('gmail.subject')
	ficheroCarrusel = config.get('file.carrusel')
	ficheroEmails = config.get('file.emails')

	ch = CarruselHandler.CarruselHandler()
	ch.generarFicheroCarrusel(ficheroCarrusel)
	msg = leerFichero(ficheroCarrusel)
	emails = open(ficheroEmails, 'r').readlines()
	for to in emails:
		try:
			sendgmail.sendGmail(gmailuser, gmailpwd, to, subject, msg, None)
			print 'Mail enviado correctamente a la direccion ' + to
		except Exception:
			print 'El mail (creo) no ha sido enviado a la direccion', to

if __name__ == "__main__":
	main()