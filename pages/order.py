from flask import Flask, render_template, request, redirect, url_for, session, abort

from models.orders import *

from .forms.order_form import OrderForm
from .forms.comment_form import CommentForm

from datetime import datetime

def orders_page():
  if session and session["logged_in"] == False:
    return redirect(url_for('signin_page'))
  else:
    orders = get_all_orders()
    return render_template("/orders/index.html", orders = orders,
      date_now = datetime.now())

def payment_page(meals):
  if session and session["logged_in"] == False:
    return redirect(url_for('signin_page'))
  else:
    if meals:
      meals

    #meal_id #meal_name #stock_size #price
    meals_list = [
      (28, "ot", 50, 25.3),
      (29, "mot", 30, 12.3),
    ]
    #max_amount - stock adedi
    
    order = OrderForm()
    
    if order.validate_on_submit():
      
      ar = []
      for i in range(1, len(meals_list)+1):
        ar.append( request.form.get("amount_of_check_{}".format(i)) ) 

      user_id = session['userid']
      restaurant_id = 14

      order_info = (
        order.order["price"].data,
        order.order["note"].data,
        order.order["payment_type"].data,
        order.order["rate"].data,
        order.order["end_at"].data,
        datetime.now(),
        restaurant_id,
        user_id
      )

      order_key = add_order(order_info)
      for i in range(0, len(ar)):
        connect_order_and_food( (order_key, meals_list[i][0], ar[i]) )
      
      return redirect(url_for("home_page")) ## will go details...
    
    return render_template(
      "/orders/payment.html",
      form = order,
      meals = meals_list
    )

def order_cancel_page(order_key):
  if session and session["logged_in"] == False:
    return redirect(url_for('signin_page'))
  else:
    if request.method == "POST":
      delete_order(order_key)
      return redirect(url_for("orders_page"))
    return render_template("/orders/cancel.html")

def order_update_page(order_key):
  if session and session["logged_in"] == False:
    return redirect(url_for('signin_page'))
  else:
    
    order = OrderForm()
    
    _order = get_order(order_key, "order")[0]

    if order.validate_on_submit():
      
      order_info = (
        order.order["price"].data,
        order.order["note"].data,
        order.order["payment_type"].data,
        order.order["rate"].data,
        order.order["end_at"].data,
        order_key
      )

      order_key = update_order(order_info)
      
      return redirect(url_for("order_details_page", order_key = order_key))

    order.order["price"].data = _order["price"]
    order.order["note"].data = _order["note"]
    order.order["payment_type"].data = _order["type"]
    order.order["rate"].data = _order["rate"]
    order.order["end_at"].data = _order["end_at"]

    return render_template(
      "/orders/edit.html",
      form = order
    )

def order_details_page(order_key):

  if session and session["logged_in"] == False:
    return redirect(url_for('signin_page'))
  else:
    order = get_detailed_order(order_key, "order")
    
    if(order is None):
      abort(404)
    return render_template(
      "/orders/details.html",
      order = order
    )

def my_orders_page():
  if session and session["logged_in"] == False:
    return redirect(url_for('signin_page'))
  else:

    myorders = get_order(session["userid"], "user")

    return render_template(
      "/orders/myorders.html",
      myorders = myorders,
      date_now = datetime.now()
    )

def comment_order_page(order_key):
  if session and session["logged_in"] == False:
    return redirect(url_for('signin_page'))
  else:

    comment = CommentForm()

    if comment.validate_on_submit():
      
      user_id     = session['userid']

      comment_info = (
        comment.comment["title"].data,
        comment.comment["description"].data,
        int(comment.comment["speed"].data),
        int(comment.comment["taste"].data),
        user_id,
        order_key
      )

      make_comment_to_order(comment_info)

      return redirect(url_for("order_details_page", order_key = order_key))
      
    return render_template(
      "/orders/comment.html",
      form = comment
    )
    