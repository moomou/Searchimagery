#!/usr/bin/env python
from __future__ import with_statement
from webapp2_extras import sessions

import os, json, datetime, logging
import webapp2
import requests
import urllib,urllib2
import markupsafe

class ScriptHandler(webapp2.RequestHandler):
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

    def post(self):
        self.response.out.write('Not supported.')

    def get(self):
        self.session = self.getSession()

        query = db.Query(SearchResultDB)
        query.order('-date')
        result = query.get() 

        if not result:
            return self.response.out.write('Data Store Failed')

        searchResult = GParser(result.searchQuery)
        searchResult.getListOfEntry()

        cmd = self.request.get("cmd")
        target = self.request.get("target")
        
        logging.info(searchResult)
        logging.info(searchResult.allURLs)

        URLLists = searchResult.getURLs(target) 

        if not URLLists:
            return self.response.out.write(json.dumps(["No Result"])) 

        logging.info("Going into exe") 
        parsedResult = Script.exe(cmd,URLLists) #all scripts contain all scripts

        return self.response.out.write(json.dumps(parsedResult)) 
