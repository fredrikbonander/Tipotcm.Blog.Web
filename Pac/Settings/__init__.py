__author__ = 'broken'

#!/usr/bin/python
# -*- coding: utf-8 -*-

# page settings
markets = [{ 'language' : 'en-us', 'currency' : '$' }, { 'language' : 'se-sv', 'currency' : 'SEK' }]
memcacheTimeout = 36000
forceMemcacheRefresh = False
host = 'http://localhost:8080'
secureHost = 'http://localhost:8080'

def getCurrencyByLanguage(language):
    for market in markets:
        if market['language'] == language:
            return market['currency']

    return None