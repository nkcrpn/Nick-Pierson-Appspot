from handler import Handler
from google.appengine.ext import db
import hashlib, string, random, json
from datetime import datetime
from utils import *
from data import *

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
