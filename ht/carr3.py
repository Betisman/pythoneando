# coding=ISO-8859-1
import sys
import time

import datetime
import httplib2
import xml.dom.minidom as minidom
#httplib2.debuglevel = 1

def getRecommendedServer(http):
    """
	Método que obtiene el servidor recomendado por Ht para realizar las conexiones.
	"""
    try:
        #urle que Hattrick dice que es la que nos dice qué servidor usar
        url = 'http://www.hattrick.org/common/chppxml.axd?file=servers'
        #realizamos la petición http a la url anterior
        response, content = http.request(url, 'GET')
        #el content que nos devuelve la respuesta es un xml. Lo parseamos y buscamos la información que indica qué servidor es el que nos recomienda ht usar.
        dom = minidom.parseString(content)
        itemlist = dom.getElementsByTagName('RecommendedURL')
        recommendedServer = itemlist[0].firstChild.nodeValue
		
        print 'Servidor recomendado:', recommendedServer
        return recommendedServer
    except Exception, msg:
        #print 'Salto una excepcion en getRecommendedServer()', sys_exc_info()
        print 'Salto una excepcion en getRecommendedServer():', msg
        return None

def login(username, password, recServer, http):
    """
	Realiza el login a ht.
	El problema es que lo hacemos con el password, cuando deberíamos hacerlo con el securitycode.
	"""
    try:
        cookie = ''
        #inicializamos la cabecera de la petición http
        #self.headers = {'Content-type': 'application/x-www-form-urlencoded'}
        headers = {}
        print 'url', recServer
        url = recServer + '/common/chppxml.axd?file=login&readonlypassword=elpiso&loginname=alecasona&actionType=login&chppID=3501&chppKey=BE421657-81E6-4AEE-8BF5-CB2E36BB3D6A'
        #print url
        #construimos el boy de la petición http (para saber qué valores enviar, hemos usado el LiveHttpHeaders de Firefox)
        body = {'actionType':'login', 'loginname':username, 'readonlypassword':'elpiso', 'chppID':'3501', 'chppKey':'BE421657-81E6-4AEE-8BF5-CB2E36BB3D6A'}
        #realizamos la conexión y recibimos el contenido de la respuesta y el response
        #response, content = self.http.request(url, 'GET', headers=self.headers, body = urllib.urlencode(body))
        response, content = http.request(url, 'GET', headers=headers)
        #print "requesting url:", url, urllib.urlencode(body)
        try:
            #capturamos la cookie devuelta para mantener la sesión
            cookie = response['set-cookie']
            headers['Cookie'] = cookie
        except KeyError:
            print 'Saltó excepción KeyError', sys.exc_info()
            #return None
        print 'se fue el try'
		
        doc = minidom.parseString(content)
        isAuth = doc.getElementsByTagName('IsAuthenticated')[0].firstChild.nodeValue
        loginResult = doc.getElementsByTagName('LoginResult')[0].firstChild.nodeValue
        userID = doc.getElementsByTagName('UserID')[0].firstChild.nodeValue
		
        response, content = http.request(url, 'GET', headers=headers)
        #print "requesting url:", url, urllib.urlencode(body)
        try:
            #capturamos la cookie devuelta para mantener la sesión
            cookie = response['set-cookie']
            headers['Cookie'] = cookie
        except KeyError:
            print 'Saltó excepción KeyError', sys.exc_info()
            #return None
		
        doc = minidom.parseString(content)
        isAuth = doc.getElementsByTagName('IsAuthenticated')[0].firstChild.nodeValue
        loginResult = doc.getElementsByTagName('LoginResult')[0].firstChild.nodeValue
        userID = doc.getElementsByTagName('UserID')[0].firstChild.nodeValue
		
        return http, headers
    except Exception, msg:
        # print 'Saltó una excepción en login().'
        # print 'Info:', sys.exc_info()
        print msg
        return None

def setRecServer():
    recServer = getRecommendedServer()

