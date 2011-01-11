from google.appengine.ext import db


class Domain(db.Model):
    """ 
        this class contain the Domain 
    
    Fields
    
        name_domain - name of the domain : string 
        shorted_name - some domain have a different domain for deploy : string
        last_assignament - last assignament for the core classic : string    
    

    """    
    
    name_domain = db.StringProperty(multiline=False)
    shorted_name = db.StringProperty(multiline=False,default="all")
    last_assignament = db.StringProperty(multiline=False)

    """
    old class
class DomainTable (db.Model):
    #domain = db.StringProperty(multiline=False)
    domain = db.ReferenceProperty(Domain)
    last_assignament = db.StringProperty(multiline=False)
    """

class UrlBox(db.Model):
    """ 
        this class contain the association between url and its url short
        plus other utils information
    
    Fields
    
        domain - is a domain of the url : Domain 
        url - is the url to short : string
        shorted_url - is the shorted url : string 
        date - date of make shorted url : date
        active - if the shorted url is active : boolean 
        last_click - last time who used this short url : date   
    
    """
    domain = db.ReferenceProperty(Domain)
    url = db.LinkProperty()
    shorted_url = db.LinkProperty()
    date = db.DateTimeProperty(auto_now=True)
    active = db.BooleanProperty(default=True)
    last_click = db.DateTimeProperty()


class WhiteList(db.Model):
    """ 
        this class contain all the safetly domains, this domain 
        not have the suffix
    
    Fields
    
        domain - a domain : Domain 
        note - particular notes : string   
    
    """
    domain = db.ReferenceProperty(Domain)
    note = db.StringProperty(multiline=False)
  

 
class BlackListShorty(db.Model):
    """ 
        this class contain all the domain who considerate dangerous
    
    Fields
    
        domain - a domain : Domain 
        note - particular notes : string   
    
    """
    domain = db.ReferenceProperty(Domain)
    note = db.StringProperty(multiline=False)
  

class User(db.Model):
    """ 
        this class contain access's credentials 
    
    Fields
    
        user_name - user's name : string 
        password -  user's password  : string   
    
    """
  
    user_name = db.StringProperty(multiline=False)
    password = db.StringProperty(multiline=False)

""" 
non piu' necessaria gestisco black list    
class Settings(db.Model):
     
        this class contain settings 
    
    Fields
    
        check_valid - to control if a link is exist : boolean    
    
      
    check_valid = db.BooleanProperty(default=False)
"""    

       

