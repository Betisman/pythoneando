# -*- coding: UTF-8 -*-
from pysqlite2 import dbapi2 as sqlite
import codecs
import sys
#script para inicialización de la bd

# lines = open('misc\\inserts.sql').readlines()
# sqls = []
# for sql in lines:
	# print sql
	# if sql.startswith('--'):
		# print 'no hacemos nada'
		# pass
	# else:
		# sqls.append(unicode(sql, sys.stdout.encoding))
sql = open('misc\\inserts.sql').read()
#sql = unicode(sql, sys.stdout.encoding)
sql = unicode(sql, 'utf-8')
ini = sql.find('DROP')
sql = sql[ini:]
sqls = sql.split(';\n')
print 'length ==', len(sqls)

conn = sqlite.connect('misc\\ht.sqlite')
cur = conn.cursor()
for sql in sqls:
	print sql
	try:
		if (sql == "COMMIT;"):
			conn.commit()
		else:
			cur.execute(sql)
	except sqlite.OperationalError, m:
		print 'Excepcion de pysqlite2 con >', sql, '<'
conn.close()

# sql = "select * from equipos"
# cur.execute(sql)
# for i in cur:
	# print i[1]