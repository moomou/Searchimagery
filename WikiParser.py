from bs4 import BeautifulSoup as BS

from Callable import Callable
from google.appengine.api import channel
from google.appengine.ext import db

import model
import re, os, json, datetime, logging, hashlib
import urllib, requests

class WikiParser:
    def __init__(self, url, query):
        self.searchTerm = query['searchTerm'] 
        self.searchEntity = query['searchEntity']
        self.url = url

        self.cardId = self.searchTerm + \
                      self.searchEntity + \
                      hashlib.md5(self.url).hexdigest()[0:5]

    def getSearchEntry(self):
        dbWrapper = model.DataStoreWrapper()
        searchEntry = dbWrapper.search(model.SearchEntry, 
                                     {'searchTerm': self.searchTerm,
                                      'searchEntity': self.searchEntity})
        return searchEntry 
    
    def storePicograph(self, funcName, content, jsonContent, searchEntry):
        pico = model.Picograph()

        pico.searchEntry = searchEntry
        pico.srcUrl = self.url
        pico.funcName = funcName

        pico.title = content['cardTitle']
        pico.content = jsonContent

        pico.rating = content['cardRating']
        pico.put()
        
        return pico

    def parseInfoBox(self, soup, options):
        content = ''

        infoBox = soup.select('.infobox')

        if not infoBox:
            return None

        infoBox = infoBox[0] 
        content += str(infoBox)
         
        return {'cardId': 'infoBox'+self.cardId,
                'cardType': 'infoBox', #content type - media etc.
                'cardTitle': '&nbsp;'+self.searchTerm.title(), 
                'cardRating': 0, #rating 
                'cardSrc': self.url,
                'cardContent': content,
                'editable': False, #user can update
                'hashId': 'pi'+self.url #unique hash of this picograph
        }

    def parseIntro(self, soup, imageURLs, options):
        content = ''
        pCount = 0;
        for child in soup.select('#mw-content-text')[0].contents:
            if hasattr(child,'name'):
                if child.name == "p":
                    content += child.get_text() + "<br><br>"
                    pCount += 1
                    if pCount > 3: break
        
        content = re.sub('\[.*?\]', '', content)

        if len(imageURLs) != 0:
            img = '<div class="outer">' + \
                    '<img class="inner" src="'+imageURLs[0]['Thumbnail']['MediaUrl']+'"></img>' + \
                  '</div>'
            img = img.encode('ascii')
            content = img + '<br><br>' + content

        content = content

        return {'cardId': 'intro'+self.cardId, #if generated, update this box
                'cardType': 'intro', #content type - media etc.
                'cardTitle': '&nbsp;'+self.searchTerm.title(), 
                'cardRating': 0, #rating 
                'cardSrc': self.url,
                'cardContent': content, 
                'editable': False, #user can update
                'hashId': 'intro-'+self.url #unique hash of this picograph
        }

    def parseTOC(self, soup, options):
        tocLevel1 = soup.select('.toclevel-1')
        content = []

        if not tocLevel1:
            return None
        for tocs in tocLevel1:
            for toc in tocs.select('.toctext'):
                content.append(toc.string)
         
        return {'cardId': 'toc'+self.cardId, 
                'cardType': 'toc', #content type - media etc.
                'cardTitle': '&nbsp;Details', 
                'cardRating': 0, #rating 
                'cardSrc': self.url,
                'cardContent': ' '.join(content),
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

    def loadContent(query, rpc, url, imageURLs, channelName):
        try:
            #should check whether to update entry or just load past data
            result = requests.get(url)
            #if not successful, count as failure
            if result.status_code != 200: 
                raise requests.exceptions.RequestException
            
            soup = BS(result.text)         
            self = WikiParser(url, query)
            searchResultRef = self.getSearchEntry()
            content = self.parseInfoBox(soup, {})

            if content: 
                jsonContent = json.dumps(content)
                channel.send_message(channelName, jsonContent) 
                picoRef = self.storePicograph(self.parseInfoBox.func_name,
                                         content, 
                                         jsonContent, 
                                         searchResultRef)

            content = self.parseIntro(soup, imageURLs, {})
            if content: 
                jsonContent = json.dumps(content)
                channel.send_message(channelName, jsonContent) 
                picoRef = self.storePicograph(self.parseIntro.func_name,
                                         content, 
                                         jsonContent, 
                                         searchResultRef)

            content = self.parseTOC(soup, {})
            if content: 
                jsonContent = json.dumps(content)
                channel.send_message(channelName, jsonContent) 
                picoRef = self.storePicograph(self.parseTOC.func_name,
                                         content, 
                                         jsonContent, 
                                         searchResultRef)

        except requests.exceptions.RequestException: #failed or timed out
            logging.error('Wiki load failed') 
            return None 
    loadContent = Callable(loadContent)
    
    def getName():
        return "wikipedia"
    getName = Callable(getName)
