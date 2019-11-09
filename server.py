from flask import Flask

import views

app = Flask(__name__)

def create_app():
    ## Urls for application
    app.add_url_rule("/", view_func = views.home_page)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run()
