from handler import Handler
from utils import *
from data import *
import urlparse

class Accounts(Handler):
    def set_referrer_cookie(self):
        referer = self.request.headers.get('referer')
        if referer:
            path = urlparse.urlparse(referer)[2]
            if path != '/login' and path != '/signup':
                cookie = str("referrer=%s; Path=/" % path)
                self.response.headers.add_header("Set-Cookie", cookie)
                return

        cookie = str("referrer=/; Path=/")
        self.response.headers.add_header("Set-Cookie", cookie)

    def set_login_cookie(self, user):
        user_cookie = hash_user_id(user.key().id())
        cookie = str("user_id=%s; Path=/" % user_cookie)
        self.response.headers.add_header("Set-Cookie", cookie)

    def return_user(self):
        referrer = self.request.cookies.get('referrer')
        if referrer:
            self.redirect(referrer)
        else:
            self.redirect('/')

class SignUp(Accounts):
    def render_page(self, username="", error_username="",
                    error_password="", error_verify=""):
        self.render("signup.html", username=username,
                    error_username=error_username,
                    error_password=error_password, error_verify=error_verify)

    def get(self):
        self.set_referrer_cookie()
        self.render_page()

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')

        have_error = False
        args = {'username' : username}
        if not valid_username(username):
            have_error = True
            args['error_username'] = "Invalid username"
        elif User.user_exists(username):
            have_error = True
            args['error_username'] = "Username already exists"
        if not valid_password(password):
            have_error = True
            args['error_password'] = "Invalid password"
        if verify != password:
            have_error = True
            args['error_verify'] = "Passwords don't match"

        if have_error:
            self.render_page(**args)
        else:
            user = User.register_user(username, password)
            self.set_login_cookie(user)
            self.return_user()

class LogIn(Accounts):
    def render_page(self, error=""):
        self.render("login.html", error=error);

    def get(self):
        self.set_referrer_cookie()
        self.render_page();

    def post(self):
        username = self.request.get('username');
        password = self.request.get('password');

        if User.valid_login(username, password):
            user = User.get_user(username)
            self.set_login_cookie(user)
            self.return_user()
        else:
            self.render_page(error="Invalid login");

class LogOut(Accounts):
    def get(self):
        cookie = str("user_id=; Path=/")
        self.response.headers.add_header("Set-Cookie", cookie)
        self.redirect('/')
