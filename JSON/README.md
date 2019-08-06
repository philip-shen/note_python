# note of_JSON
Take some note of JSON

# Table of Content

# 


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