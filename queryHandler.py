import webapp2
import urllib, urllib2, requests
import markupsafe
import os, json, datetime, logging

import model

from webapp2_extras import sessions
from google.appengine.api import channel 

from searchimagery import ScriptEngine 
from searchEngine import SearchEngine
from geolocation import Geolocation 
from YoutubeSearch import YtubeSearch 

geolocation = Geolocation()
searchEngine = SearchEngine()
dbWrapper = model.DataStoreWrapper 

class QueryHandler(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)
        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    def getSession(self):
        return self.session_store.get_session('default',backend="datastore")

    #used to establish a channel
    def post(self):
        self.createChannel()

    #parse query and write to channel
    def get(self):
        searchType = self.request.get('cmd','general')
        funcs = {'ytube':self.ytubeQuery,
                 'gen':self.parseQuery}

        if searchType in funcs:
            funcs[searchType]()
        else:
            funcs['gen']()

    def createChannel(self):
        #eventually need a sessionId from client
        uniqueId = self.request.get('id')
        token = channel.create_channel(uniqueId)
        self.response.out.write(json.dumps({'channelToken':token,
                                            'channelName': uniqueId}))

    def ytubeQuery(self):
        searchTerm = self.request.get('q')
        channelName = self.request.get('channelName')
        query = {'searchTerm':searchTerm, 'searchType':'lyric'}

        if not channelName:
            logging.error("ERROR: No channel found")
            self.response.out.write("ERROR: No channel found")
            return

        searchEngineResult = self.webSearch(searchTerm, "lyric")
        ScriptEngine.exeAll(query, searchEngineResult, channelName)

    def parseQuery(self):
        searchTerm = self.request.get('q')
        channelName = self.request.get('channelName')
        query = {'searchTerm':searchTerm, 'searchEntity':''}

        if not channelName:
            logging.error("ERROR: No channel found")
            self.response.out.write("ERROR: No channel found")
            return
        
        searchResultEntry = dbWrapper.search(model.SearchEntry, 
                                             {'searchTerm': searchTerm,
                                              'searchEntity': ''})
        
        if searchResultEntry:
            logging.info(searchResultEntry.searchTerm)

            for picograph in searchResultEntry.picographs:
                logging.info(picograph.rating)
                channel.send_message(channelName, picograph.content)
        else:
            newSearchEntry = model.SearchEntry()
            newSearchEntry.searchTerm = searchTerm
            newSearchEntry.searchEntity = '' 

            newSearchEntry.put()

            searchEngineResult = self.webSearch(searchTerm) #+ image
            ScriptEngine.exeAll(query, searchEngineResult, channelName)
        
        #if searchTerm is a celebrity, search video 
        youtubeResult = self.getYoutubePlaylist(searchTerm) #youtube
        channel.send_message(channelName, json.dumps(youtubeResult))

        #searchEngineResult = self.relatedSearch(searchTerm)
        #ScriptEngine.exeAll(searchEngineResult['web'], channelName)

    def relatedSearch(self, searchTerm):
        pass

    def webSearch(self, searchTerm, searchEntity=""):
        #shouldn't have to resolve every query
        #self.session = self.getSession()
        location = geolocation.lookup(self.request.remote_addr) or {'location':'US'}

        options = {'location': location[u'country_code'],
                   'searchEntity': searchEntity}

        searchTerm = searchTerm.encode('utf-8')
        result = searchEngine.search(searchTerm, options)

        return result

    def getYoutubePlaylist(self, searchTerm):
        #self.session = self.getSession()
        categoryTerm = self.request.get("c",'music')
        ySearch = YtubeSearch(searchTerm,categoryTerm) 

        return {'cardId': '', #if generated, update this box
                'cardType': 'yPlaylist', #content type - media etc.
                'cardTitle': 'N/A', 
                'cardRating': 'N/A', #rating 
                'cardSrc': 'N/A',
                'cardContent': ySearch.getTopPlaylist(),
                'editable': False, #user can update
                'hashId': '' #unique hash of this picograph
        }

    def imageSearch(self):
        pass
