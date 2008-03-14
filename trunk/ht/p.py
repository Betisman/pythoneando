#!/usr/bin/env python
print "Content-type: text/html"
print
import cgi
form=cgi.FieldStorage()
x = form.getvalue("val")
return val+str('Pepsicola')