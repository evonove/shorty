from google.appengine.ext import db
from binding import bind
from models import DomainTable
from models import UrlBox
from urlparse import urlparse
import response
import whitelist
import time
import sys 

def core_classic(url):
    '''
    '''
    #aggiungere la retrun
    try :
        if is_shorted(url):
            du=UrlBox()
            query = db.Query(UrlBox).filter('url = ',url ).filter('active = ', True)
            du = query.fetch(1)[0]
             #shorted = du.shorted_url
            message_list=[]
            message_list.append(du.shorted_url)
            resp = response.MakeJson(message_list,du.date,False,"0",totals())
            #resp.printJsonElement("message")
            #resp.printJsonElement("total_short")
         
        else:
            mydomain="www.cerbero.it/"
            dominio = computeDomain(url)
            is_recycle=isReciclable(dominio)
            if is_recycle:
                shorted = recycle(dominio,url)
                message_list=[]
                message_list.append(shorted)
                resp = response.MakeJson(message_list,"devo modificare data",False,"0",totals())
            else:
                shorted = bind(dominio) 
                url_shortato = mydomain+dominio+shorted
                dt=UrlBox()
                dt.domain = dominio
                dt.url = url 
                dt.shorted_url=url_shortato
                dt.date=time.mktime(time.localtime())
                dt.active = True
                db.put(dt)
                message_list=[]
                message_list.append(dt.shorted_url)
                resp = response.MakeJson(message_list,dt.date,False,"0",totals())
    #         
    #res = response.MakeJson(dt.shorted_url,)
        #return shorted
    except:
        error = str(sys.exc_info()[0])
        date=time.mktime(time.localtime())
        #print error
        message_list=["si è verificato un errore"]
        resp = response.MakeJson(message_list,date,True,"1",totals()) 

    
def core_custum(url,user_url):
    '''
    '''
    try : 
        mydomain="www.cerbero.it/"
        dominio = computeDomain(url)
        url_shortato = mydomain+dominio+"_"+user_url    
        if is_alredy_custum(url_shortato):
        #query = db.Query(UrlBox).filter('shorted_url = ',url_shortato).filter('active = ',True)
            print "attenzione :"
            print "errore gia short" 
        else:
            dt=UrlBox()
            if isReciclableCustum(url_shortato):
                query = db.Query(UrlBox).filter('shorted_url = ', url_shortato ).filter('active = ' , False)
                dt = query.fetch(1)[0]
                dt.shorted_url = url_shortato 
                dt.date=time.mktime(time.localtime())
                dt.active = True
                db.put(dt)     
            else:
                dt.domain = dominio
                dt.url = url 
                dt.shorted_url=url_shortato
                dt.date=time.mktime(time.localtime())
                dt.active = True
                db.put(dt)
    except:
        error = str(sys.exc_info()[0])
        print error
        
        
def domainList(domain,max_view):
    '''
    '''
    try :
        list_of_short =[]
        query = db.Query(UrlBox).filter('domain = ', domain )
        results = query.fetch(max_view)
        for res in results:
            list_of_short.append(res.shorted_url)
        
        return list_of_short
    
    except:
        error = str(sys.exc_info()[0])
        print error
    
def totalsDomain(domain):
    '''
    '''
    try :
        query = UrlBox.all().filter(' domain = ', domain)
        return query.count()
    except:
        error = str(sys.exc_info()[0])
        print error

def totals():
    '''
    '''
    try:
        query = UrlBox.all()
        return query.count()
    except:
        error = str(sys.exc_info()[0])
        print error

def is_alredy_custum(shorted_url):
    '''
    '''
    query = db.Query(UrlBox).filter('shorted_url = ', shorted_url ).filter('active = ' , True )
    if query.count()>0:
        return True
    
    else :
        return False
    



def is_shorted(url):
    '''
    '''
    #du=UrlBox()
    query = db.Query(UrlBox).filter('url = ',url ).filter('active = ', True)
    if query.count()>0:
        return True
    else:
        return False


def isReciclableCustum(shorted_url):
    '''
    '''
    query = db.Query(UrlBox).filter('shorted_url = ',shorted_url).filter('active = ', False)
    if query.count()>0:
        return True
    else:
        return False
        



def isReciclable(dominio):
    '''
    '''
    #dt=UrlBox()
    query = db.Query(UrlBox).filter('domain = ',dominio ).filter('active = ', False)
    if query.count()>0:
        return True
    else:
        return False
    

def recycle(dominio,url):
    '''
    '''
    dt=UrlBox()
    query = db.Query(UrlBox).filter('domain = ',dominio ).filter('active = ', False)
    dt = query.fetch(1)[0]
    dt.active=True
    dt.url = url
    dt.date = time.mktime(time.localtime())
    shorted = dt.shorted_url
    db.put(dt)
    return shorted



def computeDomain(url):
    '''
    '''
    parsed = urlparse(url)
    domain = parsed.hostname
    count = 0
    for i in domain:
        if i==".":
                dom=domain[count+1:len(domain)+1]
                break
        count = count+1

    if whitelist.checkInWhite(dom):
        dom = dom[0:len(dom)-3]
    
    return dom


def cancel(url_short):
    try:
        dt=UrlBox()
        query = db.Query(UrlBox).filter('shorted_url = ',url_short ).filter('active = ', True)
        if query.count()>0:
            dt = query.fetch(1)[0]
            dt.active=False
            db.put(dt)
        else:
            print "attenzione"
            print "errore url non presente"
    except:
        error = str(sys.exc_info()[0])
        print error


def main():
    
    whitelist.insertInWhite("facebook.it","sito di social network")
    core_classic("http://www.google.it/abc/lod")
    core_classic("http://www.facebook.it/abc/loa")
    #core_classic("http://www.libero.it/ac/lde")
    #core_custum("http://www.facebook.it/ddd.html","my_facebook_page")
    core_custum("http://msn.xxx.it/la_sss","thiisnot")
    #core_custum("http://www.facebook.it/jjfn","fieradellibro")
    #cancel("www.cerbero.it/facebook_facebook_libro")
    #tot = totalsDomain("facebook")
    #tot2 = totals()
    #print tot  
    #print tot2
    #list = domainList("facebook",10)
    #for i in list:
    #   print i
    
     
  
if __name__ == "__main__":
    main()

        