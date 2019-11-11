from flask import Flask

import views

app = Flask(__name__)
app.add_url_rule("/", view_func = views.home_page)

app.add_url_rule("/companies", view_func = views.companies_page)
app.add_url_rule("/companies/create", view_func = views.company_add_page)
app.add_url_rule("/companies/<int:company_key>", view_func = views.company_details_page)
app.add_url_rule("/companies/<int:company_key>/edit", view_func = views.company_update_page)
app.add_url_rule("/companies/<int:company_key>/delete", view_func = views.company_delete_page)


if __name__ == "__main__":
    app.run()
