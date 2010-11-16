import sys 
import cgi 

from google.appengine.api import users 
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class BoxUrl(db.Model):
    url = db.StringProperty(multiline=False)
    shorted_url = db.StringProperty(multiline=False)
    record_id = db.IntegerProperty()
    date = db.IntegerProperty()
    
    def ShortCompute(self,url):
        dominio = "www.cerbero.it/"
        shorted = "short"
        self.url = url
        self.shorted_url = dominio+shorted
        self.record_id = 1
        self.date = 123
        self.put()  
        return shorted   

def main():
    #url=sys.argv[1]
    url = "www.pippo.it"
    box_url=BoxUrl()
    response = box_url.ShortCompute(url)
    print response 

if __name__ == "__main__":
    main()
 
