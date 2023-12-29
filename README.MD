This is a demo application: it shows how it is possible using a Cesium viewer to show and save 
a near-real time stream of data  originated by an IoT device belonging to a Building 

The application main components are the following : 

PYCODE
PORT 8080
.web-server : cherrypy webserver to provide frontend assets

PYCODE
.MQTTclient : py code which emulates an IoT device publishing data on topic /EnergyCenter

SERVICE
PORT 1883
.MQTT.Broker : mosquitto 

SERVICE 
.Telegraf : agent server configured to receive MQTT data on /EnergyCenter topic and write them in influxdb 

SERVICE
PORT 8086
.influx-db : temporal series database where streamed data are saved 
 
PYCODE
PORT 8081
.influx-server : cherrypy wrapper which allows to start and stop a stream of data (from influxdb) from the client using server-sent-event (SSE)

.CesiumJS : frontend component to view and manage 3D buildings

.PLOTTING LIBRARY - TO CHOOSE

/
.Cesium-IoN-asset : the file with building geometries hosted on the Cesium cloud

SERVICE
PORT 27017
.mongodb : object-database which keeps track of IoT devices mounted by a specific building

PYCODE
PORT 8082
.mongodb-server : cherrypy wrapper which allows to receive request involving a specific building and returns the device it mounts 


