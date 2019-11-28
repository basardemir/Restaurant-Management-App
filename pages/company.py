from flask import Flask, render_template, request, redirect, url_for

from models.company import *

from .forms.company_form import CompanyForm


def companies_page():
  companies = get_all_companies()
  return render_template("/companies/index.html", companies = companies)

def company_add_page():
  
  company = CompanyForm()
  if company.validate_on_submit():
    
    user_key    = -1
    
    company_info = (
      company.company["name"].data,
      company.company["information"].data,
      company.company["mission"].data,
      company.company["vision"].data,
      company.company["abbrevation"].data,
      company.company["foundation_date"].data,
      company.company["type"].data

    )

    company_key = add_company(company_info)
    return redirect(url_for("company_details_page", company_key = company_key))
  
  return render_template(
    "/companies/create.html",
    form = company
  )

def company_delete_page(company_key):
  if request.method == "POST":
    delete_company(company_key)
    return redirect(url_for("companies_page"))
  return render_template("/companies/delete.html")

def company_update_page(company_key):
  _company = get_company(company_key)
  if(_company is None):
    abort(404)
  company = CompanyForm()

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
    update_company(company_info)

    return redirect( url_for("company_details_page", company_key = company_key) )

  company.company["name"].data             = _company["name"]
  company.company["information"].data      = _company["information"]
  company.company["mission"].data          = _company["mission"]
  company.company["vision"].data           = _company["vision"]
  company.company["abbrevation"].data      = _company["abbrevation"]
  company.company["foundation_date"].data  = _company["foundation_date"]
  company.company["type"].data             = _company["type"] if _company["type"] is not None else -1

  return render_template(
    "/companies/update.html",
    form = company
  )

def company_details_page(company_key):
  company = get_company(company_key)
  if(company is None):
    abort(404)
  return render_template(
    "/companies/details.html",
    company = company
  )
