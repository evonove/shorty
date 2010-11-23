import cgi
import os

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template




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
        print "invio dati"
        print self.request.get('url')
        print self.request.get('core')
        
        
application = webapp.WSGIApplication([('/', MainPage),('/result', Result)],debug=True)



def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()