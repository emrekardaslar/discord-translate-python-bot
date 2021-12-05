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


