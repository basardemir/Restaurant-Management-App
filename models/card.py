import os
import psycopg2 as dbapi2

DB_URL = os.getenv("DATABASE_URL")

def check_card_number(card_number):
  res = None
  with dbapi2.connect(DB_URL) as connection:
    with connection.cursor() as cursor:
      query = "select COUNT(*) from card where card_number = %s;"
      cursor.execute(query, (card_number, ))
      res = cursor.fetchone()[0]
  return res

def get_all_cards():
  cards = []
  with dbapi2.connect(DB_URL) as connection:
    with connection.cursor() as cursor:
      query = "select card_id, p.name as name, color , p.surname as surname, points, expire_date, card_number, com.name as company from card left outer join company as com on card.company_id = com.company_id left join useraccount as users on card.user_id = users.id inner join person as p on p.id = users.person"
      cursor.execute(query)
      desc = list( cursor.description[i][0] for i in range(0, len(cursor.description)) )
      for i in cursor:
        res = dict(zip(desc, list(i) ))
        cards.append( res )
  return cards

def get_card(card_key):
  res = None
  with dbapi2.connect(DB_URL) as connection:
    with connection.cursor() as cursor:
      query = "select CONCAT(p.name,' ',p.surname) as person_name, color, ph.path as path, p.birthDay, p.educationLevel, p.gender, card_number, points, is_active, activation_date, expire_date, card.company_id as company_id, c.name as company_name, c.information as company_information from card full join useraccount on card.user_id = useraccount.id full join company as c on c.company_id = card.company_id full join person as p on p.id = useraccount.person full join photo as ph on p.photo = ph.id where card_id = %s;"
      cursor.execute(query, (card_key, ))
      data = cursor.fetchone()
      if data:
        card = list( data )
        desc = list( cursor.description[i][0] for i in range(0, len(cursor.description)) )
        res = dict(zip(desc, card ))
  return res

def add_card(card):
  card_id = -1
  with dbapi2.connect(DB_URL) as connection:
    with connection.cursor() as cursor:
      query = "insert into card(points, card_number, is_active, color, expire_date, user_id, company_id) values(%s, %s, %s, %s, %s, %s, %s) RETURNING card_id;"
      cursor.execute(query, card)
      connection.commit()
      card_id = cursor.fetchone()[0]
  return card_id

def update_card(card):
  with dbapi2.connect(DB_URL) as connection:
    with connection.cursor() as cursor:
      query = "update card set points = %s, card_number = %s, is_active = %s, color = %s, expire_date = %s, user_id = %s, company_id=%s where card_id = %s;"
      cursor.execute(query, card)
      connection.commit()

def delete_card(card_key):
  with dbapi2.connect(DB_URL) as connection:
    with connection.cursor() as cursor:
      query = "delete from card where card_id = %s;"
      cursor.execute( query, (card_key,) )
      connection.commit()