from bs4 import BeautifulSoup as BS
from collections import defaultdict
from HTMLParser import HTMLParser
from bing import Bing

import logging
import re 
import tldextract

SEARCH_IMAGE = "image"; 
SEARCH_WEB = "web"; 
SEARCH_VIDEO = "video";

IMAGE_FILTER = {'person': "'"+'Face:Face+Face:Portrait'+"'",
                 'place': '',
                 'entity': ''}

class SearchEngine:
    def __init__(self):
        self.searchType = {SEARCH_IMAGE:self.__searchImage,
                            SEARCH_WEB:self.__searchWeb}
        self.bing = Bing()

    def __searchImage(self, query, options=None):
        imageFilter = ''

        if options and options['searchEntity']: 
            options['filter'] = IMAGE_FILTER[options['searchEntity']]

        result = self.bing.searchImage(query, options)

        return {'url':result[u'd'][u'results']}

    def __searchWeb(self, query, options=None):
        result = self.bing.searchWeb(query, options)
        websites, allURL = [], defaultdict(list)

        for entry in result[u'd'][u'results']:
            entryURL = entry[u'Url']
            urlObj = tldextract.extract(entryURL)
            siteName = urlObj.domain
            
            if not siteName:
                continue # ignoring anything that fails parser
            else:
                allURL[siteName.lower()].append(entryURL) 
                websites.append(entryURL)
        
        return {'ranking':allURL, 'url':websites}

    def search(self, query, options=None):
        '''returns a list of URLs from search engine result'''
        result = {SEARCH_IMAGE:None,
                  SEARCH_WEB:None}

        query += " "+options['searchEntity']

        if options and 'type' in options:
            for searchType in options['type']:
                result[searchType] = self.searchType[searchType](query, options)     
        else:
            for searchType in result:
                result[searchType] = self.searchType[searchType](query, options) 
        return result
