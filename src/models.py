import sys 
import cgi 

from google.appengine.api import users 
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db


#cambiare filosofia quando inserisco un associazione 
#tengo l'ultimo assegnamento come stringa  e il dominio
#per il prossimo assegamento parso la stringa e incremento
#i contatori 

class DomainTable (db.Model):
    domain = db.StringProperty(multiline=False)
    last_assignament = db.StringProperty(multiline=False)
    
# il flag active dice che l'associazione e' attiva . Quando faccio un
#nuovo bindings per quel dominio vado a vedere se c'e' n'e' uno disattivo 
#e gli asssegno quello 

class UrlBox(db.Model):
    domain = db.StringProperty(multiline=False)
    url = db.StringProperty(multiline=False)
    shorted_url = db.StringProperty(multiline=False)
    date = db.FloatProperty()
    active = db.BooleanProperty()

class WhiteList(db.Model):
    domain = db.StringProperty(multiline=False)
    note = db.StringProperty(multiline=False)
