import time
import threading

#comment this para mapagana nyo sa local machine ninyo
#raspi specific na libraries ito
import adafruit_dht
import board

class Sensor_Data:
    def __init__(self, temperature, humidity):
        self.temperature = temperature
        self.humidity = humidity


class DHT11_Data:
    def __init__(self):
        self.dht11 = adafruit_dht.DHT11(board.D23, use_pulseio=True) #GPIO 23 ang kanyang pin sa raspi
        self.readings = []
        self.currentIndex = 0
        
        self.thread = threading.Thread(target=self.read_loop, daemon=True)    
        self.thread.start()
    

    def read_loop(self):
        print('Reading start')

        #probably going to use a thread turn on and off here
        while True:
            try:
                self.temp = self.dht11.temperature #celsius
                self.humidity = self.dht11.humidity

                self.currentReading = Sensor_Data(self.temp, self.humidity)

                #shit implementation of a circular array
                if len(self.readings) < 20:
                    #print (f"Test temp: {self.temp}")
                    #print (f"Test hum: {self.humidity}")
                    self.readings.append(self.currentReading)
                else:
                    self.readings[self.currentIndex] = self.currentReading
                self.currentIndex = (self.currentIndex + 1) % 20

                #print (f"Current Index: {self.currentIndex}")
                
            except Exception as e:
                print(f"Sensor read error: {e}")
                #pass
            time.sleep(2.0)

    def get_current_reading(self):
        print("Index Returned: ".format(self.currentIndex))
        return self.readings[self.currentIndex]