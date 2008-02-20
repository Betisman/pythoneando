from urllib import urlopen
import sys

user = sys.argv[1]

def leer(user):
	print urlopen('http://www.fotolog.com/'+user).read()
	
leer(user)