'''
Created on 11/gen/2011

@author: matteo
'''

from google.appengine.ext import db
from models import BlackList
from google.appengine.ext.db import NotSavedError


def insertInBlack(domain,note=None):
    '''
    insert a domain in Blacklist . This domain not be shortered   
    
    Params 
        domain - a valid domain : Domain 
        note - a note : string
    
    Return 
        True - if is insert in whitelist otherwise False
    '''
    insertIntoBlack = db.Query(BlackList).filter('domain = ', domain).count()
    if not insertIntoBlack:
        black = BlackList()
        black.domain=domain
        black.note = note
        db.put(black)
        insertIntoBlack = True
    else : 
        insertIntoBlack= False
    return insertIntoBlack
    
def cancelInBlack(domain):
    '''
    cancel a domain in blacklist   
    
    Params 
        domain - a valid domain : Domain 
    
    Return 
        True - if is cancel to whitelist otherwise False
    '''
    black_element=None
    is_delete = False
    try :
        black_element = db.Query(BlackList).filter('domain = ', domain ).get()
    except NotSavedError:
        pass
    if black_element:
        db.delete(black_element)
        is_delete = True
    return is_delete

def modifyNoteBlack(domain,note):
    '''
    Modify the notes to  a domain in BlackList  
    
    Params 
        domain - a valid domain : Domain 
        note - a note : string
    
    Return 
        True - if is update in whitelist otherwise False
    '''
    black_element = None
    modifiedNote = False     
    try : 
        black_element = db.Query(BlackList).filter('domain = ', domain ).get()
    except NotSavedError:
        pass
    if black_element:
        black_element.note = note
        modifiedNote = db.put(black_element).id() > 0
    return modifiedNote == True

def checkInBlack(domain):
    '''
    control if a domain  is in BlackList  
    
    Params 
        domain - a valid domain : Domain 
    
    Return 
        True - if the domain is in BlackList otherwise False
    '''
    check = db.Query(BlackList).filter('domain = ', domain).count()
    if check >0:
        return True
    else:
        return False
    