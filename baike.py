from Callable import Callable
from google.appengine.api import channel
from bs4 import BeautifulSoup as BS
from google.appengine.ext import db
from model import Picograph

import os, json, datetime, logging
import urllib
import requests
import hashlib

class WikiParser:
    def __init__(self, url, query):
        self.searchTerm = query['searchTerm'] 
        self.searchType = query['searchType']
        self.url = url

    def loadFromDataStore(self, url):
        q = Picograph.all()
        q.filter('src =', url)
        q.filter('funcName =', self.parseTOC.__name__)
        picograph = q.get()
    
    def parseInfoBox(self, soup, options):
        content = ''

        infoBox = soup.select('.infobox')
        if not infoBox:
            return None

        infoBox = infoBox[0] 
        #infoBox.img.extract() #removing img references
        content += str(infoBox)
         
        return {'cardId': self.searchTerm+'_'+self.searchType, #if generated, update this box
                'cardType': 'infoBox', #content type - media etc.
                'cardTitle': '&nbsp;'+self.searchTerm.title(), 
                'cardRating': -1, #rating 
                'cardSrc': self.url,
                'cardContent': content,
                'editable': True, #user can update
                'hashId': 'pi'+self.url #unique hash of this picograph
        }

    def parseTOC(self, soup, options):
        tocLevel1 = soup.select('.toclevel-1')
        content = []

        if not tocLevel1:
            return None
        for tocs in tocLevel1:
            for toc in tocs.select('.toctext'):
                content.append(toc.string)
         
        return {'cardId':  self.searchTerm+'_'+self.searchType, #if generated, update this box
                'cardType': '', #content type - media etc.
                'cardTitle': '&nbsp;Details', 
                'cardRating': -1, #rating 
                'cardSrc': self.url,
                'cardContent': content,
                'editable': False, #user can update
                'hashId': 'pt'+self.url #unique hash of this picograph
        }

    def parseCitedInfo(self,soup, options, url):
        content = ''
        refs = soup.select('.reference')

        if len(refs) == 0:
            return None
        
        for ref in refs:
            content += str(ref.parent())

        return {'color':'','size': 'small','content':content}#.encode('utf-8')

    def loadContent(query, rpc, url, channelName):
        self = WikiParser(url, query)

        try:
            #should check whether to update entry or just load past data
            result = requests.get(url)

            #if not successful, count as failure
            if result.status_code != 200: 
                raise requests.exceptions.RequestException
            
            soup = BS(result.text)         

            content = self.parseInfoBox(soup, {})
            logging.error(str(content))
            if content: channel.send_message(channelName, json.dumps(content))

            content = self.parseTOC(soup, {})
            if content: channel.send_message(channelName, json.dumps(content))

        except requests.exceptions.RequestException: #failed or timed out
            logging.error('Wiki load failed') 
            return None 

    loadContent = Callable(loadContent)
    
    def getName():
        return "wikipedia"
    getName = Callable(getName)

