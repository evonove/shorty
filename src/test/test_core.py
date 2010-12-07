'''
Created on 30/nov/2010

@author: masci
'''
from core.core import compute_next, grammar
from google.appengine.ext  import db
from core.models import UrlBox
from core import functions

def test_next():
    assert compute_next(grammar[0]) == grammar[1]
    assert compute_next(grammar[-1]) == 'aa'
    assert compute_next('') == grammar[0]
    assert compute_next('ab+') == 'aca'

def test_already_custom():
    u = UrlBox()
    u.shorted_url = 'asdfgh'
    db.put(u)
    
    assert(functions.isAlredyCustum('asdfgh'))
    
    db.delete(u)
