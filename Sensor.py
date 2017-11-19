import Adafruit_DHT
import datetime

class Sensor:
    def gather(self):
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
        timestamp = datetime.datetime.now()
        return temperature, humidity, timestamp
