from google.appengine.ext import db
from utils import *

class User(db.Model):
    username = db.StringProperty(required = True)
    password = db.StringProperty(required = True)

    @classmethod
    def register_user(cls, username, password):
        password = hash_password(password)
        user = cls(username=username, password=password)
        user.put()
        return user

    @classmethod
    def valid_login(cls, username, password):
        stored_user = cls.get_user(username)
        if not stored_user:
            return False

        stored_password = stored_user.password
        salt = stored_password.split(',')[1]
        hashed_password = hash_password(password, salt)

        if hashed_password == stored_password:
            return True
        else:
            return False

    @classmethod
    def user_exists(cls, username):
        stored_user = cls.get_user(username)
        if stored_user:
            return True
        return False

    @classmethod
    def get_user(cls, username):
        return cls.all().filter("username = ", username).get()

class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class Page(db.Model):
    topic = db.StringProperty(required = True)
    content = db.TextProperty(required = True)

    @classmethod
    def make_page(cls, topic, content):
        page = cls(topic=topic, content=content)
        page.put()

    @classmethod
    def get_by_topic(cls, topic):
        return cls.all().filter("topic = ", topic).get()
