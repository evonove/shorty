'''
Created on 05/feb/2011

@author: masci
'''
from google.appengine.ext import db
from conftest import datastore
from core import functions
from core.models import UrlBox, Domain
from core import settings

def test_url_already_shorted():
    datastore.Clear()
    u = UrlBox()
    u.url = 'http://test_fixture.ext/'
    u.put()
    assert functions.url_already_shorted('http://test_fixture.ext')
    assert functions.url_already_shorted('http://test_fixture.ext/')
    u.active = False
    u.put()
    assert functions.url_already_shorted('http://test_fixture.ext/')
    assert not functions.url_already_shorted('http://test_fixture.ext/', False)
    db.delete(u)
    assert not functions.url_already_shorted('http://test_fixture.ext')


def test_num_of_shorts():
    datastore.Clear()
    dom  = Domain(name = u"yyyy")
    dom2 = Domain(name = u"xxxx")
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


def test_get_shorts():
    datastore.Clear()
    shorting_frags = ['test_%d' % x for x in xrange(10)]
    shorted_urls = []
    
    dom=Domain(name = u"test_fixture")
    db.put(dom)
    
    for s in shorting_frags:
        u = UrlBox()
        u.domain = dom
        u.shorting_frag = s
        u.put()
        shorted_urls.append(u.shorted_url)
        
    computed = functions.get_shorts(dom , 100)
    assert shorted_urls == computed


def test_get_real_url():
    datastore.Clear()
    dom=Domain(name = u"the_gambit")
    db.put(dom)
    u = UrlBox()
    u.shorting_frag="test_fixture"
    u.url="http://www.the_gambit.it/test"
    u.active = True
    u.domain = dom
    db.put(u)
    assert functions.expand(u.shorted_url)=="http://www.the_gambit.it/test"


def test_short():
    datastore.Clear()
    domain = Domain(name=u"wolverine.it")
    db.put(domain)
    #test classic core pass
    short = functions.short("http://www.wolverine.it/test/test")
    expected = '%s%s/wolverine.it/a' % (settings.SERVICE_SCHEME, settings.SERVICE_HOSTNAME)
    assert short == expected
    # TODO expand this test


