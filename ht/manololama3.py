import carr3
import sendgmail
import gcalendar #implica instalar la libreria gdata (de Google)!!!
import sys
import security

def leerFichero(file):
	return open(file, 'r').read()

def enviar():
    return bool(int(open('./xmls/enviar.txt', 'r').read()))

def lama():
    if sys.argv:
        if 'ini' in sys.argv:
            carr3.inicializarXmlMatchIds('./xmls/matchids3.xml')
        else:
            gmailusers = ['betisman@gmail.com', 'cbmdodo@gmail.com']

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
                import twitter
                twitter.Api(username='m40htnews', password='casona')
                twitter.PostUpdate(msg)
            else:
                print 'no enviamos sms'

            open('./xmls/enviar.txt', 'w').write('0')
	
if __name__ == "__main__":
	lama()