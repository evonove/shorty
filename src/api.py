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
        
        if parametri['url']=="":
            #errore ci deve essere l'url
            print "error"
        elif parametri['custom_string']=="":
            res = core.core_classic(parametri['url'])
            return res
        else:
            json_obj = core.core_custum(parametri['url'],parametri['custom_string'])
            return json_obj
        
    def get (self):
        try:
            url = self.request.url
            dominio = "www.cerbero.it"
            sub = url[21:len(url)]
            red = dominio + sub
            normal_url=core.getRealUrl(red)
            self.redirect(normal_url)              
        except:
            self.error(500)

application = webapp.WSGIApplication([('/.+', short)])

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()    