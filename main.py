#!/usr/bin/env python
from google.appengine.ext import db
from google.appengine.api import files
from webapp2_extras import sessions

from queryHandler import QueryHandler
from scriptHandler import ScriptHandler
from dbHandler import DBHandler

import os, json, datetime, logging
import webapp2
import markupsafe
import jinja2

jinjaEnv = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinjaEnv.get_template('templates/index.html')
        self.response.out.write(template.render())

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': os.urandom(64),
}

app = webapp2.WSGIApplication([
                                (r'/db/.*',DBHandler),
                                (r'/query/.*',QueryHandler),
                                (r'/script/.*',ScriptHandler),
                                ('/', MainHandler)],
                              debug=True,config=config)
