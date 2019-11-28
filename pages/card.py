from flask import Flask, render_template, request, redirect, url_for

from models.card import *

from .forms.card_form import CardForm


def cards_page():
  cards = get_all_cards()
  return render_template("/cards/index.html", cards = cards)

def card_add_page():
  
  card = CardForm()
  if card.validate_on_submit():
    
    user_key    = -1

    card_info = (
      card.card["points"].data,
      card.card["card_number"].data,
      card.card["is_active"].data,
      str(card.card["color"].data),
      card.card["activation_date"].data,
      card.card["expire_date"].data
    )

    card_key = add_card(card_info)
    return redirect(url_for("card_details_page", card_key = card_key))
  
  return render_template(
    "/cards/create.html",
    form = card
  )

def card_delete_page(card_key):
  if request.method == "POST":
    delete_card(card_key)
    return redirect(url_for("cards_page"))
  return render_template("/cards/delete.html")

def card_update_page(card_key):
  _card = get_card(card_key)
  if(_card is None):
    abort(404)
  card = CardForm()

  if card.validate_on_submit():
    card_info = (
      card.card["points"].data,
      card.card["card_number"].data,
      card.card["is_active"].data,
      card.card["color"].data,
      card.card["activation_date"].data,
      card.card["expire_date"].data,
      card_key
    )
    update_card(card_info)

    return redirect( url_for("card_details_page", card_key = card_key) )
  
  card.card["points"].data           = _card["points"]
  card.card["card_number"].data      = _card["card_number"]
  card.card["is_active"].data        = _card["is_active"]
  card.card["color"].data            = _card["color"]
  card.card["activation_date"].data  = _card["activation_date"]
  card.card["expire_date"].data      = _card["expire_date"]

  return render_template(
    "/cards/update.html",
    form = card
  )

def card_details_page(card_key):
  card = get_card(card_key)
  if(card is None):
    abort(404)
  return render_template(
    "/cards/details.html",
    card = card
  )
