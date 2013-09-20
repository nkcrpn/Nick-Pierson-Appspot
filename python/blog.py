from handler import Handler
from google.appengine.ext import db

class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

class Blog(Handler):
    def get(self):
        posts = db.GqlQuery("SELECT * FROM Post "
                            "ORDER BY created Desc")
        self.render("blog.html", posts=posts)

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
