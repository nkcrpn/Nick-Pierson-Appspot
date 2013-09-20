from handler import Handler

class Home(Handler):
    def get(self):
        self.render("home.html")
