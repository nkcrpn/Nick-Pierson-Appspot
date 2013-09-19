import webapp2
import cgi
import re

signup_form = """
<form method='post'>
    <h1>Signup</h1>
    <label>
        Username
        <input type="text" name="username" value="%(username)s">
        %(error_username)s
    </label>
    <br>
    <label>
        Password
        <input type="password" name="password">
        %(error_password)s
    </label>
    <br>
    <label>
        Verify Password
        <input type="password" name="verify">
        %(error_verify)s
    </label>
    <br>
    <label>
        Email (optional)
        <input type="text" name="email" value="%(email)s">
        %(error_email)s
    </label>
    <br>
    <input type="submit">
</form>
"""

class SignUp(webapp2.RequestHandler):
    def write_form(self, err_username="", err_password="", err_verify="",
                    err_email="", username="", email=""):
        self.response.out.write(signup_form % { 'error_username' : err_username,
                                                'error_password' : err_password,
                                                'error_verify' : err_verify,
                                                'error_email' : err_email,
                                                'username' : username,
                                                'email' : email })

    def get(self):
        self.write_form()

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        if not valid_username(username) and not valid_password(password):
            self.write_form(username=username, email=email,
                        err_username="Not a valid username.",
                        err_password="Not a valid password.")
        elif not valid_username(username):
            self.write_form(username=username, email=email,
                        err_username="Not a valid username.")
        elif not valid_password(password):
            self.write_form(username=username, email=email,
                        err_password="Not a valid password.")
        elif password != verify:
            self.write_form(username=username, email=email,
                        err_verify="Passwords don't match.")
        elif email and not valid_email(email):
            self.write_form(username=username, email=email,
                        err_email="Not a valid email.")
        else:
            #TODO this feels wrong
            self.redirect('/welcome?username=' + username)

class Welcome(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Welcome, " + self.request.get('username'))

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_username(username):
    return USER_RE.match(username)

def valid_password(password):
    return PASS_RE.match(password)

def valid_email(email):
    return EMAIL_RE.match(email)
