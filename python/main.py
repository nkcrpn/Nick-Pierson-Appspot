import webapp2
from home import Home
from rot13 import Rot13
from asciichan import AsciiChan
from blog import *
from wiki.wiki import *
from accounts import *

PAGE_RE = r'(/wiki/(?:[a-zA-Z0-9_-]+/?)*)'
application = webapp2.WSGIApplication(
    [(r'/', Home),
     (r'/rot13', Rot13),
     (r'/ascii', AsciiChan),
     (r'/signup', SignUp),
     (r'/login', LogIn),
     (r'/logout', LogOut),
     (r'/blog/?', Blog),
     (r'/blog/newpost', NewPost),
     (r'/blog/flush', BlogFlush),
     (r'/blog/(\d+)', BlogPost),
     (r'/blog/?.json', BlogJSON),
     (r'/blog/(\d+)/?.json', BlogPostJSON),
     (r'/wiki/?', WikiHome),
     (PAGE_RE, WikiPage)],
     debug = True)
