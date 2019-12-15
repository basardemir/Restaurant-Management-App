from flask import Flask, render_template, request, redirect, url_for, session, abort

from models.orders import *

from .forms.order_form import OrderForm

import datetime

def orders_page():
  '''if session and session["logged_in"] == False:
    return redirect(url_for('signin_page'))
  #elif session['membershiptype'] != 'Admin':
    #return redirect(url_for("access_denied_page"))
  else:
    orders = get_all_orders()
    return render_template("/orders/index.html", orders = orders)'''
  
  return redirect(url_for("payment_page", meals=[22,23]))

def payment_page(meals):
  if session and session["logged_in"] == False:
    return redirect(url_for('signin_page'))
  else:
    if meals:
      print(meals)

    #meal_id #meal_name #stock_size #price
    meals_list = [
      (23, "ot", 50, 25.3),
      (22, "mot", 30, 12.3),
    ]
    #max_amount - stock adedi
    
    order = OrderForm()
    
    if order.validate_on_submit():
      order_key = -1
      return redirect(url_for("order_details_page", order_key = order_key))
    
    return render_template(
      "/orders/payment.html",
      form = order,
      meals = meals_list
    )

def order_cancel_page(order_key):
  if session and session["logged_in"] == False:
    return redirect(url_for('signin_page'))
  elif session['membershiptype'] != 'Boss':
    return redirect(url_for("access_denied_page"))
  else:
    if request.method == "POST":
      delete_order(order_key)
      return redirect(url_for("orders_page"))
    return render_template("/orders/delete.html")

def order_update_page(order_key):
  if session and session["logged_in"] == False:
    return redirect(url_for('signin_page'))
  elif session['membershiptype'] != 'Boss':
    return redirect(url_for("access_denied_page"))
  else:
    _order = get_order(order_key)
    
    if(_order is None):
      return redirect(url_for("not_found_page"))
    
    _contact  = get_contact_of_order(_order['contact_id'])
    order   = OrderForm()

    if order.validate_on_submit():

      order_info = (
        order.order["name"].data,
        order.order["information"].data,
        order.order["mission"].data,
        order.order["vision"].data,
        order.order["abbrevation"].data,
        order.order["foundation_date"].data,
        order.order["type"].data,
        order_key
      )
      update_contactinfo_with_id(_order["contact_id"], order.contact.data)
      update_order(order_info)

      return redirect( url_for("order_details_page", order_key = order_key) )

    order.order["name"].data             = _order["name"]
    order.order["information"].data      = _order["information"]
    order.order["mission"].data          = _order["mission"]
    order.order["vision"].data           = _order["vision"]
    order.order["abbrevation"].data      = _order["abbrevation"]
    order.order["foundation_date"].data  = _order["foundation_date"]
    order.order["type"].data             = _order["type"] if _order["type"] is not None else -1
    order.contact["phoneNumber"].data      = _contact["phonenumber"]
    order.contact["email"].data            = _contact["email"]
    order.contact["fax"].data              = _contact["fax"]
    order.contact["homePhone"].data        = _contact["homephone"]
    order.contact["workmail"].data         = _contact["workmail"]
    
    return render_template(
      "/orders/update.html",
      form = order
    )

def order_details_page(order_key):

  if session and session["logged_in"] == False:
    return redirect(url_for('signin_page'))
  elif session['membershiptype'] != 'Boss':
    return redirect(url_for("access_denied_page"))
  else:
    order = get_order(order_key)
    contact = get_contact_of_order( order['contact_id'] )
    founder = select_a_user_and_info( order['user_id'])
    if founder:
      founder = founder[0]
    if(order is None):
      abort(404)
    return render_template(
      "/orders/details.html",
      order = order,
      contact = contact,
      founder = founder
    )
