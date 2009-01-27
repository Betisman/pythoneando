import carr
import sendgmail
import gcalendar #implica instalar la libreria gdata (de Google)!!!

def leerFichero(file):
	return open(file, 'r').read()

def lama():
	gmailuser = 'betisman@gmail.com'
	gmailpwd = 'logaritmo'
	subject = 'Carrusel'

	carr.carruselear()
	msg = leerFichero('./xmls/carr.txt')
	emails = open('./xmls/emails.txt', 'r').readlines()
	# for to in emails:
		# try:
			# sendgmail.sendGmail(gmailuser, gmailpwd, to, subject, msg, None)
			# print 'Mail enviado correctamente a la direccion ' + to
		# except Exception:
			# print 'El mail (creo) no ha sido enviado a la direccion', to
	# msg = msg.replace("Real Betisman Balompi", "RBB")
	# msg = msg.replace("Los filososfos", "lf")
	# msg = msg.replace("ThePiso", "TP")
	# msg = msg.replace("Borrachines Team", "BT")
	
	mgc = gcalendar.MyGCalendar('betisman@gmail.com', 'logaritmo')
	mgc.login()
	mgc.enviarSms(msg)
	
if __name__ == "__main__":
	lama()