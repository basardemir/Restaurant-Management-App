import os
DB_URL = os.getenv("DATABASE_URL")

import psycopg2 as dbapi2

class Company:
  def __init__(self, name, information, mission, vision, abbrevation, foundation_date, type, user_id = None, contact_id = None):
    self.name             = name
    self.information      = information
    self.mission          = mission
    self.vision           = vision
    self.abbrevation      = abbrevation
    self.foundation_date  = foundation_date
    self.type             = type
    self.user_id          = user_id
    self.contact_id       = contact_id

def get_all_companies():
  companies = []
  with dbapi2.connect(DB_URL) as connection:
    with connection.cursor() as cursor:
      query = "select * from company"
      cursor.execute(query)
      desc = list( cursor.description[i][0] for i in range(0, len(cursor.description)) )
      for i in cursor:
        res = dict(zip(desc, list(i) ))
        companies.append( res )
  return companies

def get_company(company_key):
  res = None
  with dbapi2.connect(DB_URL) as connection:
    with connection.cursor() as cursor:
      query = "select * from company where company_id = %s;"
      cursor.execute(query, (company_key, ))
      company = list( cursor.fetchone() )
      desc = list( cursor.description[i][0] for i in range(0, len(cursor.description)) )
      res = dict(zip(desc, company ))
  return res

def search_company_by_columns(company_key):
  print("index page search")

def add_company(company):
  company_id = -1
  with dbapi2.connect(DB_URL) as connection:
    with connection.cursor() as cursor:
      query = "insert into company(name, information, mission, vision, abbrevation, foundation_date, type) values(%s, %s, %s, %s, %s, %s, %s) RETURNING company_id;"
      cursor.execute(query, company)
      connection.commit()
      company_id = cursor.fetchone()[0]
  return company_id

def update_company(company):
  with dbapi2.connect(DB_URL) as connection:
    with connection.cursor() as cursor:
      query = "update company set name = %s, information = %s, mission = %s, vision = %s, abbrevation = %s, foundation_date = %s, type = %s where company_id = %s;"
      cursor.execute(query, company)
      connection.commit()

def delete_company(company_key):
  with dbapi2.connect(DB_URL) as connection:
    with connection.cursor() as cursor:
      query = "delete from company where company_id = %s;"
      cursor.execute( query, (company_key,) )
      connection.commit()
