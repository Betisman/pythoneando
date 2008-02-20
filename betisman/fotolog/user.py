from urllib import urlopen
import sys

strFotologDown = 'Fotolog se encuentra bajo mantenimiento programado'
strRedDown = 'Se han detectado problemas de red, compruebe su conexion a Internet'

def getHtml(amigo):
	return urlopen('http://www.fotolog.com/'+amigo).read()

def getDivComments(html):
	enc = html.find('<div class="comment"')
	comments = []
	while (enc != -1):
		divend = html.find('</div>', enc)
		comments.append(html[enc:divend])
		enc = html.find('<div class="comment"', enc+1)
	return comments

def getUserEnDiv(divcomment):
	guestend = divcomment.find('</a>')
	guestst = divcomment.rfind('>', 0, guestend)
	if guestst > -1:
		guest = divcomment[guestst+1:guestend]
		if len(guest) > 0:
			return guest
		else:
			return 'ERROR NOT(len(guest) > 0)'
	else:
		return 'ERROR NOT(guestst > -1)'

def getMensajeEnDiv(divcomment):
	#<p>...user...</p><p>...mensaje...</p>
	#nos situamos en la primera <p>
	p = divcomment.find('<p>')
	#nos situamos en la <p> del mensaje
	p = divcomment.find('<p>', p+1)
	ini = divcomment.find('>', p)+1
	fin = divcomment.find('</p>', p)
	mensaje = divcomment[ini:fin].strip()
	return mensaje

def getPhototitle(html):
	indexend = html.find('</h1>', html.find('<h1 id="phototitle">'))
	indexst = html.rfind('>', 0, indexend)
	title = html[indexst+1:indexend]
	return title

def getBlog(html):
	indexst = html.find('</h1>', html.find('<h1 id="phototitle">'))
	indexst = html.find('<p>', indexst)+len('<p>')
	indexend = html.find('</p>', indexst)
	blog = html[indexst:indexend]
	return blog
	
def printMensajes(amigo):
	html = getHtml(amigo)
	title = getPhototitle(html)
	blog = getBlog(html)
	divcomments = getDivComments(html)
	print '\nFotolog de --> %s <-- (%s)' %(amigo, title)
	print sustBrs(blog)
	print '%s comentarios:' %len(divcomments)
	cont = 1
	for div in divcomments:
		user = getUserEnDiv(div)
		mensaje = sustBrs(getMensajeEnDiv(div))
		lines = mensaje.splitlines()
		print '  %s.- %s' %(cont, user)
		for line in lines:
			print '\t%s' %(line)
		print ''
		cont = cont + 1

def sustBrs(str):
	enc = str.lower().find('<br/>')
	while enc != -1:
		str = str.replace('<br/>', '\n')
		enc = str.lower().find('<br/>')
	return str

def isFotologRunning():
	try:
		content = urlopen('http://www.fotolog.com').read()
		if content.find(strFotologDown) != -1:	#si lo encuentra
			return 0 #fotolog caido
		else:
			return 1 #fotolog funcionando
	except IOError:
		return -1 #problemas de red

fotorun = isFotologRunning()	
if  fotorun > 0:
	try:
		amigo = sys.argv[1]
	except IndexError:
		amigo = raw_input('amigo: ')

	printMensajes(amigo)
else:
	if fotorun == 0:
		print strFotologDown
	else:
		print strRedDown