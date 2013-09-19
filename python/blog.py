from handler import Handler
from google.appengine.ext import db

class Post(db.Model):
    title = db.StringProperty(required = True)
    message = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class Blog(Handler):
    def get(self):
        self.render("blog.html")
