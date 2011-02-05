import core.functions as core

from google.appengine.ext import webapp

class ShortHandler(webapp.RequestHandler):
    """Given a long url, return a shorted one"""
    def post(self):
        parametri= self.request.str_params
        
        if parametri['url']=="":
            #errore ci deve essere l'url
            print "error"
        elif parametri['custom_string']=="":
            res = core.short(parametri['url'])
            return res
        else:
            json_obj = core.short(parametri['url'],parametri['custom_string'])
            return json_obj

class ExpandHandler(webapp.RequestHandler):
    """ Given an url shorted by shorty, expand and return the original one """
    def get (self):
        try:
            print 'shorting'
            self.response.out.write('Hello, webapp World!')
            return
            url = self.request.url
            dominio = "www.cerbero.it"
            sub = url[21:len(url)]
            red = dominio + sub
            normal_url=core.expand(red)
            self.redirect(normal_url)              
        except:
            self.error(500)
"""
    if checkInBlack(domain) :
        date=datetime.datetime.now()
        message_list=["si e' verificato un errore : "+ "dominio Proibito"]
        json = formats.Response(message_list,date,True,"1",num_of_shorts())
        resp = json.serializeJson()
        return resp
"""
