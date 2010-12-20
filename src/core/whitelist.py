from google.appengine.ext import db
from models import WhiteList
from google.appengine.ext.db import NotSavedError

#senza www - chiedere 
def insertInWhite(domain,note=None):
    '''
    insert a domain in whitelist to omit second part  
    
    Params 
        domini - a valid domain : Domain 
        note - a note : string
    
    Return 
        True - if is insert in whitelist otherwise False
    '''
    insertIntoWhite = db.Query(WhiteList).filter('domain = ', domain).count()
    if not insertIntoWhite:
        white = WhiteList()
        white.domain=domain
        white.note = note
        db.put(white)
        insertIntoWhite = True
    else : 
        insertIntoWhite= False
    return insertIntoWhite
    
def cancelInWhite(domain):
    '''
    cancel a domain in whitelist   
    
    Params 
        domain - a valid domain : Domain 
    
    Return 
        True - if is cancel to whitelist otherwise False
    '''
    white_element=None
    is_delete = False
    try :
        white_element = db.Query(WhiteList).filter('domain = ', domain ).get()
    except NotSavedError:
        pass
    if white_element:
        db.delete(white_element)
        is_delete = True
    return is_delete

def modifyNote(domain,note):
    '''
    Modify the notes to  a domain in whitelist  
    
    Params 
        domain - a valid domain : Domain 
        note - a note : string
    
    Return 
        True - if is update in whitelist otherwise False
    '''
    white_element = None
    modifiedNote = False     
    try : 
        white_element = db.Query(WhiteList).filter('domain = ', domain ).get()
    except NotSavedError:
        pass
    if white_element:
        white_element.note = note
        modifiedNote = db.put(white_element).id() > 0
    return modifiedNote == True

def checkInWhite(domain):
    '''
    control if a domain  is in whitelist  
    
    Params 
        domain - a valid domain : Domain 
    
    Return 
        True - if the domain is in whitelist otherwise False
    '''
    check = db.Query(WhiteList).filter('domain = ', domain).count()
    if check >0:
        return True
    else:
        return False
    