from flask import Flask, render_template, request, redirect, url_for

from models.company import *

from .forms.company_form import CompanyForm


def companies_page():
  companies = get_all_companies()
  return render_template("/companies/index.html", companies = companies)

def company_add_page():
  
  company = CompanyForm()
  if company.validate_on_submit():
    company_info = (
      company.data["name"],
      company.data["information"],
      company.data["mission"],
      company.data["vision"],
      company.data["abbrevation"],
      company.data["foundation_date"],
      company.data["type"]
    )
    
    company_key = add_company(company_info)
    return redirect(url_for("company_details_page", company_key = company_key))
  
  return render_template(
    "/companies/create.html",
    form = company
  )

def company_delete_page(company_key):
  delete_company(company_key)
  return render_template("/companies/delete.html")

def company_update_page(company_key):
  _company = get_company(company_key)
  company = CompanyForm()

  if company.validate_on_submit():
    company_info = (
      company.data["name"],
      company.data["information"],
      company.data["mission"],
      company.data["vision"],
      company.data["abbrevation"],
      company.data["foundation_date"],
      company.data["type"],
      company_key
    )
    update_company(company_info)
    return redirect( url_for("company_details_page", company_key = company_key) )
  
  company.name.data             = _company["name"]
  company.information.data      = _company["information"]
  company.mission.data          = _company["mission"]
  company.vision.data           = _company["vision"]
  company.abbrevation.data      = _company["abbrevation"]
  company.foundation_date.data  = _company["foundation_date"]
  company.type.data             = _company["type"] if _company["type"] is not None else -1
  print(_company["type"])
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
