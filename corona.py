import requests

url = "https://pomber.github.io/covid19/timeseries.json"
r = requests.get(url = url)
data = r.json()


for i in range(71):
    if data["Turkey"][i]["date"] == "2020-3-31":
        print(data["Turkey"][i]['date'])
        print(data["Turkey"][i]['confirmed'])

'''
i=63
print(data["Turkey"][i]['confirmed'])
'''
