import webapp2
from home import Home
from rot13 import Rot13
from asciichan import AsciiChan
from blog import *
from wiki.wiki import *

PAGE_RE = r'(/wiki/(?:[a-zA-Z0-9_-]+/?)*)'
application = webapp2.WSGIApplication(
    [(r'/', Home),
     (r'/rot13', Rot13),
     (r'/ascii', AsciiChan),
     (r'/blog/?', Blog),
     (r'/blog/newpost', NewPost),
     (r'/blog/signup', BlogSignup),
     (r'/blog/welcome', BlogWelcome),
     (r'/blog/login', BlogLogin),
     (r'/blog/logout', BlogLogout),
     (r'/blog/flush', BlogFlush),
     (r'/blog/(\d+)', BlogPost),
     (r'/blog/?.json', BlogJSON),
     (r'/blog/(\d+)/?.json', BlogPostJSON),
     (r'/wiki/?', WikiHome),
     (r'/wiki/signup', WikiSignUp),
     (PAGE_RE, WikiPage)],
     debug = True)
