import requests
import json

api_key = '9147c5de-b3b6-4002-b254-8b224a3603e0'
uri = 'https://geocode-maps.yandex.ru/1.x/?'

with open('cities.json', 'r') as read_file:
    data = json.load(read_file)

with open('covidMap.json', 'w', encoding='utf8') as output_file:
    features = []

    covidMap = {
        "type": "FeatureCollection",
        # "metadata": {
        #     "name": "COVID-19 L0",
        #     "creator": "Yandex Map Constructor"},
        "features": features
    }

    for elem in data:
        PARAMS = {
            "geocode": 'Ленинградская область, ' + elem['city'],
            "apikey": api_key,
            "format": 'json'
        }
        resp = requests.get(uri, params = PARAMS)
        json_data = resp.json()
        coordinates = json_data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"]["pos"].split(" ")
        features.append({   'type': "Features", 
                            'geometry': {
                                'type': "Point", 
                                'coordinates': coordinates},
                            'properties': {
                                'iconCaption': elem['city'],
                                'iconContent': elem['peopleIll'],
                                'marker-color': "#ed4543"
                            }
                        })
    json.dump(covidMap, output_file, ensure_ascii=False)