from handler import Handler
from google.appengine.ext import db

class Art(db.Model):
    title = db.StringProperty(required = True)
    art = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class AsciiChan(Handler):
    def render_home(self, title="", art="", error=""):
        arts = db.GqlQuery("SELECT * FROM Art "
                           "ORDER BY created DESC")

        self.render("ascii.html", title=title, art=art, error=error, arts=arts)

    def get(self):
        self.render_home()

    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")

        if title and art:
            a = Art(title = title, art = art)
            a.put()

            self.redirect("/ascii")
        else:
            error = "we need both a title and some artwork!"
            self.render_home(title, art, error)
