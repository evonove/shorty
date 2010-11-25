import cgi
import os
import core
import response

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template
#vediamo un po
from google.appengine.api import urlfetch



class MainPage(webapp.RequestHandler):
    def get(self):
        greetings="parametro"

        template_values = {
            'greetings': greetings,
           }

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

class Result(webapp.RequestHandler):
    def post(self):
        #print "invio dati"
        #print self.request.get('url')
        #print self.request.get('core')
        methods = self.request.get('core')
        url = self.request.get('url')
        pers = self.request.get('custom_hash')
        if methods=="classic":
            res = response.DecodeJson(core.core_classic(url))
            print res.getMessage()
        elif methods=="custom":
            res = response.DecodeJson(core.core_custum(url,pers))
            print res.getMessage()
        else :
            print "non trovato"

class Resolve(webapp.RequestHandler):
    
    def get(self):
        try:
            url = self.request.url
            dominio = "www.cerbero.it"
            sub = url[21:len(url)]
            red = dominio + sub
            normal_url=core.getRealUrl(red)
            self.redirect(normal_url)              
        except:
            self.error(500)
   
            
            
application = webapp.WSGIApplication([('/', MainPage),('/result', Result),('/.+' , Resolve)],debug=True)



def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()