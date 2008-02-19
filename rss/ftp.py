# coding=ISO-8859-1
from ftplib import FTP
import time
import datetime
import xml.dom.minidom as minidom

filename = 'rss.xml'
filename2 = 'rss2.xml'

#ftp = FTP('ftp.es.geocities.com')   # connect to host, default port
#print ftp.login('betisman', 'bronzechair90')               # user anonymous, passwd anonymous@
#print ftp.retrlines('LIST')     # list directory contents
#print ftp.quit()

#getFileFromFTP()
#modificarFeed()
dom = minidom.parseString(open(filename, 'r').read())
itemlist = dom.getElementsByTagName('item')
for item in itemlist:
	title = item.getElementsByTagName('title')[0]
	print title.childNodes[0].data
	

def crearItem(dom, titulo, link, contenido):
	#	<item>
	#		<title>titulo</title>
	#		<date>fecha</date>
	#		<link>enlace</link>
	#		<description>contenido de la noticia</description>
	#	</item>
	
	#creamos el elemento item
	newitem = dom.createElement('item')
	
	#creamos el elemento title
	newtitle = dom.createElement('title')
	#creamos el nodo de texto que contiene el titulo
	newtitletext = dom.createTextNode(titulo)
	#unimos el nodo de texto titulo como hijo del nodo titulo
	newtitle.appendChild(newtitletext)
	#unimos el nodo titulo al nodo item
	newitem.appendChild(newtitle)

	#creamos el nodo fecha (con la fecha actual de la propia ejecucion)
	newdate = dom.createElement('date')
	newdatetext = dom.createTextNode(datetime.datetime.today().strftime("%a, %d %b %Y %H:%M:%S"))
	newdate.appendChild(newdatetext)
	newitem.appendChild(newdate)

	#creamos el elemento link
	newlink = dom.createElement('link')
	newlinktext = dom.createTextNode(link)
	newlink.appendChild(newlinktext)
	newitem.appendChild(newlink)

	#creamos el elemento description (contenido de la noticia)
	newdesc = dom.createElement('description')
	newdesctext = dom.createTextNode(contenido)
	newdesc.appendChild(newdesctext)
	newitem.appendChild(newdesc)
	
	return newitem

newitem = crearItem(dom, titulo, link, contenido)
channel = dom.getElementsByTagName('channel')[0]
channel.appendChild(newitem)

# xml = dom.toxml(encoding="utf-8")
# print xml[210:230], xml[220]
# print xml
f = open(filename, 'w')
#f.write(dom.toprettyxml(encoding="utf-8"))
f.write(dom.toxml(encoding="utf-8"))
f.close()


#putFileInFTP()





#now.strftime("%a, %d %b %Y %H:%M:%S")