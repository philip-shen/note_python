# note of YAML and JSON
Take some note of YAML and JSON

# Table of Content  
[What is the difference between YAML and JSON?](#what-is-the-difference-between-yaml-and-json?)

[How to use JSON with Python](#how-to-use-json-with-python)  
[Writing a JSON file](#writing-a-json-file)  
[Reading JSON](#reading-json)  

[Python JSON: Encode(dump), Decode(load) json Data & File (Example)]()  

# What is the difference between YAML and JSON?  
[What is the difference between YAML and JSON? Jun 7, 2013](https://stackoverflow.com/questions/1726802/what-is-the-difference-between-yaml-and-json)  
```
Technically YAML is a superset of JSON. This means that, in theory at least, a YAML parser can understand JSON, but not necessarily the other way around.

See the official specs, in the section entitled "YAML: Relation to JSON".

In general, there are certain things I like about YAML that are not available in JSON. 
```
[YAML: Relation to JSON](http://yaml.org/spec/1.2/spec.html#id2759572)  
## How can I parse a YAML file in Python  
[How can I parse a YAML file in Python ](https://stackoverflow.com/questions/1773805/how-can-i-parse-a-yaml-file-in-python)  
```
#!/usr/bin/env python

import yaml

with open("example.yaml", 'r') as stream:
    try:
        print(yaml.safe_load(stream))
    except yaml.YAMLError as exc:
        print(exc)
```

```
# -*- coding: utf-8 -*-
import yaml
import io

# Define data
data = {'a list': [1, 42, 3.141, 1337, 'help', u'€'],
        'a string': 'bla',
        'another dict': {'foo': 'bar',
                         'key': 'value',
                         'the answer': 42}}

# Write YAML file
with io.open('data.yaml', 'w', encoding='utf8') as outfile:
    yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)

# Read YAML file
with open("data.yaml", 'r') as stream:
    data_loaded = yaml.safe_load(stream)

print(data == data_loaded)
```

## When to use YAML instead of JSON  
[When to use YAML instead of JSON May 23, 2017](https://stackoverflow.com/questions/18395623/when-to-use-yaml-instead-of-json)
```
JSON is more formal format than YAML. IMHO:

    YAML is better for fast creation and understanding of simple configuration files of software modules;

    JSON is better for fast implementation and implementation of simple data transfering between software modules.
```

# How to use JSON with Python  
[How to use JSON with Python 06 Apr 2019](https://developer.rhino3d.com/guides/rhinopython/python-xml-json/)  
## Writing a JSON file  
```
Not only can the json.dumps() function convert a Python datastructure to a JSON string, 
but it can also dump a JSON string directly into a file. Here is an example of writing a structure above to a JSON file:
```
```
#Get the file name for the new file to write
filter = "JSON File (*.json)|*.json|All Files (*.*)|*.*||"
filename = rs.SaveFileName("Save JSON file as", filter)

# If the file name exists, write a JSON string into the file.
if filename:
    # Writing JSON data
    with open(filename, 'w') as f:
        json.dump(datastore, f)
```

## Reading JSON  
```
Reading in a JSON file uses the json.load() function.
```
```
import rhinoscriptsyntax as rs
import json

#prompt the user for a file to import
filter = "JSON file (*.json)|*.json|All Files (*.*)|*.*||"
filename = rs.OpenFileName("Open JSON File", filter)

#Read JSON data into the datastore variable
if filename:
    with open(filename, 'r') as f:
        datastore = json.load(f)

#Use the new datastore datastructure
print datastore["office"]["parking"]["style"]
```
[How to read and write a simple file 05 Dec 2018](https://developer.rhino3d.com/guides/rhinopython/python-reading-writing/)  

# Python JSON: Encode(dump), Decode(load) json Data & File (Example)   
[Python JSON: Encode(dump), Decode(load) json Data & File (Example) ](https://www.guru99.com/python-json.html)  

Python to JSON (Encoding)

Python | JSON
------------------------------------ | ---------------------------------------------
dict | Object
list | Array
unicode | String
number - int, long | number – int
float | number – real
True | True
False | False
None | Null 

# Reference
* [Why can't Python parse this JSON data? Mar 19, 2019](https://stackoverflow.com/questions/2835559/why-cant-python-parse-this-json-data)  
```

Your data is not valid JSON format. You have [] when you should have {}:

    [] are for JSON arrays, which are called list in Python
    {} are for JSON objects, which are called dict in Python

Then you can use your code:

import json
from pprint import pprint

with open('data.json') as f:
    data = json.load(f)

pprint(data)

With data, you can now also find values like so:

data["maps"][0]["id"]
data["masks"]["id"]
data["om_points"]  
```

* [JSON ValueError: Expecting property name: line 1 column 2 (char 1) Apr 13, 2016](https://stackoverflow.com/questions/25707558/json-valueerror-expecting-property-name-line-1-column-2-char-1)  
```
json.loads will load a json string into a python dict, json.dumps will dump a python dict to a json string, for example:

>>> json_string = '{"favorited": false, "contributors": null}'
'{"favorited": false, "contributors": null}'
>>> value = json.loads(json_string)
{u'favorited': False, u'contributors': None}
>>> json_dump = json.dumps(value)
'{"favorited": false, "contributors": null}'
```

* [Loading Dirty JSON With Python 24 April 2016](https://grimhacker.com/2016/04/24/loading-dirty-json-with-python/)  
```
ValueError: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)

This is because,  despite first appearances, the data I was trying  to extract was a python object built from strings, lists, integers, floats, and dictionaries which had been passed to the ‘print’ statement. But it was quite close to JSON so I decided that the best course of action in this instance was to ‘fix’ the data so that I could load it as JSON.

First, as the error above indicates, double quotes are required, not the single quotes mostly (but not always prefixed with a ‘u’  (indicating unicode) which my data had.

After removing these I encountered the error:

ValueError: No JSON object could be decoded

This thoroughly unhelpful error sent me scurrying to Google. Apparently this error is thrown in a variety of situations, but the one relevant to my data was the case of the boolean key words (True and False) in python they are capitalised, but in JSON they need to be lowercase. (This error is also thrown when there are trailing commas in lists).

I used regular expression substitution to implement these alterations. I decided to share these few lines of code for my future self and anyone else who may find it useful. (Note that this worked for my use case, but as soon as exceptions stopped being thrown I moved on. Therefore it may not be a robust or complete solution. You have been warned.)

import re
import json

def load_dirty_json(dirty_json):
    regex_replace = [(r"([ \{,:\[])(u)?'([^']+)'", r'\1"\3"'), (r" False([, \}\]])", r' false\1'), (r" True([, \}\]])", r' true\1')]
    for r, s in regex_replace:
        dirty_json = re.sub(r, s, dirty_json)
    clean_json = json.loads(dirty_json)
    return clean_json
```

* []()  
![alt tag]()

# h1 size

## h2 size

### h3 size

#### h4 size

##### h5 size

*strong*strong  
**strong**strong  

> quote  
> quote

- [ ] checklist1
- [x] checklist2

* 1
* 2
* 3

- 1
- 2
- 3