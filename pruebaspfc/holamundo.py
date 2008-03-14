import cherrypy

class HolaMundo:
	@cherrypy.expose
	def index(self):
	#	ret = open('prueba.html', 'r').read()
	#	rep = '<script type="text/javascript" src="%s"></script>' % (siteurl('/js/jquery.js'))
	#	ret = ret.replace('<head>', '<head>\n'+rep)
	#	return ret
		return open('prueba.jsp', 'r').read()
	
	@cherrypy.expose
	def ajax(self):
		return 'eo'
cherrypy.tree.mount(HolaMundo(), '/')
cherrypy.server.quickstart()
cherrypy.engine.start()