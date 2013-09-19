import webapp2
from python.handler import Handler
from python.rot13 import Rot13
from python.signup import *
from python.asciichan import AsciiChan
from python.blog import *

class MainPage(Handler):
    def get(self):
        self.render("main.html")

application = webapp2.WSGIApplication(
    [(r'/', MainPage), (r'/rot13', Rot13), (r'/signup', SignUp),
     (r'/welcome', Welcome), (r'/ascii', AsciiChan), (r'/blog', Blog),
     (r'/blog/newpost', NewPost), (r'/blog/(\d+)', BlogPost)], debug = True)
