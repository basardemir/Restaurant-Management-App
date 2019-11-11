
from flask import Flask, render_template

def companies_page():
  return render_template("/companies/index.html")

def company_add_page():
  return render_template("/companies/create.html")

def company_delete_page(company_key):
  return render_template("/companies/delete.html")

def company_update_page(company_key):
  return render_template("/companies/update.html")

def company_details_page(company_key):
  return render_template("/companies/details.html")