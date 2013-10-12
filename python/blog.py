from handler import Handler
from google.appengine.ext import db
import re, hashlib, string, random

SECRET = "not really a secret"

class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class User(db.Model):
    username = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class Blog(Handler):
    def get(self):
        posts = db.GqlQuery("SELECT * FROM Post "
                            "ORDER BY created Desc")
        self.render("blog.html", posts=posts)

def make_salt():
    return ''.join([random.choice(string.letters) for x in range(5)])

def hash_user_id(user_id):
    return str(user_id) + '|' + \
        hashlib.sha256(SECRET + str(user_id)).hexdigest()

def hash_password(password, salt=None):
    if salt == None:
        salt = make_salt()
    return hashlib.sha256(SECRET + password + salt).hexdigest() + ',' + salt

class BlogSignup(Handler):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    def valid_username(self, username):
        return username and self.USER_RE.match(username)

    def duplicate_username(self, username):
        stored_username = User.all().filter('username =', username).get()
        if stored_username:
            return True
        return False


    PASSWORD_RE = re.compile(r"^.{3,20}$")
    def valid_password(self, password):
        return password and self.PASSWORD_RE.match(password)

    EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
    def valid_email(self, email):
        return email == '' or self.EMAIL_RE.match(email)


    def render_page(self, username="", email="", error_username="",
                    error_password="",error_verify="", error_email=""):
        self.render("blog_signup.html", username=username, email=email,
                    error_username=error_username,
                    error_password=error_password, error_verify=error_verify,
                    error_email=error_email);

    def get(self):
        self.render_page();

    def post(self):
        username = self.request.get('username');
        password = self.request.get('password');
        verify = self.request.get('verify');
        email = self.request.get('email');

        params = {"username": username, "email":email}

        have_error = False
        if not self.valid_username(username):
            have_error = True
            params["error_username"] = "Invalid username"
        elif self.duplicate_username(username):
            have_error = True
            params["error_username"] = "Username already exists"
        if not self.valid_password(password):
            have_error = True
            params["error_password"] = "Invalid password"
        elif password != verify:
            have_error = True
            params["error_verify"] = "Passwords didn't match"
        if not self.valid_email(email):
            have_error = True
            params["error_email"] = "Invalid email"

        if have_error:
            self.render_page(**params)
        else:
            user = User(username=username, password=hash_password(password))
            user.put()
            cookie = str("user_id=%s; Path=/" %
                         hash_user_id(user.key().id()))
            self.response.headers.add_header("Set-Cookie", cookie)
            self.redirect('/blog/welcome')

class BlogWelcome(Handler):
    def get(self):
        user_cookie = self.request.cookies.get('user_id').split('|')
        user = User.get_by_id(int(user_cookie[0]))
        if user and user_cookie == hash_user_id(user_cookie[0]).split('|'):
            self.response.write("Welcome, %s!" % user.username)
        else:
            self.redirect('/blog/signup')

class NewPost(Handler):
    def render_page(self, subject="", content="", error=""):
        self.render("blog_new_post.html", subject=subject, content=content,
                    error=error)

    def get(self):
        self.render_page()

    def post(self):
        subject = self.request.get("subject")
        content = self.request.get("content")

        if subject and content:
            post = Post(subject=subject, content=content)
            post.put()

            self.redirect("/blog/" + str(post.key().id()))
        else:
            error = "Please enter both a subject and content!"
            self.render_page(subject, content, error)

class BlogPost(Handler):
    def render_page(self, blog_id=None):
        blog_post = Post.get_by_id(blog_id, parent=None)
        self.render("blog_post.html", blog_post=blog_post,
                    created_date=blog_post.created.date)

    def get(self, blog_id):
        self.render_page(int(blog_id))
