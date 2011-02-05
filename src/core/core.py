'''
Created on 07/dic/2010

@author: masci
'''
import string, urlparse
import settings
from errors import InvalidURLError

LETTERS = [x for x in string.ascii_letters]
NUMBERS = [x for x in string.digits]
SYMBOLS = ["_","-","+"]
grammar = LETTERS + NUMBERS + SYMBOLS


def compute_next(previous):
    """
    Compute the next short tag
    Parmas:
        previus - previous assignament : string
    Return:
        valid assignament : string
    
    """
    if not previous:
        return grammar[0]
    
    indexes = [grammar.index(c) for c in previous[::-1]]
    
    for i in xrange(len(indexes)):
        indexes[i]+=1
        if indexes[i] >= len(grammar):
            indexes[i]=0
        else:
            break
    
    if indexes.count(0) == len(indexes):
        indexes.append(0)

    return ''.join(grammar[i] for i in indexes)

def parse_domain(url):
    """
    parse a domain string from an url 
    
    Params 
        url - url to parse
    
    Return 
        domain name - string
    
    """
    parsed = urlparse.urlparse(sanitize(url))    
    return '.'.join(parsed.hostname.split('.')[-2:])


def sanitize(url):
    """Trivial checks for uniforming urls"""
    parsed = urlparse.urlparse(url)
    
    if parsed.scheme not in settings.VALID_SCHEMES:
        raise InvalidURLError(url)
    
    if not parsed.path:
        url += '/'
    
    return url
