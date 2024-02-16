import requests, json
from datetime import datetime

API_URL = "https://api.punkapi.com/v2/beers"
API_PROPERTIES = ["ibu", "target_fg", "target_og", "ebc",
                  "srm", "ph", "attenuation_level", "volume",
                  "boil_volume", "method", "ingredients",
                  "brewers_tips", "contributed_by"]

resp = requests.get(API_URL)
beers = resp.json()

for beer in beers:
    for prop in API_PROPERTIES:
        del beer[prop]

    beer["first_brewed"] = datetime.strptime(beer["first_brewed"], "%m/%Y")

writeFile = open('beers.json', 'w')
json.dump(beers, writeFile)
writeFile.close()
