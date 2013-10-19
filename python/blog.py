from handler import Handler
from google.appengine.ext import db
import re, hashlib, string, random, json
from datetime import datetime

SECRET = "not really a secret"

class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class User(db.Model):
    username = db.StringProperty(required = True)
    password = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

def make_salt():
    return ''.join([random.choice(string.letters) for x in range(5)])

def hash_user_id(user_id):
    return str(user_id) + '|' + \
        hashlib.sha256(SECRET + str(user_id)).hexdigest()

def hash_password(password, salt=None):
    if salt == None:
        salt = make_salt()
    return hashlib.sha256(SECRET + password + salt).hexdigest() + ',' + salt

def get_user(username):
    return User.all().filter("username = ", username).get()

def valid_login(username, password):
    db_user = get_user(username)
    if not db_user:
        return False
    db_password = db_user.password
    salt = db_password.split(',')[1]
    hashed_password = hash_password(password, salt);
    if db_password == hashed_password:
        return True
    else:
        return False

def show_welcome(self, user):
    cookie = str("user_id=%s; Path=/" %
                     hash_user_id(user.key().id()))
    self.response.headers.add_header("Set-Cookie", cookie)
    self.redirect('/blog/welcome')

CACHE = {}
front_page_key = "front page"
def get_all_posts():
    if front_page_key in CACHE:
        return CACHE[front_page_key][0]
    else:
        posts =  db.GqlQuery("SELECT * FROM Post "
                       "ORDER BY created DESC")
        CACHE[front_page_key] = (posts, datetime.now())
        return posts

def get_home_query_diff():
    if front_page_key in CACHE:
        return (datetime.now() - CACHE[front_page_key][1]).seconds
    else:
        return 0

def get_post(post_id):
    if post_id in CACHE:
        return CACHE[post_id][0]
    else:
        post = Post.get_by_id(post_id, parent=None)
        CACHE[post_id] = (post, datetime.now())
        return post

def get_query_diff(post_id):
    if post_id in CACHE:
        return (datetime.now() - CACHE[post_id][1]).seconds
    else:
        return 0

class Blog(Handler):
    def get(self):
        difference = get_home_query_diff()
        posts = get_all_posts()
        self.render("blog.html", posts=posts, seconds=difference)

class BlogSignup(Handler):
    USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    def valid_username(self, username):
        return username and self.USER_RE.match(username)

    def duplicate_username(self, username):
        stored_user = get_user(username)
        if stored_user:
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
            show_welcome(self, user)

class BlogLogin(Handler):
    def render_page(self, error=""):
        self.render("blog_login.html", error=error);

    def get(self):
        self.render_page();

    def post(self):
        username = self.request.get('username');
        password = self.request.get('password');

        if valid_login(username, password):
            show_welcome(self, get_user(username))
        else:
            self.render_page(error="Invalid login.");

class BlogLogout(Handler):
    def get(self):
        cookie = str("user_id=; Path=/")
        self.response.headers.add_header("Set-Cookie", cookie)
        self.redirect('/blog/signup')


class BlogWelcome(Handler):
    def get(self):
        user_cookie = self.request.cookies.get('user_id').split('|')

        user = None
        if user_cookie[0]:
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

            CACHE.pop(front_page_key, None)

            self.redirect("/blog/" + str(post.key().id()))
        else:
            error = "Please enter both a subject and content!"
            self.render_page(subject, content, error)

class BlogPost(Handler):
    def render_page(self, blog_id=None, seconds=0):
        blog_post = get_post(blog_id)
        self.render("blog_post.html", blog_post=blog_post,
                    created_date=blog_post.created.date,
                    seconds=seconds)

    def get(self, blog_id):
        self.render_page(int(blog_id), get_query_diff(int(blog_id)))

class BlogFlush(Handler):
    def get(self):
        CACHE.clear()
        self.redirect('/blog/')

class BlogJSON(Handler):
    def get(self):
        posts = Post.all()
        posts = list(posts)

        results = []
        for post in posts:
            results.append({'content' : post.content,
                            'subject' : post.subject,
                            'created' : str(post.created)
                            })
        self.response.headers['Content-Type'] = "application/json"
        self.response.out.write(json.dumps(results))

class BlogPostJSON(Handler):
    def get(self, blog_id):
        post = Post.get_by_id(int(blog_id), parent=None)

        if post:
            self.response.headers['Content-Type'] = "application/json"
            self.response.out.write(json.dumps({'content' : post.content,
                                                'subject' : post.subject,
                                                'created' : str(post.created)
                                                }))
        else:
            self.response.out.write("Invalid post id")
