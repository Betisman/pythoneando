import carr3
import sendgmail
import gcalendar #implica instalar la libreria gdata (de Google)!!!
import sys

def leerFichero(file):
	return open(file, 'r').read()

def enviar():
    return bool(open('./xmls/enviar.txt', 'r').read())

def lama():
    if sys.argv:
        if 'ini' in sys.argv:
            carr3.inicializarXmlMatchIds('./xmls/matchids3.xml')
        else:
            gmailuser = 'betisman@gmail.com'
            gmailpwd = 'logaritmo'
            subject = 'Carrusel'

            carr3.carruselear()
            msg = leerFichero('./xmls/carr.txt')

            if enviar:
                print 'enviamos sms'
                mgc = gcalendar.MyGCalendar(gmailuser, gmailpwd)
                mgc.login()
                mgc.enviarSms(msg)
            else:
                print 'no enviamos sms'

            open('./xmls/enviar.txt', 'w').write('0')
	
if __name__ == "__main__":
	lama()