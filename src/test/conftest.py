'''
Created on 07/dic/2010

@author: masci
'''
import sys
import os.path
import logging

#APPENGINE_SDK = '/usr/local/google_appengine/'
APPENGINE_SDK = '/home/matteo/Scaricati/google_appengine/'
APPLICATION_ID = 'shortydev-app'
datastore = None

def pytest_configure(config):
    # let python find SDK modules        
    sys.path.append(APPENGINE_SDK)
    sys.path.append(os.path.join(APPENGINE_SDK, 'lib', 'django'))
    sys.path.append(os.path.join(APPENGINE_SDK, 'lib', 'webob'))
    sys.path.append(os.path.join(APPENGINE_SDK, 'lib', 'antlr3'))

    # simulate we're running an app with devserver
    from google.appengine.api import apiproxy_stub_map, datastore_file_stub
    os.environ['APPLICATION_ID'] = APPLICATION_ID
    
    # overwrite default proxy with an APIProxyStubMap instance
    apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
    # create a stub to fake datastore
    global datastore
    datastore = datastore_file_stub.DatastoreFileStub('shortydev-app', None, None)
    # register the datastore stub to the proxy
    apiproxy_stub_map.apiproxy.RegisterStub('datastore_v3', datastore)

def pytest_unconfigure(config):    
    """Since GAE seems to not gracefully close its logger handler, do it by
    ourselves
    
    """
    rootLogger = logging.getLogger()
    for handler in rootLogger.handlers:
        if isinstance(handler, logging.StreamHandler):
            handler.flush()
            handler.close()
            rootLogger.removeHandler(handler)
