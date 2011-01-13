'''
Created on 13/gen/2011

@author: matteo
'''
from conftest import datastore
from shield import Shield

def test_shield():
    shield = Shield ("192.168.1.1")
    assert shield.getShieldSentence() == False
    shield2 = Shield("192.168.1.1")
    assert shield2.getShieldSentence() == False
    shield3 =Shield("192.168.1.1")
    shield4 = Shield("192.168.1.1")
    shield5=Shield("192.168.1.1")
    shield6=Shield("192.168.1.1")
    shield7=Shield("192.168.1.1")
    assert shield7.getShieldSentence() == True

 

