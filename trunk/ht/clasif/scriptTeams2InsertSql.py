#!/usr/bin/env python
# coding=ISO-8859-1

import xml.dom.minidom as minidom
import urllib, httplib2
import sys
import time, datetime

def equipo2String(equipo):
	id = equipo.getAttributeNode('id').nodeValue
	nombre = equipo.getElementsByTagName('nombre')[0].firstChild.nodeValue
	return 'INSERT INTO "equipos" VALUES('+id+',"'+nombre+'",0,0,0,0,0,0,0,0,"-");\n'

def afichero(content, fichero):
	f = open(fichero, 'w')
	f.write(content.encode("utf-8"))
	f.close()
	return 'Generado fichero ' + fichero

path = "..\\m40.xml"

doc = minidom.parse(path)
equipos = doc.getElementsByTagName('equipo')

str = ""
for equipo in equipos:
	sqlEquipo = equipo2String(equipo)
	str = str + sqlEquipo
	print sqlEquipo
afichero(str, "inserts.txt")