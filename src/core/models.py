from google.appengine.ext import db

#cambiare filosofia quando inserisco un associazione 
#tengo l'ultimo assegnamento come stringa  e il dominio
#per il prossimo assegamento parso la stringa e incremento
#i contatori 

class DomainTable (db.Model):
    domain = db.StringProperty(multiline=False)
    last_assignament = db.StringProperty(multiline=False)


class UrlBox(db.Model):
    """il flag active dice che l'associazione e' attiva . Quando faccio un
    nuovo bindings per quel dominio vado a vedere se c'e' n'e' uno disattivo 
    e gli asssegno quello
    
    Fields
        TODO: docstrings 
    
    """
    domain = db.StringProperty(multiline=False)
    url = db.LinkProperty()
    shorted_url = db.LinkProperty()
    date = db.DateTimeProperty(auto_now=True)
    active = db.BooleanProperty(default=True)
    last_click = db.DateTimeProperty()


class WhiteList(db.Model):
    domain = db.StringProperty(multiline=False)
    note = db.StringProperty(multiline=False)
#nuovi classi per gestire gli altri servizi di shortener  

 
class BlackListShorty(db.Model):
    domain = db.StringProperty(multiline=False)


class Admin(db.Model):
    user = db.StringProperty(multiline=False)
    password = db.StringProperty(multiline=False)

