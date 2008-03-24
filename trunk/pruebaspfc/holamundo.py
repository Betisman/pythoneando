import cherrypy

configFile = 'holamundo.conf'
print 'eooooooooooo'
cherrypy.config.update(config=configFile)

from cherrytemplate import renderTemplate

class HolaMundo:
	@cherrypy.expose
	def index(self):
	#	ret = open('prueba.html', 'r').read()
	#	rep = '<script type="text/javascript" src="%s"></script>' % (siteurl('/js/jquery.js'))
	#	ret = ret.replace('<head>', '<head>\n'+rep)
	#	return ret
		return renderTemplate(file = 'prueba.jsp')
		#return open('prueba.jsp', 'r').read()
		#return self.render(None, template='prueba.jsp')
		#return '<py-include="prueba.jsp">'
	
	@cherrypy.expose
	def ajax(self):
		return 'eo'
#cherrypy.tree.mount(HolaMundo(), configFile)
cherrypy.tree.mount(HolaMundo(), "/")
cherrypy.engine.start()