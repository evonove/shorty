'''
Created on 07/dic/2010

@author: masci
'''
import string

letters = [x for x in string.ascii_letters]
numbers = [x for x in string.digits]
symbols = ["_","-","+"]
grammar = letters + numbers + symbols

def compute_next(previous):
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
