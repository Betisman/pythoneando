import carr3
import sendgmail
import gcalendar #implica instalar la libreria gdata (de Google)!!!
import sys
import security
import os
import time

def leerFichero(file):
	return open(file, 'r').read()

def enviar():
    return bool(int(open('./xmls/enviar.txt', 'r').read()))

# Funcion que devuelve si existe bloqueo para la ejecucion del carrusel
def estaBloqueado():
    return os.path.isfile('proyectoM40/misc/generando.lock')

def lama():
    if sys.argv:
        if 'ini' in sys.argv:
            carr3.inicializarXmlMatchIds('./xmls/matchids3.xml')
        else:
            gmailusers = ['betisman@gmail.com', 'cbmdodo@gmail.com']

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
            open('proyectoM40/misc/generando.lock', 'w')
            print 'Fichero de bloqueo creado.'

            carr3.carruselear()
            msg = leerFichero('./xmls/carr.txt')

            print 'lama', open('./xmls/enviar.txt', 'r').read(), enviar()
            if enviar():
                for gmailuser in gmailusers:
                    try:
                        gmailpwd = security.getPassword(gmailuser)
                    except KeyError:
                        print 'El usuario %s no esta registrado.\n' %(gmailuser)
                        exit()
                    print 'enviamos sms'
                    mgc = gcalendar.MyGCalendar(gmailuser, gmailpwd)
                    mgc.login()
                    mgc.enviarSms(msg)

                #twitter
                #import twitter
                #api = twitter.Api(username='m40htnews', password='casona')
                #status = api.PostUpdate(msg)
            else:
                print 'no enviamos sms'

            open('./xmls/enviar.txt', 'w').write('0')

            os.remove('proyectoM40/misc/generando.lock')
            print 'Fichero de bloqueo eliminado'
	
if __name__ == "__main__":
	lama()