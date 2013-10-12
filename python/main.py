import webapp2
from home import Home
from rot13 import Rot13
from asciichan import AsciiChan
from blog import *

application = webapp2.WSGIApplication(
    [(r'/', Home), (r'/rot13', Rot13),
     (r'/ascii', AsciiChan), (r'/blog/?', Blog), (r'/blog/newpost', NewPost),
     (r'/blog/signup', BlogSignup), (r'/blog/welcome', BlogWelcome),
     (r'/blog/(\d+)', BlogPost)],
     debug = True)
