# -*- coding: UTF-8 -*-
from pysqlite2 import dbapi2 as sqlite
import codecs
import sys
#script para inicialización de la bd
conn = sqlite.connect('misc\\ht.sqlite')
#sql = open('misc\\inserts.txt', 'r').read()
#codecs.open( "someFile", "r", "utf-8" )
# open('w.txt', 'w').write('pérréó')
# p = open('w.txt', 'r').read()
# print p
# sql = codecs.open('r.txt', 'r', 'utf-8').read()
# print sql
# sql = sql.decode('UTF8')
# print 'hola, pepsicola'
#sql = sql.decode('utf8')
# print sql

#sql = unicode(sql)


sqlRBB = u'update equipos set nombre = "Real Betisman Balompié" where id = 487829;'
sqlInfra = 'update equipos set nombre = "Inframundo CD Drogadictos anónimos" where id = 1457502;'
print sqlRBB
print sqlRBB.encode('latin-1')	
# cur = conn.cursor()
# cur.execute(sqlRBB)
# cur.execute(sqlInfra)
# conn.commit()