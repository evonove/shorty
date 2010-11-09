import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class BoxUrl(db.Model):
    url= db.StringProperty(multiline=False)
    shorted_url = db.StringProperty(multiline=False)
   

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write('<html><body>')

        lista_url = db.GqlQuery("SELECT * FROM BoxUrl")

        for url in lista_url:
            self.response.out.write(' url :')
            self.response.out.write(cgi.escape(url.url))
            self.response.out.write('shrted url:')
            self.response.out.write(cgi.escape(url.shorted_url))

        # Write the submission form and the footer of the page
        self.response.out.write("""
              <form action="/sign" method="post">
                <div><textarea name="content" rows="3" cols="60"></textarea></div>
                <div><input type="submit" value="Sign ScriviUrl"></div>
              </form>
            </body>
          </html>""")

class ScriviUrl(webapp.RequestHandler):
    def post(self):
        box_url = BoxUrl()
        box_url.url = self.request.get('content')
        box_url.shorted_url=self.request.get('content')
        box_url.put()
        self.redirect('/')

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/sign', ScriviUrl)],
                                     debug=True)


def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()