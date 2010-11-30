import os
import core.functions as core
import core.formats as formats
from api.handlers import ShortHandler, ExpandHandler

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template


class MainPage(webapp.RequestHandler):
    def get(self):
        greetings="parametro"

        template_values = {
            'greetings': greetings,
           }

        path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
        self.response.out.write(template.render(path, template_values))

class Result(webapp.RequestHandler):
    def post(self):
        methods = self.request.get('core')
        url = self.request.get('url')
        pers = self.request.get('custom_hash')
      
        
        if methods=="classic":
            res = formats.DecodeJson(core.core_classic(url))
            list_url = res.getMessage()
        elif methods=="custom":
            res = formats.DecodeJson(core.core_custum(url,pers))
            list_url = res.getMessage()
        else :
            res = "non trovato"
            list_url = res
        
        template_values = {
            'urls': list_url,
           }

        path = os.path.join(os.path.dirname(__file__), 'templates/result.html')
        self.response.out.write(template.render(path, template_values))
        

class Resolve(webapp.RequestHandler):
    """Given a shorted url, expand it and redirect user"""
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


application = webapp.WSGIApplication([
      ('/', MainPage),
      ('/result', Result),
      ('/api/short', ShortHandler),
      ('/api/expand', ExpandHandler),
      ('/.+' , Resolve)],debug=True)


if __name__ == "__main__":
    run_wsgi_app(application)