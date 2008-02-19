from urllib import urlopen

consultar = ['betisman', 'anabc11', 'anitamaradona', 'molinete33', 'blanca07', 'marywillrain', 'analfabetadeslen', 'juan_ubago']
strFotologDown = 'Fotolog se encuentra bajo mantenimiento programado'

def isFotologDown(content):
	if content.find(strFotologDown):
		return 1 #fotolog caido
	else:
		return 0 #fotolog funcionando

def isFotologRunning():
	try:
		content = urlopen('http://www.fotolog.com').read()
		if content.find(strFotologDown) != -1:	#si lo encuentra
			return 0 #fotolog caido
		else:
			return 1 #fotolog funcionando
	except IOError:
		print 'IOError al intentar conectar.'
		return 0

if isFotologRunning():
	for cons in consultar:
		cont = 0
		html = urlopen('http://www.fotolog.com/'+cons).read()
		indexend = html.find('</h1>', html.find('<h1 id="phototitle">'))
		indexst = html.rfind('>', 0, indexend)
		title = html[indexst+1:indexend]
		enc = html.find('<div class="comment"')
		guests = []
		while (enc != -1):
			divend = html.find('</div>', enc)
			guestend = html.find('</a>', enc, divend)
			guestst = html.rfind('>', 0, guestend)
			if guestst > -1:
				guest = html[guestst+1:guestend]
				if len(guest) > 0:
					guests.append(guest)
			enc = html.find('<div class="comment"', enc+1)
			cont = cont + 1
		
		print cons + ': (%s) "%s"\n\t%s\n' %(cont,title,guests)
else:
		print strFotologDown
