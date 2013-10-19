from ..handler import Handler

class WikiHome(Handler):
    def render_page(self, logged_in=False):
        self.render("wiki_home.html");

    def get(self):
        self.render_page();
