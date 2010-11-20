from google.appengine.ext import db
from binding import bind
from models import DomainTable
from models import UrlBox
import response
import whitelist
import time
import sys 

def core_classic(url):
    '''
    '''
    try :
        if is_shorted(url):
            du=UrlBox()
            query = db.Query(UrlBox).filter('url = ',url ).filter('active = ', True)
            du = query.fetch(1)[0]
            shorted = du.shorted_url
         
        else:
            mydomain="www.cerbero.it/"
            dominio = computeDomain(url)
            is_recycle=isReciclable(dominio)
            if is_recycle:
                shorted = recycle(dominio,url)
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
    #         
    #res = response.MakeJson(dt.shorted_url,)
        return shorted
    except:
        error = str(sys.exc_info()[0])
        print error 

    
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
    count = 0
    start = 0
    stop = 0
    controllo = 1 

    for c in url:
        if c=='w' and start==0:
                start = count
        elif c=='/' and start>0 :
                stop = count
                break
        else : 
                stop=len(url)
        count = count + 1
        
    if url[0]=='w': 
        dom = url[start+3:stop]
    else:
        dom = url[start+4:stop]

   
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
    
    #whitelist.insertInWhite("facebook.it","sito di social network")
    #core_classic("http://www.google.it/abc/lod")
    #core_classic("http://www.facebook.it/abc/loa")
    #core_classic("http://www.libero.it/ac/lde")
    #core_custum("http://www.facebook.it/ddd.html","my_facebook_page")
    #core_custum("http://www.xxx.it/la_sss","thiisnot")
    #core_custum("http://www.facebook.it/jjfn","fieradellibro")
    #cancel("www.cerbero.it/facebook_facebook_libro")
    #tot = totalsDomain("facebook")
    #tot2 = totals()
    #print tot  
    #print tot2
    list = domainList("facebook",10)
    for i in list:
        print i
    
     
  
if __name__ == "__main__":
    main()

        