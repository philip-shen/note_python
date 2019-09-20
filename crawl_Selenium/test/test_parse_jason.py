import json
from pprint import pprint

with open('config.json') as f:
    data = json.load(f)

#https://stackoverflow.com/questions/5710391/converting-python-dict-to-kwargs
def trail_jsaon(**kwargs):
    #for arg in kwargs.values():
    #    pprint(arg)
    
    #for arg in kwargs:
    #    pprint(arg+':'+kwargs[arg])    

    #pprint(kwargs)
    pprint(kwargs['test_case']['description'])
    pprint(kwargs['dut'])
    pprint(kwargs['wifi_2g']['ssid'])
    pprint(kwargs['wifi_5g']['ssid'])

#pprint(data)
#pprint(data["WLANtoLAN"][0]["test_case"]["id"])
#pprint(data["WLANtoLAN"][0]["test_case"]["description"])
pprint(data["DUT_Config_WLAN"][0]["wifi_2g"])
pprint(type(data["DUT_Config_WLAN"][0]["wifi_2g"]))

#trail_jsaon(**data["DUT_Config_WLAN"][0]["wifi_2g"])
trail_jsaon(**data["DUT_Config_WLAN"][0])

pprint(data["DUT_Config_WLAN"][0]["dut"]["lan_ip_address"])
pprint(len(data["DUT_Config_WLAN"][0]["dut"]["lan_ip_address"]))
#pprint(type(data["WLANtoLANtoWLAN"][0]["test_case"]))
for key, value in data["DUT_Config_WLAN"][0]["test_case"].items():
    print(key,value)
#pprint(json.dumps(data, indent=4)) 