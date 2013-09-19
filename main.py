import webapp2
import cgi
from python.handler import Handler
from python.rot13 import Rot13
from python.signup import *
from python.asciichan import AsciiChan
from python.blog import Blog

class MainPage(Handler):
    def get(self):
        self.render("main.html")

application = webapp2.WSGIApplication(
    [('/', MainPage), ('/rot13', Rot13), ('/signup', SignUp),
     ('/welcome', Welcome), ('/ascii', AsciiChan), ('/blog', Blog),
     ('/blog/newpost', Blog)], debug = True)
