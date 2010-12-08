# -*- coding: utf-8 -*-
'''
Created on 30/nov/2010

@author: masci
'''
from google.appengine.ext  import db

from core.core import compute_next, grammar
from core.models import UrlBox
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
    for i in xrange(10):
        u = UrlBox()
        u.put()
    assert functions.num_of_shorts() == 10
    
    for i in xrange(20):
        u = UrlBox()
        u.domain = u'fixture_test'
        u.put()
    assert functions.num_of_shorts('fixture_test') == 20
    assert functions.num_of_shorts() == 30


def test_already_shorted():
    datastore.Clear()
    u = UrlBox()
    u.url = 'http://test_fixture'
    u.put()
    assert functions.already_shorted('http://test_fixture')


def test_get_shorts():
    datastore.Clear()
    shorted = ['http://test_%d' % x for x in xrange(10)]
    for s in shorted:
        u = UrlBox()
        u.domain = 'test_fixture'
        u.shorted_url = s
        u.put()
    computed = functions.get_shorts('test_fixture', 100)
    assert shorted == computed

