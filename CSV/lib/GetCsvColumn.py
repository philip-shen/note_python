# pilicurg / GetCsvColumn 
# https://github.com/pilicurg/GetCsvColumn/blob/master/demo.py

__author__ = 'www.lfhacks.com'

EXCLUDE_SIGN = '~'
EXCLUDE = lambda x: EXCLUDE_SIGN + str(x)

import csv
import re

class CsvFile(object):
    '''get columns from a comma separated values(csv) file, providing various filter'''
    def __init__(self, filename):
        self._name = filename
        self._header_list = []
        self._dataDict = {}
        self._open_file(self._name)

    def _get_data_dict(self, reader):
        datadict = {}
        for headerindex, column in enumerate(zip(*reader)):
            datadict[self._header_list[headerindex]] = column

        return datadict
    '''
    python csv2libsvm.py: AttributeError: '_csv.reader' object has no attribute 'next'
    https://stackoverflow.com/questions/42767250/python-csv2libsvm-py-attributeerror-csv-reader-object-has-no-attribute-nex

     write next(reader) instead of reader.next() 
    '''
    def _open_file(self, filename):
        with open(filename) as csvfile:
            reader = csv.reader(csvfile)
            self._header_list = next(reader);#reader.next()
            self._dataDict = self._get_data_dict(reader)

    def get_column(self, *header_list, **rule_dict):
        includelist, excludelist, converttype = self._reformat_rule_dict(rule_dict)

        if len(header_list) == 1:
            return self._filter_column(header_list[0], includelist, excludelist, converttype)
        elif len(header_list) > 1:
            return [self._filter_column(header, includelist, excludelist, converttype) for header in header_list]
        else:
            raise Exception('Empty header list!')
    '''
    Error: “ 'dict' object has no attribute 'iteritems' ”
    https://stackoverflow.com/questions/30418481/error-dict-object-has-no-attribute-iteritems

    use dict.items() instead of dict.iteritems()
    '''
            
    def _reformat_rule_dict(self, rule_dict):
        convertType = rule_dict.pop('CONVERT', None)

        seqmatch = re.compile(r'^(\[|\().*(\]|\))$')

        includedict = {}
        #for key, value in rule_dict.iteritems():
        for key, value in rule_dict.items():
            if str(value)[0] != EXCLUDE_SIGN:
                if type(value) is list:
                    includedict[key] = value
                else:
                    includedict[key] = [value]

        excludedict = {}
        #for key, value in rule_dict.iteritems():
        for key, value in rule_dict.items():
            if str(value)[0] == EXCLUDE_SIGN:
                value = str(value).lstrip(EXCLUDE_SIGN)
                if seqmatch.match(value):
                    excludedict[key] = eval(value)
                else:
                    excludedict[key] = [value]

        #includelist = tuple([{key: str(v)} for key, value in includedict.iteritems() for v in value])
        #excludelist = tuple([{key: str(v)} for key, value in excludedict.iteritems() for v in value])
        includelist = tuple([{key: str(v)} for key, value in includedict.items() for v in value])
        excludelist = tuple([{key: str(v)} for key, value in excludedict.items() for v in value])

        return includelist, excludelist, convertType

    def _filter_column(self, header, includelist, excludelist, convertType):
        if header not in self._header_list:
            raise Exception('column \"%s\" not found in %s.' % (header, self._name))

        '''
        TypeError: 'dict_keys' object does not support indexing
        https://stackoverflow.com/questions/17322668/typeerror-dict-keys-object-does-not-support-indexing

        python2.x (when d.keys() returned a list). 
        With python3.x, d.keys() returns a dict_keys object which behaves a lot more like a set than a list. As such, it can't be indexed.

        The solution is to pass list(d.keys()) (or simply list(d)) to shuffle.
        '''
        #include_unique_keys = list(set([d.keys()[0] for d in includelist]))
        #exclude_unique_keys = list(set([d.keys()[0] for d in excludelist]))
        include_unique_keys = list(set([ list(d.keys())[0] for d in includelist]))
        exclude_unique_keys = list(set([ list(d.keys())[0] for d in excludelist]))
        columnarray = []
        for index, data in enumerate(self._dataDict[header]):
            for key in include_unique_keys:
                rowinclude = {key: self._dataDict[key][index]}
                if rowinclude not in includelist:
                    break
            else:
                for key in exclude_unique_keys:
                    rowexclude = {key: self._dataDict[key][index]}
                    if rowexclude in excludelist:
                        break
                else:
                    columnarray.append(convertType(data) if convertType is not None else data)

        return tuple(columnarray)