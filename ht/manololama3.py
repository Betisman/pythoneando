import carr3
import sendgmail
import gcalendar #implica instalar la libreria gdata (de Google)!!!

def leerFichero(file):
	return open(file, 'r').read()

def enviar():
    return bool(open('./xmls/enviar.txt', 'r').read())

def lama():
	gmailuser = 'betisman@gmail.com'
	gmailpwd = 'logaritmo'
	subject = 'Carrusel'

	carr.carruselear()
	msg = leerFichero('./xmls/carr.txt')

        if enviar:
            mgc = gcalendar.MyGCalendar(gmailuser, gmailpwd)
            mgc.login()
            mgc.enviarSms(msg)

        open('./xmls/enviar.txt', 'w').write('0')
	
if __name__ == "__main__":
	lama()