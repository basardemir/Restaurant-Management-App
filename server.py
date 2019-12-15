from flask import Flask
import views

app = Flask(__name__)


app.config['SECRET_KEY'] = 'db2019'

app.add_url_rule("/", view_func = views.home_page)
app.add_url_rule("/404-not-found", view_func= views.not_found_page)
app.add_url_rule("/403-access-denied", view_func= views.access_denied_page)

## Company
app.add_url_rule("/companies", view_func = views.companies_page, methods=["GET", "POST"])
app.add_url_rule("/companies/create", view_func = views.company_add_page, methods=["GET", "POST"])
app.add_url_rule("/companies/<int:company_key>/details", view_func = views.company_details_page, methods=["GET", "POST"])
app.add_url_rule("/companies/<int:company_key>/edit", view_func = views.company_update_page, methods=["GET", "POST"])
app.add_url_rule("/companies/<int:company_key>/delete", view_func = views.company_delete_page, methods=["GET", "POST"])
app.add_url_rule("/companies/<int:company_key>/set_founder", view_func = views.company_setfounder_page, methods=["GET", "POST"])

## Card
app.add_url_rule("/cards", view_func = views.cards_page, methods=["GET", "POST"])
app.add_url_rule("/cards/create", view_func = views.card_add_page, methods=["GET", "POST"])
app.add_url_rule("/cards/<int:card_key>/details", view_func = views.card_details_page, methods=["GET", "POST"])
app.add_url_rule("/cards/<int:card_key>/edit", view_func = views.card_update_page, methods=["GET", "POST"])
app.add_url_rule("/cards/<int:card_key>/delete", view_func = views.card_delete_page, methods=["GET", "POST"])

## Order
app.add_url_rule("/orders", view_func = views.orders_page, methods=["GET", "POST"])
app.add_url_rule("/payment/<meals>", view_func = views.payment_page, methods=["GET", "POST"])
app.add_url_rule("/orders/<int:order_key>/details", view_func = views.order_details_page, methods=["GET", "POST"])
app.add_url_rule("/orders/<int:order_key>/edit", view_func = views.order_update_page, methods=["GET", "POST"])
app.add_url_rule("/orders/<int:order_key>/cancel", view_func = views.order_cancel_page, methods=["GET", "POST"])


##COUNTRY TABLE
app.add_url_rule("/countries", view_func=views.country_page, methods=["GET", "POST"]) ##Enterance Page to country table
app.add_url_rule("/countries/create", view_func=views.country_add_page, methods=["GET", "POST"]) 
app.add_url_rule("/countries/<int:country_key>", view_func=views.country_read_page)
app.add_url_rule("/countries/<int:country_key>/edit", view_func=views.country_update_page, methods=["GET","POST"])
app.add_url_rule("/countries/<int:country_key>/delete", view_func=views.country_delete_page)
#TIMEZONE TABLE
app.add_url_rule("/tz", view_func=views.tz_page,) 
#Province Table
app.add_url_rule("/provinces", view_func=views.province_page, methods=["GET","POST"])
app.add_url_rule("/provinces/create", view_func=views.province_add_page, methods=["GET", "POST"]) 
app.add_url_rule("/provinces/<int:province_key>", view_func=views.province_read_page)
app.add_url_rule("/provinces/<int:province_key>/edit", view_func=views.province_update_page, methods=["GET","POST"])
app.add_url_rule("/provinces/<int:province_key>/delete", view_func=views.province_delete_page) #question
#Location Table
app.add_url_rule("/location", view_func=views.location_page, methods=["GET", "POST"])
app.add_url_rule("/location/create", view_func=views.location_add_page, methods=["GET", "POST"]) 
app.add_url_rule("/location/<int:location_key>", view_func=views.location_read_page)
app.add_url_rule("/location/<int:location_key>/edit", view_func=views.location_update_page, methods=["GET","POST"])
app.add_url_rule("/location/<int:location_key>/delete", view_func=views.location_delete_page) #question
#Users
app.add_url_rule("/users", view_func=views.users_page)
app.add_url_rule("/users/signin", view_func=views.signin_page, methods=["GET", "POST"])
app.add_url_rule("/users/profile", view_func=views.profile_page, methods=["GET", "POST"])
app.add_url_rule("/users/create", view_func=views.add_user_page, methods=["GET", "POST"])
app.add_url_rule("/users/logout", view_func=views.logout_page, methods=["POST"])
app.add_url_rule("/users/editsocialmedia", view_func=views.editsocialmedia_page, methods=["GET", "POST"])
app.add_url_rule("/users/editcontactinfo", view_func=views.editcontactinfo_page, methods=["GET", "POST"])
app.add_url_rule("/users/editperson", view_func=views.editperson_page, methods=["GET", "POST"])
app.add_url_rule("/users/edituseraccount", view_func=views.edituser_page, methods=["GET", "POST"])

#Meals
app.add_url_rule("/meals", view_func=views.meal_page, methods=["GET", "POST"])
app.add_url_rule("/meals/<int:food_id>/food_value", view_func=views.food_value_page)
app.add_url_rule("/meals/add_meal", view_func=views.add_meal_page, methods=["GET", "POST"])
app.add_url_rule("/meals/<int:food_id>/delete", view_func=views.delete_meal_page, methods=["GET", "POST"])
app.add_url_rule("/meals/<int:food_id>/update", view_func=views.update_meal_page, methods=["GET", "POST"])

#Ingredients
app.add_url_rule("/ingredients/add", view_func=views.add_ingredient_page, methods=["GET", "POST"])
app.add_url_rule("/ingredients", view_func=views.show_ingredients, methods=['GET'])
app.add_url_rule("/ingredients/<int:ingred_id>/ingredient_value", view_func=views.ingredient_nutr_values)
app.add_url_rule("/ingredients/<int:ingred_id>/delete", view_func=views.delete_ingredient_page, methods=["GET", "POST"])
app.add_url_rule("/ingredients/<int:ingred_id>/update", view_func=views.update_ingredient_page, methods=["GET", "POST"])

#Restaurants
app.add_url_rule("/restaurant/add", view_func=views.add_restaurant_page, methods=["GET", "POST"])
app.add_url_rule("/restaurant", view_func=views.show_restaurant_page)
app.add_url_rule("/restaurant/<int:restaurant_id>/update", view_func=views.update_restaurant_page, methods=["GET", "POST"])
app.add_url_rule("/restaurant/<int:restaurant_id>/delete", view_func=views.delete_restaurant_page, methods=["GET", "POST"])

if __name__ == "__main__":
    app.run()
