import requests
import json

API_URL = "https://api.punkapi.com/v2/beers"
API_PROPERTIES = ["ibu", "target_fg", "target_og", "ebc",
                  "srm", "ph", "attenuation_level", "volume",
                  "boil_volume", "method", "ingredients",
                  "brewers_tips", "contributed_by"]

resp = requests.get(API_URL)
beers = resp.json()
beer_fixture = []

for beer in beers:
    pk = 1
    for prop in API_PROPERTIES:
        del beer[prop]
    beer_fixture.append(
        {"model": "catalog.Beer",
         "pk": pk,
         "fields": beer})
    pk += 1

writeFile = open('beers.json', 'w')
json.dump(beer_fixture, writeFile)
writeFile.close()
