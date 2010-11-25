import cgi
import os
import core
import response
import models 

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template

class short(webapp.RequestHandler):
    def post(self):
        parametri= self.request.str_params
        #print parametri['custom_string']
        #print parametri['url']
        
        if parametri['url']=="":
            #return self.response.error(500)
            print "error"
        elif parametri['custom_string']=="":
            #json_obj = core.core_classic(parametri['url'])
            #return json_obj
            print "sono qui in classic"
            #print type(parametri['url'])
            #print parametri['url'].type
            res = core.core_classic(parametri['url'])
            print res
        else:
            print "sono qui"
            print parametri['url']
            print parametri['custom_string']
            json_obj = core.core_custum(parametri['url'],parametri['custom_string'])
            print json_obj
            #return json_obj
            #res = response.DecodeJson(core.core_custum(str(parametri['url']),str(parametri['custom_string'])))
            print res.getMessage()
        
    def get (self):
        #ok il get funge
        url = self.request.get('url')
        print url
        
        
    
application = webapp.WSGIApplication([('/.+', short)])

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()    