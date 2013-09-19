import webapp2
import jinja2

my_dir = "/home/nick/Dev/Workspace/AppEngine/Udacity/templates/"
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(my_dir),
                               autoescape=True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))
