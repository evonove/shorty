'''
Created on 05/feb/2011

@author: masci
'''
from google.appengine.ext import db
from conftest import datastore
from core.blacklist import *
from core.models import BlackListed

def test_check_in_black():
    datastore.Clear()
    black_one = BlackListed(domain_name= u"wolverine.it")
    black_two = BlackListed(domain_name= u"test.it")
    db.put(black_one)
    db.put(black_two)
    
    assert is_blacklisted("wolverine.it")
    assert is_blacklisted("test.it")
    assert not is_blacklisted('example.com')


def test_blacklist():
    datastore.Clear()
    blacklist('wolverine.it')
    blacklist('test.it')
    
    assert is_blacklisted("wolverine.it")
    assert is_blacklisted("test.it")


def test_unblack():
    datastore.Clear()
    blacklist('wolverine.it')
    unblacklist('wolverine.it')


    assert not is_blacklisted('wolverine.it')