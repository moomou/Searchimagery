from Callable import Callable
from google.appengine.api import channel
from bs4 import BeautifulSoup as BS
from google.appengine.ext import db
from model import Picograph

import os, json, datetime, logging
import requests
import hashlib

class JLyricParser:
    def __init__(self, url, query):
        self.searchTerm = query['searchTerm'] 
        self.searchType = query['searchType']
        self.url = url

    def parseLyric(self, soup, options, url):
        content = ''
        lyric = soup.select('#lyricBody')

        if not lyric:
            return None

        lyric = lyric[0]
        content += str(lyric)

        return {'cardId': 'lyric', #if generated, update this box
                'cardType': 'lyric', #content type - media etc.
                'cardTitle': self.searchTerm.title(), 
                'cardRating': -1, #rating 
                'cardSrc': self.url,
                'cardContent': content,
                'editable': True ,#user can update
                'hashId': 'pl'+self.url, #unique hash of this picograph
        }

    def loadContent(query, rpc, url, channelName):
        self = JLyricParser(url, query)
        try:
            #should check whether to update entry or just load past data
            result = requests.get(url)

            #if not successful, count as failure
            if result.status_code != 200: 
                raise requests.exceptions.RequestException

            soup = BS(result.text)         

            content = self.parseLyric(soup, {}, url) 
            if content: channel.send_message(channelName, json.dumps(content))

        except requests.exceptions.RequestException: #failed or timed out
            logging.error('Wiki load failed') 
            return None 

    loadContent = Callable(loadContent)
        
    def getName():
        return "jlyric"
    getName = Callable(getName)