def valorElementoSimple(elem, tag):
    return elem.getElementsByTagName(tag)[0].firstChild.nodeValue
    # equipo.getElementsByTagName('teamid')[0].firstChild.nodeValue
	
def setValorElementoSimple(elem, tag, valor):
    elem.getElementsByTagName(tag)[0].firstChild.nodeValue = valor
	
def afichero(content, fichero):
    f = open(fichero, 'w')
    f.write(content.encode("utf-8"))
    f.close()
    return 'Generado fichero ' + fichero

def getMatches(path):
    doc = minidom.parse(path)
    matchids = doc.getElementsByTagName('matchid')
    ret = []
    for matchid in matchids:
        ret.append(matchid.firstChild.nodeValue)
    return ret
	
def asciizacion(cadena):
    #primero limpiamos las tildes
    tildes = {u'á':'a', u'é':'e', u'í':'i', u'ó':'o', u'ú':'u'}
    keys = tildes.keys()
    try:
        for i in tildes:
            abuscar = keys.pop()
            while cadena.find(abuscar) > -1:
                cadena = cadena.replace(abuscar, tildes[abuscar])
    except IndexError:
        pass
    # ahora limpiamos el resto de caracteres no ISO-8859-1
    charsmalos = []
    try:
        cadena.decode('iso-8859-1')
    except UnicodeEncodeError, message:
        for i in cadena:
            try:
                i.decode('iso-8859-1')
            except UnicodeEncodeError, message:
                charsmalos.append(i)
        if len(charsmalos) > 0:
            for c in charsmalos:
                cadena = cadena.replace(c, '?')
	
    # return cadena
    return cadena.encode('utf-8')

def sustituyeNombre(nombre):
    ret = nombre
    if nombre.find('Betisman') > -1:
        ret = 'RBB'
    elif nombre.find('ThePiso') > -1:
        ret = 'ThP'
    elif nombre.find('erroloro') > -1:
        ret = 'Per'
    elif nombre.find('ukakke') > -1:
        ret = 'Buk'
    elif nombre.find('Basullo') > -1:
        ret = 'Bas'
    elif nombre.find('Jumfr') > -1:
        ret = 'Jum'
    elif nombre.find('CONGRIO') > -1:
        ret = 'CON'
    else:
        ret = nombre[0]
    return ret

def actualizaXmlMatchids(pathMatchids, matchid, homegoals, awaygoals, minuto, nuevoEstado):
    #TODO:
    #sería una buena opción refactorizar este metodo y el getMatches() para que
    #parseemos varias veces el mismo fichero, sino que se haga una sola vez.
    #lo dejo pendiente.
    doc = minidom.parse(pathMatchids)
    mts = doc.getElementsByTagName('matchid')
    for mt in mts:
        if mt.firstChild.nodeValue == matchid:
            elem = mt
    elem.setAttribute('homegoals', homegoals)
    elem.setAttribute('awaygoals', awaygoals)
    elem.setAttribute('minuto', str(minuto))
    elem.setAttribute('estado', nuevoEstado)
    #afichero(pathMatchids, doc.toxml())
    open(pathMatchids, 'w').write(doc.toxml())
    print 'nuevo estado: ', nuevoEstado

def inicializarXmlMatchIds(pathMatchids):
    doc = minidom.parse(pathMatchids)
    mts = doc.getElementsByTagName('matchid')
    for elem in mts:
        elem.setAttribute('homegoals', '0')
        elem.setAttribute('awaygoals', '0')
        elem.setAttribute('minuto', '0')
        elem.setAttribute('estado', '00')
    #afichero(pathMatchids, doc.toxml())
    open(pathMatchids, 'w').write(doc.toxml())

def carruselear():
    http = httplib2.Http()
    #variables globales
    recServer = ''
    #headers = {'Content-type': 'application/x-www-form-urlencoded'}
    username = 'alecasona'
    password = 'casona'
    seccode = 'odonkor'
    #hasta aquí, variables globales
    pathXmls = "./xmls/"
    pathMatchids = pathXmls + "matchids3.xml"
    pathEnviar = pathXmls + 'enviar.txt'
    now = datetime.datetime.now()
    strResultados = ''

