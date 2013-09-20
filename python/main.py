import webapp2
from handler import Handler
from rot13 import Rot13
from asciichan import AsciiChan
from blog import *

class MainPage(Handler):
    def get(self):
        self.render("main.html")

application = webapp2.WSGIApplication(
    [(r'/', MainPage), (r'/rot13', Rot13),
     (r'/ascii', AsciiChan), (r'/blog', Blog), (r'/blog/newpost', NewPost),
     (r'/blog/(\d+)', BlogPost)], debug = True)
