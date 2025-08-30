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
        self.thread = threading.Thread(target=self.read_loop, daemon=True)        
        self.readings = []
        self.currentIndex = 0

    def read_loop(self):
        print('Reading start')

        #probably going to use a thread turn on and off here
        while True:
            try:
                self.temp = self.dht11.temperature #celsius
                self.humidity = self.dht11.humidity

                self.currentReading = DHT11_Data(self.temp, self.humidity)

                #shit implementation of a circular array
                if len(self.currentIndex) < 20:
                    self.readings.append(self.currentReading)
                else:
                    self.readings[self.currentReading] = self.currentReading
                self.currentIndex = (self.currentIndex + 1) % 20

                print ("Current Index: ".format(self.currentIndex))
                
                '''
                #debugger statement
                print("The current index is now in: {}".format(self.currentIndex))
                self.readings.insert(self.currentIndex, self.currentReading)
                '''
            except:
                pass
            time.sleep(2.0)

    def get_current_reading(self):
        print ("Index Returned: ".format(self.currentIndex))
        return self.readings[self.currentIndex]