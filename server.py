from flask import Flask

import views

app = Flask(__name__)
app.add_url_rule("/", view_func = views.home_page)

app.add_url_rule("/companies", view_func = views.companies_page)
app.add_url_rule("/companies/create", view_func = views.company_add_page)
app.add_url_rule("/companies/<int:company_key>", view_func = views.company_details_page)
app.add_url_rule("/companies/<int:company_key>/edit", view_func = views.company_update_page)
app.add_url_rule("/companies/<int:company_key>/delete", view_func = views.company_delete_page)

##COUNTRY TABLE
app.add_url_rule("/countries", view_func=views.country_page, methods=["GET", "POST"]) ##Enterance Page to country table
app.add_url_rule("/countries/create", view_func=views.country_add_page, methods=["GET", "POST"]) 
app.add_url_rule("/countries/<int:country_key>", view_func=views.country_read_page)
app.add_url_rule("/countries/<int:country_key>/edit", view_func=views.country_update_page)

#Users
app.add_url_rule("/users", view_func=views.users_page)
app.add_url_rule("/users/create", view_func=views.add_user_page, methods=["GET", "POST"])

#Meals
app.add_url_rule("/meals", view_func=views.meal_page)
app.add_url_rule("/meals/food_values", view_func=views.food_value_page)
app.add_url_rule("/meals/add_meal", view_func=views.add_meal_page)


if __name__ == "__main__":
    app.run()
