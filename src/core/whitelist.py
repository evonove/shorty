from google.appengine.ext import db
from models import WhiteList

#senza www - chiedere 
def insertInWhite(domain,note):
    query = db.Query(WhiteList).filter('domain = ', domain )
    if query.count()>0:
        print "errore"
    else:
        white = WhiteList()
        white.domain=domain
        white.note = note
        db.put(white)
    
def cancelInWhite(domain):
    white = WhiteList()
    query = db.Query(WhiteList).filter('domain = ', domain )
    white = query.fetch(1)[0]
    db.delete(white)

def modifyNote(domain,note):
    white = WhiteList()
    query = db.Query(WhiteList).filter('domain = ', domain )
    white = query.fetch(1)[0]
    white.note = note
    db.put(white)
    
def checkInWhite(domain):
    query = db.Query(WhiteList).filter('domain = ', domain )
    if query.count()>0:
        return True
    else:
        return False
    