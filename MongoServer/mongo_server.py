import re
import cherrypy
import json
from pymongo import MongoClient
import cherrypy_cors

cherrypy_cors.install()

def remove_id(d):
        if isinstance(d, dict):
            d = {key: remove_id(value) for key, value in d.items() if key != "_id"}
        elif isinstance(d, list):
            d = [remove_id(item) for item in d]
        return d


class Root :
	___mongo_manager = MongoClient("localhost",27017)
	___db = ___mongo_manager["DevicesDB"]
	___collection = ___db["buildings"]
	exposed = True
	def POST(self):
		cherrypy.response.headers["Content-Type"] = "application/json"
		cherrypy.response.headers['Access-Control-Allow-Origin']= "*" 
		cherrypy.response.headers['Access-Control-Allow-Methods']= 'POST,OPTIONS'

		___body = json.loads(cherrypy.request.body.read())
		print(___body["building_id"])
		___results = self.___collection.find({"CityObject.city_object_id":___body["building_id"]})	
		___response = list(___results)
		___response = remove_id(___response)
		___response = json.dumps(___response)
		return str(___response).replace("'","\"").encode("utf8")
	
	def OPTIONS(self): #needed for CORS preflight
		cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
		cherrypy.response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
		cherrypy.response.headers['Access-Control-Allow-Headers'] = 'Content-Type'

if __name__ == '__main__':

	conf = {
		'/': {
			'request.dispatch' : cherrypy.dispatch.MethodDispatcher(),
			'cors.expose.on': True,
			#'tools.encode.text_only': False
		}
	}

	cherrypy.tree.mount(Root(), '/', conf)

	cherrypy.config.update({'server.socket_host':'0.0.0.0'})
	cherrypy.config.update({'server.socket_port':8082})

	cherrypy.engine.start()
	cherrypy.engine.block()
