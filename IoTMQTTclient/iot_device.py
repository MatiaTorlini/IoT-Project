
#								I M P O R T S 
#//region
from datetime import datetime
import json
import random
from datetime import datetime
import time
from Classes.Influx_mqtt_device import InfluxMQTTDevice
#//endregion

#						D E V I C E - S T A T I C - D A T A
#//region
___DEV_ID = "7854909A2347"
#//endregion


#//region
def _generate_data():
	___value = random.random() % 7
	___json_frame = {
		"measurement" : "weather",
		"device_id":___DEV_ID,
		"fields": {
			"temperature":___value,
			"humidity":___value*10
		}
	}

	return ___json_frame
#//endregion
	
#//region
if __name__ == "__main__":

	___IoT_dev = InfluxMQTTDevice(___DEV_ID)
	___IoT_dev.start()
	cnt = 0
	try:
		while(cnt!=500):
			___payload = []
			___payload.append(_generate_data())
			___IoT_dev._publish(json.dumps(___payload))
			time.sleep(0.5)
			print(str(___payload))
			cnt+=1
	except KeyboardInterrupt:
		___IoT_dev.stop()
#//endregion