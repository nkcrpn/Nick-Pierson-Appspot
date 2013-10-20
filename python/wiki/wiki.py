from ..handler import Handler
from ..data import Page

class WikiHome(Handler):
    def render_page(self, logged_in=False, username=""):
        self.render("wiki_home.html", logged_in=logged_in,
                    username=username);

    def get(self):
        if self.user:
            self.render_page(True, self.user.username)
        else:
            self.render_page();

    def post(self):
        topic = self.request.get('topic').split(' ')
        self.redirect('/wiki/' + topic[0])

class WikiPage(Handler):
    def get(self, page):
        topic = page.split('/')[-1]

        if not self.user:
            self.render("wiki_no_page.html", topic=topic)
            return

        self.redirect('/wiki/edit/' + topic)

class WikiEdit(Handler):
    def render_page(self, username, topic, content=""):
        self.render("wiki_edit.html", username=username,
                    topic=topic, content=content)

    def get(self, page):
        topic = page.split('/')[-1]

        if not self.user:
            self.redirect('/wiki/' + topic)

        page = Page.get_by_topic(topic)
        if page:
            self.render_page(self.user.username, topic, page.content)
        else:
            self.render_page(self.user.username, topic)

    def post(self, page):
        topic = page.split('/')[-1]
        content = self.request.get('content')

        if not self.user:
            return

        page = Page.get_by_topic(topic)
        if page:
            page.content = content
            page.put()
        else:
            page = Page.make_page(topic, content)

        self.redirect('/wiki/' + topic)
