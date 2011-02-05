'''
Created on 01/feb/2011

@author: masci
'''

class CoreError(Exception):
    """Base class for exceptions in this module.

    Attributes:
        msg - Explanation of the error (if present)
    """
    def __init__(self, msg=''):
        self.msg = msg

    def __str__(self):
        return self.msg


class InvalidURLError(CoreError):
    def __init__(self, url):
        msg = 'Url is not valid: %s' % url
        CoreError.__init__(self, msg)


class DomainBlacklistedError(CoreError):
    def __init__(self, domain_name):
        msg = 'Domain is blacklisted: %s' % domain_name
        CoreError.__init__(self, msg)


class URLExistsError(CoreError):
    def __init__(self, url):
        msg = 'URL already exists: %s' % url
        CoreError.__init__(self, msg)

