import webapp2
import urllib,urllib2
import requests
import markupsafe
import os, json, datetime, logging

from webapp2_extras import sessions
from google.appengine.api import channel 

class DBHandler(webapp2.RequestHandler):
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
        searchType = self.request.get('cmd','general')

    #parse query and write to channel
    def get(self):
        searchType = self.request.get('cmd','general')
        searchType = self.request.get('cmd','general')
        funcs = {'ytube':self.ytubeQuery,
                 'gen':self.parseQuery}

        if searchType in funcs:
            funcs[searchType]()
        else:
            funcs['gen']()
