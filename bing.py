import requests
import json
import urllib
import urllib2
import logging
from base64 import b64encode

class Bing:
    def __init__(self):
        self.searchURL = "https://api.datamarket.azure.com/Data.ashx/Bing/Search/v1/"
        self.safetySettings = "&Adult=%27Moderate%27"
        self.defaultWebSearchOptions = "&$top=50&$format=json"
        self.defaultImageSearchOptions = "&$skip=1&$top=10&$format=json"

        self.username = ""
        self.accountKey = "wXZ58kaKOzp2znC2Y39f/O6XgUz0atUch20HUv008lQ="
        self.accountKey2 = "Ybv/NkhAYwLRaIjOl7MrRnVZkWdEx3cWSe+3FfBLiTE="

        self.locationFilter = {u'CA':'en-CA',
                                u'US':'en-US',
                                u'JP':'ja-JP',
                                u'TW':'zh-TW',
                                u'RD':'en-US',
                                u'CN':'zh-CN'}

    def __encode(self, param, value):
        value = value.rstrip()
        return urllib.urlencode({param: "'" + value + "'"})

    def __encodeQuery(self,query):
        logging.error("Query: "+query)
        return self.__encode("Query", query)
    
    def __sendQuery(self,searchURL):
        logging.info('Requesting: '+searchURL)
        request = urllib2.Request(searchURL)
        request.add_header('Authorization', 'Basic ' + b64encode(self.accountKey + ':' + self.accountKey))
        r = urllib2.urlopen(request)
        result = json.loads(r.read())
        return result

    def getLocationFilter(self, countryCode):
        locFilter = self.__encode('Market', self.locationFilter[countryCode.upper()])
        return '&'+locFilter 

    def searchWeb(self,query,options=None):
        query = self.__encodeQuery(query)

        searchURL = self.searchURL + \
                     "Web?" + \
                     query +  \
                     self.getLocationFilter(options['location']) + \
                     self.safetySettings + \
                     self.defaultWebSearchOptions;
        logging.info(searchURL)

        return self.__sendQuery(searchURL)

    def searchImage(self,query,options=None):
        imageFilters = ""

        if filter in options:
            imageFilters = '&' + \
                        urllib.urlencode({'ImageFilters':options['filter']});

        query = self.__encodeQuery(query)
    
        searchURL = self.searchURL + \
                    "Image?" + \
                    query + \
                    self.getLocationFilter(options['location']) + \
                    self.safetySettings + \
                    imageFilters + \
                    self.defaultImageSearchOptions;
        logging.info(searchURL)

        return self.__sendQuery(searchURL)
