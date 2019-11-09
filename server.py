from flask import Flask

import views

app = Flask(__name__)

if __name__ == "__main__":
    app.add_url_rule("/", view_func = views.home_page)
    app.run()
