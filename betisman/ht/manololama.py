import carr
import sendgmail

def leerFichero(file):
	return open(file, 'r').read()

def lama():
	gmailuser = 'betisman@gmail.com'
	gmailpwd = 'logaritmo'
	subject = 'Carrusel'

	carr.carruselear()
	msg = leerFichero('.\\xmls\\carr.txt')
	emails = open('.\\xmls\\emails.txt', 'r').readlines()
	for to in emails:
		try:
			sendgmail.sendGmail(gmailuser, gmailpwd, to, subject, msg, None)
			print 'Mail enviado correctamente a la direccion ' + to
		except Exception:
			print 'El mail (creo) no ha sido enviado a la direccion', to

if __name__ == "__main__":
	lama()