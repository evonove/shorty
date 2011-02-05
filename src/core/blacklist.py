'''
Created on 11/gen/2011

@author: matteo
'''

from google.appengine.ext import db
from models import BlackListed
from google.appengine.ext.db import NotSavedError


def blacklist(domain_name):
    '''
    blacklist a domain   
    
    Params 
        domain_name - a valid domain name: string 
    
    Return 
        None
    '''
    bl = BlackListed(domain_name=domain_name)
    bl.put()


def unblacklist(domain_name):
    '''
    remove blacklisted status for a domain   
    
    Params 
        domain - a valid domain name: string 
    
    Return 
        None
    '''
    black_domain = db.Query(BlackListed).filter('domain_name = ', domain_name).get()
    if black_domain:
        db.delete(black_domain)


def is_blacklisted(domain_string):
    '''
    control if a domain string is BlackListed  
    
    Params 
        domain string: string 
    
    Return 
        True - if the domain is in BlackList otherwise False
    '''
    entry = db.Query(BlackListed).filter('domain_name = ', domain_string).get()
    return entry is not None
