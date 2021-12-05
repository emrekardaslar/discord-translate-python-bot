import requests


class City:
    name = ""
    weather = ""
    tempKelvin = ""
    url = ""

    def __init__(self, name):
        self.url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid=8310d0bdfed84872959abfeb47e4eab7".format(
            name)
        r = requests.get(url=self.url)
        data = r.json()
        self.name = data['name']
        self.weather = data['weather'][0]['main']
        self.tempKelvin = data['main']['temp']

    def getTemp(self):
        return self.tempKelvin

    def convert(self, kelvin):
        return round(float(kelvin) - 273.15, 1)

    def getData(self):
        data = "The weather in " + self.name + " is:  " + self.weather + "\nThe temperature is " + str(
            self.convert(self.tempKelvin)) + " °C\n"
        return data

    def getName(self):
        return self.name

    def kill(self):
        del self