#    recServer = getRecommendedServer(http)
#    # http, headers = login(username, password, recServer, http)
#    # url = recServer + '/Common/chppxml.axd?file=live&actionType=clearAll&version=1.4'
#    # response, content = http.request(url, 'GET', headers=headers)
#    recServer = getRecommendedServer(http)
#    http, headers = login(username, password, recServer, http)

    matchids = getMatches(pathMatchids);
    print str(len(matchids)) + ' partidos'
#    url = recServer + '/Common/chppxml.axd?file=live'
    try:
#        #Cargamos los partidos
#        response, content = http.request(url, 'GET', headers=headers)
#
#        doc = minidom.parseString(content)
#
#        #recuperamos el fichero y sacamos los ids de todos los partidos que se encuentran en el
#        matches = doc.getElementsByTagName('Match')
#        print 'checkout0', len(matches)
#        matchidsborrar = []
#
#        url = recServer + '/Common/chppxml.axd?file=live'
#        response, content = http.request(url, 'GET', headers=headers)
#        doc = minidom.parseString(content)
#        matches = doc.getElementsByTagName('Match')
	
#        for matchid in matchids:
#            url = recServer + '/Common/chppxml.axd?file=live&actionType=addMatch&matchid=' + matchid
#            response, content = http.request(url, 'GET', headers=headers)
#            print 'añadido', matchid
#            url = recServer + '/Common/chppxml.axd?file=live'
#            response, content = http.request(url, 'GET', headers=headers)
#            doc = minidom.parseString(content)
#            matches = doc.getElementsByTagName('Match')
#
#        url = recServer + '/Common/chppxml.axd?file=live'
#        response, content = http.request(url, 'GET', headers=headers)
#        doc = minidom.parseString(content)
#        matches = doc.getElementsByTagName('Match')
#       MOCK
        doc = minidom.parseString(open('./xmls/live.xml', 'r').read())
        matches = doc.getElementsByTagName('Match')
#       END MOCK

        enviar = False

        matches = doc.getElementsByTagName('Match')
        for m in matches:
            agregarASms = False
            xmlMatchID = m.getElementsByTagName('MatchID')[0].firstChild.nodeValue
            if xmlMatchID in matchids:
                print 'procesando', xmlMatchID
                hometeam = m.getElementsByTagName('HomeTeamName')[0].firstChild.nodeValue
                awayteam = m.getElementsByTagName('AwayTeamName')[0].firstChild.nodeValue
                homegoals = m.getElementsByTagName('HomeGoals')[0].firstChild.nodeValue
                awaygoals = m.getElementsByTagName('AwayGoals')[0].firstChild.nodeValue

                hometeam = sustituyeNombre(hometeam)
                awayteam = sustituyeNombre(awayteam)
				
                #calculo del minuto actual
                inicio = m.getElementsByTagName('MatchDate')[0].firstChild.nodeValue
                inicio = time.mktime(time.strptime(inicio, "%Y-%m-%d %H:%M:%S"))
                inicio = datetime.datetime.fromtimestamp(inicio)
                ahora = datetime.datetime.now()
                # #########PARCHE CUTRE PARA LOS TIEMPOS CON LA DIFERENCIA DE 8 HORAS DE BLUEHOST
                ahora = datetime.datetime.now() + datetime.timedelta(hours=8)
                if ahora < inicio:
                    diferencia = 0
                else:
                    diferencia = ahora-inicio
                    diferencia, segundos = divmod(diferencia.seconds, 60)
                    if (diferencia > 45):
                        if (diferencia > 60):
                            diferencia = diferencia - 15
                            if (diferencia > 90):
                                diferencia = 90
                        else:
                            diferencia = 45
                minuto = str(diferencia)
                # MOCK
                minuto = 90
                # END MOCK

                #cambio de estado
                doc = minidom.parse(pathMatchids)
                mids = doc.getElementsByTagName('matchid')
                # encontrar el partido a usar
                for mt in mids:
                    if mt.firstChild.nodeValue == xmlMatchID:
                        matchid = mt
                # fin encontrar
                id = matchid.firstChild.nodeValue
                mi_homegoals = matchid.getAttribute('homegoals')
                mi_awaygoals = matchid.getAttribute('awaygoals')
                mi_minuto = matchid.getAttribute('minuto')
                mi_estado = matchid.getAttribute('estado')
                #import pdb;pdb.set_trace()

                print 'estado actual:', mi_estado
                if mi_estado == '00':   # Sin comenzar y no enviado
                    agregarASms = True
                    enviar = True
                    actualizaXmlMatchids(pathMatchids, xmlMatchID, homegoals, awaygoals, minuto, '10')
                if mi_estado == '10':   # Sin comenzar y enviado
                    if minuto <= 0:
                        agregarASms = False
                        estado = '10'
                    else:
                        agregarASms = True
                        enviar = True
                        estado = '30'
                    actualizaXmlMatchids(pathMatchids, xmlMatchID, homegoals, awaygoals, minuto, estado)
