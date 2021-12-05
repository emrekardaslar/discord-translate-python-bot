import requests
from datetime import datetime


class Corona:
    def __init__(self):
        self.url = "https://pomber.github.io/covid19/timeseries.json"
        req = requests.get(url=self.url)
        self.data = req.json()
        self.date = datetime.today().strftime('%Y-%m-%d')

    def getData(self, country):
        info = ''
        info += "Confirmed: " + str(self.data[country][len(self.data[country]) - 1]["confirmed"]) + '\n'
        info += "Deaths: " + str(self.data[country][len(self.data[country]) - 1]["deaths"]) + '\n'
        todayConfirmed = self.data[country][len(self.data[country]) - 1]["confirmed"] - self.data[country][len(self.data[country]) - 2]["confirmed"]
        todayDeaths = self.data[country][len(self.data[country]) - 1]["deaths"] - self.data[country][len(self.data[country]) - 2]["deaths"]
        info += "Confirmed Today: " + str(todayConfirmed) + '\n'
        info += "Confirmed Deaths: " + str(todayDeaths) + '\n'

        return info

    def listCountries(self):
        countryList = []
        for country in self.data:
            countryList.append(country)
        return countryList

    def getDate(self):
        return datetime.today().strftime('%Y-%m-%d')
