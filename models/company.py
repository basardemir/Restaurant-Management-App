import os
DB_URL = os.getenv("DATABASE_URL")

import psycopg2 as dbapi2

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

def get_id_and_name_of_companies():
  companies = []
  with dbapi2.connect(DB_URL) as connection:
    with connection.cursor() as cursor:
      query = "select company_id, name from company order by company_id;"
      cursor.execute(query)
      companies = list(cursor.fetchall())
  return companies

def get_company_by_user(user_key):
  res = None
  with dbapi2.connect(DB_URL) as connection:
    with connection.cursor() as cursor:
      query = "select * from company where user_id = %s;"
      cursor.execute(query, (user_key, ))
      company = list( cursor.fetchone() )
      desc = list( cursor.description[i][0] for i in range(0, len(cursor.description)) )
      res = dict(zip(desc, company ))
  return res

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

def get_contact_of_company(contact_id):
  res = None
  with dbapi2.connect(DB_URL) as connection:
    with connection.cursor() as cursor:
      query = "select * from contactinfo where id = %s;"
      cursor.execute(query, (contact_id, ))
      contact = list( cursor.fetchone() )
      desc = list( cursor.description[i][0] for i in range(0, len(cursor.description)) )
      res = dict(zip(desc, contact ))
  return res

def search_company_by_columns(company_key):
  print("index page search")

def add_company(company):
  company_id = -1
  with dbapi2.connect(DB_URL) as connection:
    with connection.cursor() as cursor:
      query = "insert into company(name, information, mission, vision, abbrevation, foundation_date, type, user_id, contact_id) values(%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING company_id;"
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

def update_company_founder(company):
  with dbapi2.connect(DB_URL) as connection:
    with connection.cursor() as cursor:
      query = "update company set user_id = %s where company_id = %s;"
      cursor.execute(query, company)
      connection.commit()

def delete_company(company_key):
  with dbapi2.connect(DB_URL) as connection:
    with connection.cursor() as cursor:
      query = "delete from company where company_id = %s;"
      cursor.execute( query, (company_key,) )
      connection.commit()

