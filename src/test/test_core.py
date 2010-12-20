# -*- coding: utf-8 -*-
'''
Created on 30/nov/2010

@author: masci
'''
from google.appengine.ext  import db


from core.core import compute_next, grammar
from core.models import UrlBox, Domain, WhiteList
from core.whitelist import checkInWhite, modifyNote, insertInWhite, cancelInWhite
from core import functions 

from conftest import datastore # TODO non è proprio elegante...

def test_next():
    assert compute_next(grammar[0]) == grammar[1]
    assert compute_next(grammar[-1]) == 'aa'
    assert compute_next('') == grammar[0]
    assert compute_next('ab+') == 'aca'


def test_is_short():
    datastore.Clear()
    
    u = UrlBox()
    u.shorted_url = 'http://test_fixture.ext'
    u.url = 'http://another_test_fixture/'
    u.put()
    assert functions.is_short('http://test_fixture.ext')
    db.delete(u)
    assert not functions.is_short('http://test_fixture.ext')

def test_num_of_shorts():
    datastore.Clear()
    dom = Domain(name_domain = u"yyyy")
    dom2=Domain(name_domain = u"xxxx")
    db.put(dom)
    db.put(dom2)
    for i in xrange(10):
        u = UrlBox()
        u.domain = dom
        u.put()
    assert functions.num_of_shorts() == 10
    
    for i in xrange(20):
        u = UrlBox()
        u.domain = dom2
        u.put()
    assert functions.num_of_shorts(dom2) == 20
    assert functions.num_of_shorts() == 30

def test_already_shorted():
    datastore.Clear()
    dom=Domain(name_domain = u"http://test_fixture")
    db.put(dom)
    u = UrlBox()
    u.domain = dom
    u.url="http://test_fixture"
    u.put()
    assert functions.already_shorted(u"http://test_fixture")

def test_get_shorts():
    datastore.Clear()
    shorted = ['http://test_%d' % x for x in xrange(10)]
    dom=Domain(name_domain = u"test_fixture")
    db.put(dom)
    for s in shorted:
        u = UrlBox()
        u.domain = dom
        u.shorted_url = s
        u.put()
    computed = functions.get_shorts(dom , 100)
    assert shorted == computed
    
def test_is_reciclable_custum():
    datastore.Clear()
    dom=Domain(name_domain = u"the_gambit")
    db.put(dom)
    u = UrlBox()
    u.shorted_url="http://test_fixture"
    u.active = False
    u.domain = dom
    db.put(u)
    assert functions.isReciclableCustum(u.shorted_url)==True
    assert functions.isReciclableCustum("bad")==False
    
def test_is_reciclable():
    datastore.Clear()
    dom=Domain(name_domain = u"the_gambit")
    db.put(dom)
    u = UrlBox()
    u.shorted_url="http://test_fixture"
    u.active = False
    u.domain = dom
    db.put(u)
    assert functions.isReciclable(dom)==True
    assert functions.isReciclable("bad")==False
    
def test_get_real_url():
    datastore.Clear()
    dom=Domain(name_domain = u"the_gambit")
    db.put(dom)
    u = UrlBox()
    u.shorted_url="http://test_fixture"
    u.url="http://www.the_gambit.it/test"
    u.active = False
    u.domain = dom
    db.put(u)
    assert functions.getRealUrl( u.shorted_url)=="http://www.the_gambit.it/test"

   
def test_compute_domain():
    datastore.Clear()
    dom=Domain(name_domain = u"wolverine.it")
    db.put(dom)
    test = u"http://www.the_gambit.it"
    test2= u"http://www.wolverine.it"
    w = WhiteList()
    w.domain = dom 
    db.put(w)
    assert functions.computeDomain(test)==u"the_gambit.it"
    assert functions.computeDomain(test2)==u"wolverine"

   
def test_check_in_white():
    datastore.Clear()
    dom=Domain(name_domain = u"wolverine.it")
    dom2=Domain(name_domain = u"test.it")
    db.put(dom)
    db.put(dom2)
    w = WhiteList()
    w.domain = dom 
    db.put(w)
    assert checkInWhite(dom)==True
    assert checkInWhite(dom2)==False
    
def test_modify_note():
    datastore.Clear()
    dom=Domain(name_domain = u"the_gambit.it",note = u"energia cinetica")
    dom2 = Domain(name_domain = u"test.it")
    db.put(dom)
    w = WhiteList()
    w.domain = dom 
    db.put(w)
    assert modifyNote(dom,"energia_cinetica e solare")==True
    assert modifyNote(dom2,"energia")==False
    
def test_insert_in_white():
    dom=Domain(name_domain = u"the_gambit.it")
    db.put(dom)
    assert insertInWhite(dom) == True 
    assert insertInWhite(dom,"notes") == False
    
def test_camcel_in_white():
    datastore.Clear
    dom=Domain(name_domain = u"the_gambit.it")
    dom2 = Domain(name_domain = u"test.it")
    db.put(dom)
    w = WhiteList()
    w.domain = dom 
    db.put(w)
    insertInWhite(dom)
    assert cancelInWhite(dom)==True
    assert cancelInWhite(dom2)==False 

    

