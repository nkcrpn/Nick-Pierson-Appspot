from handler import Handler
from google.appengine.ext import db

class Post(db.Model):
    title = db.StringProperty(required = True)
    message = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class Blog(Handler):
    def get(self):
        posts = db.GqlQuery("SELECT * FROM Post "
                            "ORDER BY created Desc")
        self.render("blog.html", posts=posts)

class NewPost(Handler):
    def render_page(self, title="", message="", error=""):
        self.render("new_post.html", title=title, message=message,
                    error=error)

    def get(self):
        self.render_page()

    def post(self):
        title = self.request.get("title")
        message = self.request.get("message")

        if title and message:
            post = Post(title=title, message=message)
            post.put()

            self.redirect("/blog/" + str(post.key().id()))
        else:
            error = "Please enter both a title and message!"
            self.render_page(title, message, error)

class BlogPost(Handler):
    def render_page(self, blog_id=None):
        blog_post = Post.get_by_id(blog_id, parent=None)
        self.render("blog_post.html", blog_post=blog_post,
                    created_date=blog_post.created.date)

    def get(self, blog_id):
        self.render_page(int(blog_id))
