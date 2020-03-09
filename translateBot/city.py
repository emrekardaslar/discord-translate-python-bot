import requests 
import sched,time
import keyboard
import smtplib

class City:
      name = ""
      weather = ""
      tempKelvin = ""
      url = ""

      def __init__(self,name):
            self.url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid=8310d0bdfed84872959abfeb47e4eab7".format(name)
            r = requests.get(url = self.url)
            data = r.json()
            self.name = name
            self.weather = data['weather'][0]['main']
            self.tempKelvin = data['main']['temp']

      def convert(self,kelvin):
            return round(float(kelvin) - 273.15,2)

      def getData(self):
            data = "The weather in " + self.name + ": " + self.weather + "\nThe temperature is " + str(self.convert(self.tempKelvin)) +  " °C\n" 
            return data
            
      def kill(self):
            del self
