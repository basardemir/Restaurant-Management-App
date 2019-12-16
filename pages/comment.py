from flask import Flask, render_template, request, redirect, url_for

from models.comment import *

from .forms.comment_form import CommentForm

def comments_page():
  comments = get_all_comments()
  return render_template("/comments/index.html", comments = comments)

def comment_add_page():
  
  comment = CommentForm()
  if comment.validate_on_submit():
    
    user_key    = -1
    
    comment_info = (
      comment.comment["name"].data,
      comment.comment["information"].data,
      comment.comment["mission"].data,
      comment.comment["vision"].data,
      comment.comment["abbrevation"].data,
      comment.comment["foundation_date"].data,
      comment.comment["type"].data

    )

    comment_key = add_comment(comment_info)
  
  return render_template(
    "/comments/create.html",
    form = comment
  )

def comment_delete_page(comment_key):
  if request.method == "POST":
    delete_comment(comment_key)
    return redirect(url_for("comments_page"))
  return render_template("/comments/delete.html")

def comment_update_page(comment_key):
  _comment = get_comment(comment_key)
  if(_comment is None):
    abort(404)
  comment = CommentForm()

  if comment.validate_on_submit():
    comment_info = (
      comment.comment["name"].data,
      comment.comment["information"].data,
      comment.comment["mission"].data,
      comment.comment["vision"].data,
      comment.comment["abbrevation"].data,
      comment.comment["foundation_date"].data,
      comment.comment["type"].data,
      comment_key
    )
    update_comment(comment_info)

    return redirect( url_for("comment_details_page", comment_key = comment_key) )

  comment.comment["name"].data             = _comment["name"]
  comment.comment["information"].data      = _comment["information"]
  comment.comment["mission"].data          = _comment["mission"]
  comment.comment["vision"].data           = _comment["vision"]
  comment.comment["abbrevation"].data      = _comment["abbrevation"]
  comment.comment["foundation_date"].data  = _comment["foundation_date"]
  comment.comment["type"].data             = _comment["type"] if _comment["type"] is not None else -1

  return render_template(
    "/comments/update.html",
    form = comment
  )

def comment_details_page(comment_key):
  comment = get_comment(comment_key)
  if(comment is None):
    abort(404)
  return render_template(
    "/comments/details.html",
    comment = comment
  )