#                if mi_estado == '20':   # En juego y no enviado
#                    if homegoals != mi_homegoals or awaygoals != mi_awaygoals:
#                        agregarASms = True
#                        enviar = True
#                        estado = '20'
#                    elif minuto == 45:
#                        estado = '40'
#                    elif minuto == 90:
#                        estado = '60'
#                    else:
#                        estado = '30'
#                    actualizaXmlMatchids(pathMatchids, xmlMatchID, homegoals, awaygoals, minuto, estado)
                if mi_estado == '30':   # En juego y enviado
                    if homegoals != mi_homegoals or awaygoals != mi_awaygoals:
                        agregarASms = True
                        enviar = True
                        #estado = '20'
                        estado = '30'
                    elif minuto == 45:
                        agregarASms = True
                        enviar = True
                        estado = '50'
                    elif minuto >= 90:
                        agregarASms = True
                        enviar = True
                        estado = '70'
                    else:
                        estado = '30'
                    actualizaXmlMatchids(pathMatchids, xmlMatchID, homegoals, awaygoals, minuto, estado)

                if mi_estado == '50': # Descanso y enviado
                    if minuto < 46:
                        agregarASms = False
                        estado = '50'
                    else:
                        agregarASms = True
                        enviar = True
                        estado = '30'
                    actualizaXmlMatchids(pathMatchids, xmlMatchID, homegoals, awaygoals, minuto, estado)
                    
                if mi_estado == '70': # Final y enviado
                    agregarASms = False
                    estado = '70'
                    actualizaXmlMatchids(pathMatchids, xmlMatchID, homegoals, awaygoals, minuto, estado)
                #estoy viendo que es una grandisima chapuza
                #print xmlMatchID, 'cambio de estado a', estado

                #strResultados = strResultados + hometeam + " " + homegoals + "-" + awaygoals + " " + awayteam + "(" + minuto + ")"
                if agregarASms:
                    strResultados = '%s%s %s-%s %s(%d);' %(strResultados, hometeam, homegoals, awaygoals, awayteam, minuto)

    except Exception, message:
        print 'Excepción tratando partidos\n', sys.exc_info()
        print message

    print 'enviar:', enviar
    print strResultados
    
    url = recServer + '/Common/chppxml.axd?file=live&actionType=clearAll&version=1.4'
    response, content = http.request(url, 'GET', headers=headers)
    doc = minidom.parseString(content)
    matches = doc.getElementsByTagName('Match')

    print 'mensaje\n', asciizacion(strResultados)
    afichero(unicode(strResultados), pathXmls+'carr.txt')

    if enviar:
        afichero(pathEnviar, '1')
    else:
        afichero(pathEnviar, '0')