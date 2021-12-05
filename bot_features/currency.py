import http.client
import json

from yaml import safe_load


class Currency:
    def __init__(self):
        self.token = self.setToken()

    def setToken(self):
        with open("env.yaml", encoding="utf-8") as env:
            config = safe_load(env)
            return config["CURRENCY"]

    def getInfo(self, currency):
        currency = currency.upper()
        conn = http.client.HTTPSConnection("api.collectapi.com")

        headers = {
            'content-type': "application/json",
            'authorization': self.token
        }

        conn.request("GET", "/economy/singleCurrency?int=10&tag={}".format(currency), headers=headers)

        res = conn.getresponse()
        data = res.read()
        dataDict = json.loads(data.decode("utf-8"))
        buying = dataDict['result'][0]['buying']
        selling = dataDict['result'][0]['selling']
        rate = dataDict['result'][0]['rate']
        info = 'Buying: ' + str(buying) + '\n'
        info += 'Selling: ' + str(selling) + '\n'
        info += 'Rate: ' + str(rate)
        return info

    def getInfoWithAmount(self, amount, currency):
        amount = amount.upper()
        currency = currency.upper()
        conn = http.client.HTTPSConnection("api.collectapi.com")

        headers = {
            'content-type': "application/json",
            'authorization': self.token
        }

        conn.request("GET", "/economy/singleCurrency?int=10&tag={}".format(currency), headers=headers)

        res = conn.getresponse()
        data = res.read()
        dataDict = json.loads(data.decode("utf-8"))
        buying = dataDict['result'][0]['buying'] * float(amount)
        selling = dataDict['result'][0]['selling'] * float(amount)
        rate = dataDict['result'][0]['rate']
        info = 'Buying: ' + str(buying) + '\n'
        info += 'Selling: ' + str(selling) + '\n'
        info += 'Rate: ' + str(rate)
        return info

    def exchangeWith(self, amount, xfrom, to):
        import http.client
        xfrom = xfrom.upper()
        to = to.upper()
        conn = http.client.HTTPSConnection("api.collectapi.com")

        headers = {
            'content-type': "application/json",
            'authorization': self.token
        }

        conn.request("GET", "/economy/exchange?int=10&to={}&base={}".format(to, xfrom), headers=headers)

        res = conn.getresponse()
        data = res.read()
        dataDict = json.loads(data.decode("utf-8"))
        calculated = float(dataDict['result']['data'][0]['rate']) * float(amount)
        rate = dataDict['result']['data'][0]['rate']
        info = 'Calculated: ' + str(calculated) + '\n'
        info += 'Rate: ' + str(rate)
        return info
