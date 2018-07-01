import Adafruit_DHT
import datetime
from SDS011Sensor import SDS011Sensor

class Sensor:
    def __init__(self):
        self.sds011 = SDS011Sensor()

    def gather(self):
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
        [pm25, pm10] = self.sds011.read_sensor()
        print(pm25, pm10)
        timestamp = datetime.datetime.now()
        return timestamp, temperature, humidity, pm25, pm10