import os, webapp2, jinja2
from data import User
from utils import *

template_dir = os.path.join(os.path.dirname(__file__), '../templates')
jinja_env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def read_secure_cookie(self):
        user_cookie = self.request.cookies.get('user_id')
        if not user_cookie:
            return None

        cookie_user_id = user_cookie.split('|')
        hashed_user_id = hash_user_id(cookie_user_id[0]).split('|')

        if hashed_user_id == cookie_user_id:
            return user_cookie
        return None

    def get_user(self):
        user_cookie = self.read_secure_cookie()
        if user_cookie:
            user_cookie = user_cookie.split('|')
            return User.get_by_id(int(user_cookie[0]))
        return None

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        user = self.get_user()
        self.user = user
