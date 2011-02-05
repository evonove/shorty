# -*- coding: utf-8 -*-
'''
Created on 30/nov/2010

@author: masci
'''
import pytest
from google.appengine.ext import db
from conftest import datastore # TODO non è proprio elegante...

from core.core import grammar, compute_next, parse_domain

def test_next():
    assert compute_next(grammar[0]) == grammar[1]
    assert compute_next(grammar[-1]) == 'aa'
    assert compute_next('') == grammar[0]
    assert compute_next('ab+') == 'aca'

   
def test_parse_domain():
    assert parse_domain('http://www.example.com') == 'example.com'
    assert parse_domain('http://www.example.com/') == 'example.com'
    assert parse_domain('http://www.ex.com/test') == 'ex.com'


@pytest.mark.xfail
def test_failing_parse_domain():
    parse_domain('www.example.com')
    parse_domain('file://www.example.com')
    



