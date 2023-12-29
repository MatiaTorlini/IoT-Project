#											I M P O R T S 
import time
import cherrypy
import json
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import cherrypy_cors

#this server has 3 controller : GET /start, GET /stop and GET /events. 
# GET /start  sets variable stream_active to TRUE
# GET /stop  sets variable stream_active to FALSE
# GET /events is a channel to connect from the EventSource in the client to receive a stream of data



#	#								G L O B A L - I N S T A L L A T I O N S 

#									I N F L U X - C O N F I G
bucket = "energycenter"
org = "energycenter"
token = "ghN3nL6_wSNPnsoYsjRpnf5cT_tOTt30UbBzMlhm77vCm0MEcKT9MBfLXoNMOiMnh_-w0wZnho7_MsUDnxcmAw=="
url = "http://localhost:8086"
client = influxdb_client.InfluxDBClient(url=url,token=token,org=org)

#									I N F L U X - M A N A G E R
def query_data():
	query_api = client.query_api()
	query = 'from(bucket:"energycenter")\
			|> range(start:-1s)'
	result = query_api.query(org=org,query=query)
	results = []
	for table in result : 
		for record in table.records:
			results.append((record.get_field(),record.get_value()))
	return json.dumps(results)
	

	#									C L A S S E S 

	#									R O O T
class Root:
    exposed = True
    stream_active = False
    device_id = ''
	#									HTTP - M E T H O D S 
    
    def GET(self, *path):
	#										 N O N E       GET/
        if not path:
            pass	
        
	#									C H A N N E L - S T R E A M     GET/events
        
        elif path and path[0] == 'events':			
            cherrypy.response.headers["Content-Type"] = "text/event-stream;charset=utf-8"
            cherrypy.response.headers['Cache-Control'] = "no-cache"
            cherrypy.response.headers['Connection'] = "keep-alive"
            cherrypy.response.headers['Access-Control-Allow-Origin']= "*" 
            cherrypy.response.headers['Transfer-Encoding'] = "identity" #otherwise data got chunked (so?)
            def stream(): #generator fn + yield function returns the value at each step but does not stop
                i = -1
                while Root.stream_active:
                    i+=1
                    time.sleep(0.5)
                    data = i
                    yield f'data: {data}\n\n'
            return stream() #return all the data yielded by the stream() generator function
        
    def POST(self, *path, **params):
	#										 N O N E       POST/
        if not path:
            pass	        
        
	#									S T A R T - S T R E A M I N G      POST/start {body : deviceid}
        elif path and path[0]=='start':
            cherrypy.response.headers["Content-Type"] = "application/json"
            Root.stream_active = True
            body = json.loads(cherrypy.request.body.read())
            print(body)
            return b'true'
    #									S T O P - S T R E A M I N G      POST/stop
        elif path and path[0]=='stop':
            Root.stream_active = False
            return b'false'
        else:
    #										N O T - F O U N D      any pat not above
            return 'Invalid path'

if __name__ == '__main__':
    cherrypy_cors.install()

    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'cors.expose.on': True,
            'response.stream': True #!!!IMPORTANT!!!
        }
    }

    cherrypy.tree.mount(Root(), '/', conf)
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': 8081})
    cherrypy.engine.start()
    cherrypy.engine.block()
