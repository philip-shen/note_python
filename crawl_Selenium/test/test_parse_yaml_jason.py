import json,yaml
import io
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

class trail_yaml():
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def read_yaml(self,*args):
        read_file_name = args[0]
        # Read YAML file
        with io.open(read_file_name, 'r', encoding='utf8') as stream:
            data_loaded = yaml.safe_load(stream)    
        
        return data_loaded        

    def write_yaml(self,*args):
        # Write YAML file
        out_file_name = args[0];#'data.yaml'
        data_input = args[1];#data
        with io.open(out_file_name, 'w', encoding='utf8') as outfile:
            yaml.dump(data_input, outfile, default_flow_style=False, allow_unicode=True)   
        
        #pprint('Write data to:',out_file_name)     

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

# Define data
data = {'a list': [1, 42, 3.141, 1337, 'help', u'€'],
        'a string': 'bla',
        'another dict': {'foo': 'bar',
                         'key': 'value',
                         'the answer': 42}}

local_trail_yaml=trail_yaml()
#local_trail_yaml.write_yaml('data.yaml',data)
data_loaded = local_trail_yaml.read_yaml('data.yaml')
pprint(data_loaded)    