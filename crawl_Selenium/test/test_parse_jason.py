import json
from pprint import pprint

with open('config.json') as f:
    data = json.load(f)

#pprint(data)
#pprint(data["WLANtoLAN"][0]["test_case"]["id"])
#pprint(data["WLANtoLAN"][0]["test_case"]["description"])
pprint(type(data["WLANtoLAN"][0]["test_case"]))
for key, value in data["WLANtoLAN"][0]["test_case"].items():
    print(key,value)
#pprint(json.dumps(data, indent=4)) 