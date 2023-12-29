import json

import paho.mqtt.client as PahoMQTT


class InfluxMQTTDevice:
    
	#									C O N S T R U C T O R
	#//region
    def __init__(self, device_id, notifier = None):

        self.notifier = notifier
        self.___device_id = device_id
        self._isSubscriber = False
        # create an instance of paho.mqtt.client
        self._paho_mqtt = PahoMQTT.Client(str(device_id), True)
        # register the callback
        self._paho_mqtt.on_connect = self._OnConnect
        self._paho_mqtt.on_message = self._OnMessageReceived
        
        
        with open('iot_dev_mqtt_config.json') as conf_file :
            ___config = json.load(conf_file)
        self.___mqtt__broker_address = ___config['MQTTConf']['mqtt_broker']
        self.___mqtt__broker_port = ___config['MQTTConf']['mqtt_port']
        self.___root_topic = ___config['MQTTConf']['mqtt_root_topic']
        self.___QoS = ___config['MQTTConf']['devices_QoS']
        
	#//endregion
        
	#										M E T H O D S 								
	#//region
    def _OnConnect(self, paho_mqtt, userdata, flags, rc):
        print("Device connected to " + self.___mqtt__broker_address + "with status code :" + str(rc))
	#//endregion
        

	#//region     
    def _OnMessageReceived(self, paho_mqtt, userdata, msg):
        print("Received " + str(msg.payload))
        

        #json_data = json.loads(msg.payload.decode('utf8'))
        #HINT : MATCH ON TOPIC?
                    
        #match json_data:
        #    case {'command': 'stop'}:
        #        self.stop()
        #        pass
        #    case {'command': 'start'}:
        #        self.start()
        #        pass     
    #//endregion
        

	#//region
    def _publish(self,msg):
    #def _publish(self,leaf_topic, msg):
        self._paho_mqtt.publish("EnergyCenter/", msg, 0)
        #self._paho_mqtt.publish(self.___root_topic + self.___device_id + '/' + leaf_topic, msg, self.___QoS)
    #//endregion


	#//region
    def start(self):
        self._paho_mqtt.connect(self.___mqtt__broker_address, self.___mqtt__broker_port)
        self._paho_mqtt.loop_start()
        self._paho_mqtt.subscribe(self.___root_topic + str(self.___device_id) ,self.___QoS)
        print("Connected to " + self.___mqtt__broker_address + " on port: " + str(self.___mqtt__broker_port))
	#//endregion
                    

	#//region
    def stop(self):
        self._paho_mqtt.unsubscribe(self.___root_topic)
        self._paho_mqtt.loop_stop()
        self._paho_mqtt.disconnect()
	#//endregion