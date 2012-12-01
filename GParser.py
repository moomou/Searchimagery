from bs4 import BeautifulSoup as BS
import logging
import lxml
import operator
import urllib,urllib2
import re 
import tldextract

from google.appengine.api import urlfetch
from collections import defaultdict
from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

SEARCHURL = "http://www.google.com/search?"
DOMAIN_NAME_REGEX = re.compile("s/[^/]*\/\/\([^@]*@\)\?\([^:/]*\).*/\2/")

class GParser:
    def cleanURL(self, inputURL):
        return inputURL.strip('/url?q=').split(',')[0].split('&sa=')[0]

    def __init__(self,searchTerm):
        logging.info(SEARCHURL+searchTerm)
        req = urllib2.Request(SEARCHURL+searchTerm,
                headers={'User-Agent' : "Magic Browser"})
        try:
            con = urllib2.urlopen(req)
            result = con.read() #eventually want to clean up data a bit 
            self.html = result
            self.soup = BS(result) #GParser is parsing Google search result
            self.allURLs = defaultdict(list)
            
        except urllib2.URLError, e:
            self.html = "ERROR: "+str(e)
            logging.error(self.html)

    def parse(self):
        pass

    def getSiteName(self,url):
        URLParts = url.split(".")

        if len(URLParts) < 2:
            return None 

        return URLParts[-2]

    def getURLs(self,target):
        logging.info(target.lower)
        logging.info(self.allURLs.keys)

        if target.lower() in self.allURLs:
            return self.allURLs[target]
        return None

    def getListOfEntry(self):
        logging.info('In getListOfEntry')
        websites = {}

        #tags = self.soup.find_all('div', {'class':'vsc'}) 
        tags = self.soup.find_all('h3', {'class':'r'}) 
        logging.info(tags)

        for tag in tags: 
            #tag = tag.find('h3', {'class':'r'}).a.href
            #tagString = tag.extract() 
            #fullWebURL = strip_tags(str(tagString))

            fullWebURL = tag.find('a')['href']  
            fullWebURL = self.cleanURL(fullWebURL)
            urlObj = tldextract.extract(fullWebURL) 

            faviconURL = urlObj.domain+'.'+urlObj.tld
            if urlObj.subdomain: faviconURL = urlObj.subdomain+'.'+faviconURL

            logging.info(fullWebURL)
            logging.info(faviconURL) 

            siteName = urlObj.domain 

            if not siteName:
                continue    
            else:
                self.allURLs[siteName.lower()].append(fullWebURL)

            if websites.has_key(siteName):
                websites[siteName]['count'] += 1
            else:
                websites[siteName] = {'count':1,'favicon': faviconURL} 

        websites = sorted(websites.items(), key=operator.itemgetter(1))
        return websites
