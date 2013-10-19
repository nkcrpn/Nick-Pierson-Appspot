from ..handler import Handler

class WikiHome(Handler):
    def render_page(self, logged_in=False):
        self.render("wiki_home.html");

    def get(self):
        self.render_page();

    def post(self):
        topic = self.request.get('topic').split(' ')
        self.redirect('/wiki/' + topic[0])

class WikiPage(Handler):
    def get(self, page):
        topic = page.split('/')[2]

        self.render("wiki_no_page.html")
