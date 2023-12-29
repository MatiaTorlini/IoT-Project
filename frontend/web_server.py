import cherrypy
import os

class Root :
	exposed = True
	def GET(self, *path, **params):
		if (len(path) == 0):
			#return the html page. In case of different pages a match on path[i] has to be done
			return open("index.html")
		return "Not found"
	

	
if __name__ == '__main__':

	conf = {
		'/': {
			'request.dispatch' : cherrypy.dispatch.MethodDispatcher(),
			'tools.staticdir.on' : True,
			'tools.staticdir.root' : os.path.abspath(os.getcwd()), #set the root dir from where to serve static files
			'tools.staticdir.dir' : '' #set this dir as static
		},
		'/css' : {
			'tools.staticdir.on' : True,
			'tools.staticdir.dir' : 'css' #specific dir in the base dir for serving static files
		},
		'/js' : {
			'tools.staticdir.on' : True,
			'tools.staticdir.dir' : 'js'
		}
	}

	cherrypy.tree.mount(Root(), '/', conf)

	cherrypy.config.update({'server.socket_host':'0.0.0.0'})
	cherrypy.config.update({'server.socket_port':8080})

	cherrypy.engine.start()
	cherrypy.engine.block()
