from google.appengine.ext import db

import settings

from urlparse import urlparse

class Domain(db.Model):
    """ 
        this class contain the Domain 
    
    Fields
    
        name_domain - name of the domain : string 
        last_assignment - last assignament for the core classic : string    

    """
    name = db.StringProperty()
    last_shorting_frag_assigned = db.StringProperty()
    friendly_name = db.StringProperty()


class User(db.Model):
    """ 
        this class contain access's credentials 
    
    Fields
    
        user_name - user's name : string 
        password -  user's password  : string   
    
    """
    user_name = db.StringProperty(multiline=False)
    password = db.StringProperty(multiline=False)


class UrlBox(db.Model):
    """ 
        this class contain the association between url and its url short
        plus other utils information
    
    Fields
    
        domain - is a domain of the url : Domain 
        url - is the original url : string
        shorting_frag - is the shorted fragment of the shorted url : string 
        date - date of make shorted url : date
        active - if the shorted url is active : boolean 
        last_click - last time who used this short url : date   
    
    """
    domain = db.ReferenceProperty(Domain)
    _url = db.LinkProperty()
    shorting_frag = db.StringProperty()
    date = db.DateTimeProperty(auto_now=True)
    active = db.BooleanProperty(default=True)
    custom = db.BooleanProperty(default=False)
    last_click = db.DateTimeProperty()
    click = db.IntegerProperty(default=0)
    owner = db.ReferenceProperty(User)
    
    def url(self):
        return self._url
    
    def seturl(self, url):
        u = urlparse(url)
        if not u.path: url+='/'
        self._url = url
    
    url=property(fget=url, fset=seturl) # python2.5 does not fully support @property decorator 
    
    @property
    def shorted_url(self):
        verbose_frag = self.domain.friendly_name
        if not verbose_frag:
            verbose_frag = self.domain.name
        
        return '%s%s/%s/%s' % (settings.SERVICE_SCHEME, 
                               settings.SERVICE_HOSTNAME,
                               verbose_frag, 
                               self.shorting_frag)

 
class BlackListed(db.Model):
    """ 
        this class wraps a domain we don't want to short
    
    Fields
        domain_name - blacklisted domain name: string    
    
    """
    domain_name = db.StringProperty()

