from flask import Flask, render_template, request, redirect, url_for, session, abort

from models.company import *
from models.users import insert_contactinfo, update_contactinfo_with_id, select_a_user_and_info

from .forms.company_form import CompanyForm
import datetime

def companies_page():
  if session and session["logged_in"] == False:
    return redirect(url_for('signin_page'))
  elif select_a_user_and_info(session['userid'])[0]['membershiptype'] != 'Boss':
    return redirect(url_for("access_denied_page"))
  else:
    companies = get_all_companies()
    return render_template("/companies/index.html", companies = companies)

def company_add_page():
  if session and session["logged_in"] == False:
    return redirect(url_for('signin_page'))
  elif select_a_user_and_info(session['userid'])[0]['membershiptype'] != 'Boss':
    return redirect(url_for("access_denied_page"))
  else:
    company = CompanyForm()
    if company.validate_on_submit():
      user_id     = session['userid']
      contact_id  = insert_contactinfo(company.contact.data, None)

      company_info = (
        company.company["name"].data,
        company.company["information"].data,
        company.company["mission"].data,
        company.company["vision"].data,
        company.company["abbrevation"].data,
        company.company["foundation_date"].data,
        company.company["type"].data,
        user_id,
        contact_id
      )

      company_key = add_company(company_info)
      return redirect(url_for("company_details_page", company_key = company_key))

    return render_template(
      "/companies/create.html",
      form = company
    )

def company_delete_page(company_key):
  if session and session["logged_in"] == False:
    return redirect(url_for('signin_page'))
  elif select_a_user_and_info(session['userid'])[0]['membershiptype'] != 'Boss':
    return redirect(url_for("access_denied_page"))
  else:
    if request.method == "POST":
      delete_company(company_key)
      return redirect(url_for("companies_page"))
    return render_template("/companies/delete.html")

def company_update_page(company_key):
  if session and session["logged_in"] == False:
    return redirect(url_for('signin_page'))
  elif select_a_user_and_info(session['userid'])[0]['membershiptype'] != 'Boss':
    return redirect(url_for("access_denied_page"))
  else:
    _company = get_company(company_key)
    
    if(_company is None):
      return redirect(url_for("not_found_page"))
    
    _contact  = get_contact_of_company(_company['contact_id'])
    company   = CompanyForm()

    if company.validate_on_submit():

      company_info = (
        company.company["name"].data,
        company.company["information"].data,
        company.company["mission"].data,
        company.company["vision"].data,
        company.company["abbrevation"].data,
        company.company["foundation_date"].data,
        company.company["type"].data,
        company_key
      )
      print(company.contact.data)
      update_contactinfo_with_id(_company["contact_id"], company.contact.data)
      update_company(company_info)

      return redirect( url_for("company_details_page", company_key = company_key) )

    company.company["name"].data             = _company["name"]
    company.company["information"].data      = _company["information"]
    company.company["mission"].data          = _company["mission"]
    company.company["vision"].data           = _company["vision"]
    company.company["abbrevation"].data      = _company["abbrevation"]
    company.company["foundation_date"].data  = _company["foundation_date"]
    company.company["type"].data             = _company["type"] if _company["type"] is not None else -1
    company.contact["phoneNumber"].data      = _contact["phonenumber"]
    company.contact["email"].data            = _contact["email"]
    company.contact["fax"].data              = _contact["fax"]
    company.contact["homePhone"].data        = _contact["homephone"]
    company.contact["workmail"].data         = _contact["workmail"]
    
    return render_template(
      "/companies/update.html",
      form = company
    )

def company_details_page(company_key):
  if session and session["logged_in"] == False:
    return redirect(url_for('signin_page'))
  elif select_a_user_and_info(session['userid'])[0]['membershiptype'] != 'Boss':
    return redirect(url_for("access_denied_page"))
  else:
    company = get_company(company_key)
    contact = get_contact_of_company( company['contact_id'] )
    founder = select_a_user_and_info( company['user_id'])

    if(company is None):
      abort(404)
    return render_template(
      "/companies/details.html",
      company = company,
      contact = contact,
      founder = founder
    )
