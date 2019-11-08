from flask import Flask

import views

def create_app():
    app = Flask(__name__)
    
    ## Urls for application
    app.add_url_rule("/", view_func = views.home_page)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run()
