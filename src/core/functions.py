from google.appengine.ext import db

from models import Domain, UrlBox
from errors import *
from blacklist import is_blacklisted
from core import compute_next, sanitize, parse_domain

from datetime import datetime
from urlparse import urlparse

def short(url, custom_string=None):
    """
    Perform the shortening of given url. Optionally use a custom string
    instead of using internal algorithm provided by core module
    
    Params
        url - the url to shorten: url
        custom_string - the string to use to short the link: string
    
    Return
        shorted url: url string
    
    """    
    domain_name = parse_domain(url)
    
    if is_blacklisted(domain_name):
        raise DomainBlacklistedError(domain_name)
    
    if custom_string and shorting_frag_already_exists(custom_string, False):
        raise URLExistsError(custom_string)
    
    domain = get_or_create_domain(domain_name)
    urlbox = None
    
    if custom_string:
        urlbox = UrlBox()
        urlbox.shorting_frag = custom_string
        urlbox.custom = True
    else:
        urlbox = respawn_urlbox(domain)
        if not urlbox:
            urlbox = UrlBox()
            short = compute_next(domain.last_shorting_frag_assigned)
            while shorting_frag_already_exists(domain, short):
                short = compute_next(short)
            urlbox.shorting_frag = short
            urlbox.custom = False
    
    urlbox.domain = domain
    urlbox.url = url
    urlbox.put()
    
    return urlbox.shorted_url


def respawn_urlbox(domain):
    """Try to recycle and respawn an inactive domain.
    
    Params:
        domain: Domain instance
        
    Returns:
        urlbox: A respawned urlbox or None
    
    """
    query = db.Query(UrlBox)
    query.filter('domain = ', domain)
    query.filter('active = ', False)
    query.filter('custom = ', False)
    query.order('-date')
    
    ub = query.get()
    
    if ub:
        # TODO: maybe following calls could be grouped into a method 
        # (ex. reset()) of the UrlBox class
        ub.url = None
        ub.last_click = None
        ub.click = 0
        ub.active = True
        ub.date = datetime.datetime.now()
    
    return ub


def get_or_create_domain(domain_string):
    """
    check in the instance of the specific domain is saved . 
    If yes return an instance of domain, if not save an instance and return it 
    
    Params
        domain_string - the domain name (ex. facebook.com): string
    
    Return
        an instance of domain object : Domain 
    
    """
    domain = db.Query(Domain).filter('name = ', domain_string).get()
    if not domain:
        domain = Domain()
        domain.name = domain_string
        db.put(domain)

    return domain 


def get_shorts(domain, limit, offset=0):
    '''Retrieve shorted urls for a certain domain.
    
    Params
        domain - the domain for which retrieve results: string
        limit - how many results at max to retrieve: int
        offset - how many results to skip: int
    
    Return
        a list containing shorted urls for the domain: list
    '''
    query = db.Query(UrlBox).filter('domain = ', domain)
    results = query.fetch(limit, offset)
    return [x.shorted_url for x in results]


def num_of_shorts(domain=None):
    '''Count how many shorts we've got in the datastore
    
    Params
        domain - if not None count shorts for that domain, count all otherwise
    
    Return
        number of shorts: integer
    '''
    
    query = UrlBox.all()
    if domain:
        query.filter(' domain = ', domain)
    return query.count()


def shorting_frag_already_exists(domain, shorting_frag, include_inactives=True):
    '''Check if a shorting frag is known to the system, and in case if it is
    currently active
    
    Params
        domain - 
        shorting_frag - an already shorted url to check: string
        include_inactives - extend query to inactive UrlBoxes
        
    Return
        whether shorted url is known: boolean
    '''
    q = db.Query(UrlBox, keys_only=True)
    q.filter('shorting_frag = ', shorting_frag).filter('domain = ', domain)
    if not include_inactives:
        q.filter('active = ' , True)
    
    return q.get() is not None


def url_already_shorted(url, include_inactives=True):
    '''Check if an url was already shorted
    
    Params
        url - url to check: string
        include_inactives - extend query to inactive UrlBoxes
    
    Return
        whether the url was already shorted: boolean
    '''
    url = sanitize(url)

    q = db.Query(UrlBox, keys_only=True).filter('_url = ', url)
    if not include_inactives:
        q.filter('active = ', True)
    
    return q.get() is not None

    
def expand(shorted_url):
    """
    return the real url associated to a short url and increase the number of click
    
    Params 
        shorted_url - a shorted url
    
    Return 
        url - the real url to redirect
    """
    parsed_url = urlparse(sanitize(shorted_url))
    domain_frag, shorting_frag = parsed_url.path[1:].split('/')
    
    domain = db.Query(Domain).filter('name = ', domain_frag).get()
    if not domain:
        domain = db.Query(Domain).filter('friendly_name = ', domain_frag).get()

    q = db.Query(UrlBox)
    q.filter('shorting_frag = ', shorting_frag)
    q.filter('active = ', True)
    q.filter('domain = ', domain)
    urlbox = q.get()
    
    urlbox.click+=1 
    db.put(urlbox) 
    return urlbox.url

def cancelByPolicy(soglia):
    """
    this is a sample of cancellation policy. In this case, cancel all row in 
    UrlBox table if the the shorted url not used before a certain date 
    
    Params 
        solgia - a date
    
    Return 
        void - cancel rows 
    """
    import time
    data_from_cancel = time.mktime(time.localtime()) - soglia
    query = db.Query(UrlBox).filter('last_click < ', data_from_cancel)
    results = query.all
    for res in results:
        db.delete(res)
    
