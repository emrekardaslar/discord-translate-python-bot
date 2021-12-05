import requests
from yaml import safe_load


class City:
    name = ""
    weather = ""
    tempKelvin = ""
    url = ""

    def __init__(self, name):
        self.token = self.setToken()
        self.url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid={}".format(
            name, self.token)
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

    def setToken(self):
        with open("env.yaml", encoding="utf-8") as env:
            config = safe_load(env)
            return config["OPENWEATHER_TOKEN"]
