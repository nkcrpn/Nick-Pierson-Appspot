import re, string, random, hmac
from private import *
from hashlib import sha256

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASSWORD_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASSWORD_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_email(email):
    return email == '' or self.EMAIL_RE.match(email)

def hash_password(password, salt=None):
    if salt == None:
        salt = make_salt()
    hashed = hmac.new(SECRET, password + salt, sha256).hexdigest()
    return hashed + ',' + salt

def make_salt():
    return ''.join([random.choice(string.letters) for x in range(5)])

def hash_user_id(user_id):
    return str(user_id) + '|' + \
        hmac.new(SECRET, str(user_id), sha256).hexdigest()
