Parts Implemented by Mehmet Can Gün
================================


Code Structure
---------------

Models Folder
===============

Containing database connection codes for forms.
- company.py
- card.py
- order.py

Pages Folder
===============
Containing pages to be connected with views page.
- company.py
- card.py
- order.py

Forms Folder in Pages Folder
==============================
Containing wtfforms forms to be called in pages and used in views.
Also, forms contains validations.
- company_form.py
- card_form.py
- order_form.py
- comment_form.py

views.py
===============
Containing the pages for import to use in urls.

server.py
===============
Containing the url rules for company, card, comment and order pages.


COMPANY
---------------

Company class is connected to user class as a founder info and to contact info to keep companies information to the system.
- Primary Key: COMPANY_ID
- Non-relational Key: NAME, INFORMATION, MISSION, ABBREVATION, FOUNDATION_DATE, TYPE( Limited or Anonymous )
- Foreign Key(table_name): USER_ID(USERACCOUNT), CONTACT_ID(CONTACT_INFO)

DB Functions
===============

- get_all_companies()
  This method get all companies in **index page of company**
  .. code-block:: SQL Queries
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

- get_company(company_key)
  This method get company in **detail page of company**
  .. code-block:: SQL Queries
  def get_company(company_key):
    res = None
    with dbapi2.connect(DB_URL) as connection:
      with connection.cursor() as cursor:
        query = "select * from company where company_id = %s;"
        cursor.execute(query, (company_key, ))
        data = cursor.fetchone()
        if data:
          company = list( data )
          desc = list( cursor.description[i][0] for i in range(0, len(cursor.description)) )
          res = dict(zip(desc, company ))
    return res

- add_company(company)
  This method add company in **add page of company**
  .. code-block:: SQL Queries
  def add_company(company):
    company_id = -1
    with dbapi2.connect(DB_URL) as connection:
      with connection.cursor() as cursor:
        query = "insert into company(name, information, mission, vision, abbrevation, foundation_date, type, user_id, contact_id) values(%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING company_id;"
        cursor.execute(query, company)
        connection.commit()
        company_id = cursor.fetchone()[0]
    return company_id

- update_company(company)
  This method update company in **update page of company**
  .. code-block:: SQL Queries
  def update_company(company):
    with dbapi2.connect(DB_URL) as connection:
      with connection.cursor() as cursor:
        query = "update company set name = %s, information = %s, mission = %s, vision = %s, abbrevation = %s, foundation_date = %s, type = %s where company_id = %s;"
        cursor.execute(query, company)
        connection.commit()

- delete_company(company_key)
  This method delete company in **delete page of company**
  .. code-block:: SQL Queries
  def delete_company(company_key):
    with dbapi2.connect(DB_URL) as connection:
      with connection.cursor() as cursor:
        query = "delete from company where company_id = %s;"
        cursor.execute( query, (company_key,) )
        connection.commit()

other functions
- get_contact_of_company(contact_id)
- get_id_and_name_of_companies()
- get_company_by_user(user_key)
- update_company_founder(company)

Forms
===============

.. code-block:: Company Abstract Class
class Company(FlaskForm):
  name = StringField(
    "Name", 
    validators = [ DataRequired(message = msgRequired.format("name") )],
    render_kw = { "class" : "form-control" }
  )

  information = TextAreaField(
    "Information", 
    validators = [ DataRequired(message = msgRequired.format("Information")) ],
    render_kw = { "class" : "form-control" }
  )

  mission = TextAreaField(
    "Mission",
    validators = [ DataRequired(message = msgRequired.format("Mission")) ],
    render_kw = { "class" : "form-control" }
  )

  vision = TextAreaField(
    "Vision",
    validators = [ DataRequired(message = msgRequired.format("Vision")) ],
    render_kw = { "class" : "form-control" }
  )

  abbrevation = StringField(
    "Abbrevation",
    validators = [ DataRequired(message = msgRequired.format("Abbrevation")) ],
    render_kw = { "class" : "form-control" }
  )

  foundation_date = DateField(
    'Founded Date', 
    render_kw = { "class" : "form-control" }
  )

  type = SelectField(
    "Type", 
    choices = typeChoices, 
    validators = [ unselectedValid ],
    render_kw = { "class" : "form-control" }
  )

.. code-block:: CompanyForm Class instanced from Company and ContactInfo class
class CompanyForm(FlaskForm):
  company   = FormField(Company)
  contact   = FormField(ContactInfoForm)
  submit    = SubmitField( render_kw = { "class" : "btn btn-primary"}

- Founder( class ), FounderForm( instanced from Founder )

Pages
===============
Pages connected to forms, views and call database operations.

.. code-block:: Company Index Page
def companies_page():
  if session and session["logged_in"] == False:
    return redirect(url_for('signin_page'))
  elif session['membershiptype'] != 'Boss':
    return redirect(url_for("access_denied_page"))
  else:
    companies = get_all_companies()
    return render_template("/companies/index.html", companies = companies)

.. code-block:: Company Add Page
def company_add_page():
  if session and session["logged_in"] == False:
    return redirect(url_for('signin_page'))
  elif session['membershiptype'] != 'Boss':
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

.. code-block:: Company Delete Page
def company_delete_page(company_key):
  if session and session["logged_in"] == False:
    return redirect(url_for('signin_page'))
  elif session['membershiptype'] != 'Boss':
    return redirect(url_for("access_denied_page"))
  else:
    if request.method == "POST":
      delete_company(company_key)
      return redirect(url_for("companies_page"))
    return render_template("/companies/delete.html")

.. code-block:: Company Update Page
def company_update_page(company_key):
  if session and session["logged_in"] == False:
    return redirect(url_for('signin_page'))
  elif session['membershiptype'] != 'Boss':
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

.. code-block:: Company Details Page
def company_details_page(company_key):
  if session and session["logged_in"] == False:
    return redirect(url_for('signin_page'))
  else:
    company = get_company(company_key)
    contact = get_contact_of_company( company['contact_id'] )
    founder = select_a_user_and_info( company['user_id'])
    if founder:
      founder = founder[0]
    if(company is None):
      return redirect(url_for("not_found_page"))
    return render_template(
      "/companies/details.html",
      company = company,
      contact = contact,
      founder = founder
    )

Views
===============
.. code-block:: List Companies if compaies exists.
  {% if companies %}
  <table class="table table-light table-hover">
    <thead>
      <tr>
        <th>Name</th>
        <th>Information</th>
        <th>Mission</th>
        <th>Vision</th>
        <th>Abbrevation</th>
        <th>Founded Date</th>
        <th>Type</th>
        <th>Operations</th>
      </tr>
    </thead>
    <tbody>
      {% for i in companies %}
      <tr>
        <td>{{ i['name'] }}</td>
        <td>{{ i['information'] }}</td>
        <td>{{ i['mission'] }}</td>
        <td>{{ i['vision'] }}</td>
        <td>{{ i['abbrevation'] }}</td>
        <td>{{ i['foundation_date'] }}</td>
        <td>{{ i['type'] }}</td>
        <td>
          <a href="{{ url_for('company_details_page', company_key = i['company_id']) }}" class="btn btn-info">Details </a>
          <a href="{{ url_for('company_update_page', company_key = i['company_id']) }}" class="btn btn-warning">Update</a>
          <a href="{{ url_for('company_delete_page', company_key = i['company_id']) }}" class="btn btn-danger">Delete</a>
          {% if not i['user_id'] %}
          <a href="{{ url_for('company_setfounder_page', company_key = i['company_id']) }}" class="btn btn-warning">Set Founder</a>
          {% endif%}
        </td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
  {% endif %}

.. code-block:: Add company
  <form method="post" action="{{ request.path }}" >
    {{ form.csrf_token }}
    
    {% for field, msg in form.errors.items() %}
      {% for i in msg: %}
        <div class="alert alert-warning" role="alert">
          <strong>{{ msg[i][0] }}</strong>
        </div>
      {% endfor %}
    {% endfor %}
    <h1 class="display-4">Create <small class="text-muted font-italic">company</small></h1>
    <hr>
    {{ form.company( class_ = "mt-5 table table-hover") }}
    <h1 class="display-4">Complete <small class="text-muted font-italic">contact</small></h1>
    <hr>  
    {{ form.contact( class_ = "mt-5 table table-hover") }}
    <p class="text-right">If you cannot find your location, you can create by using link below</p>
    <a href="{{ url_for('location_page') }}" class="float-right btn btn-dark">Add Location</a>
    <div class="text-center">
      {{ form.submit }}
      <a href="{{ url_for('companies_page') }}" class="btn btn-secondary">Cancel</a>
    </div>
  </form>

.. code-block:: Update company

  <form method="post" action="{{ request.path }}" >
    {{ form.csrf_token }}
    
    {% for field, msg in form.errors.items() %}
      {% for i in msg: %}
        <div class="alert alert-warning" role="alert">
          <strong>{{ msg[i][0] }}</strong>
        </div>
      {% endfor %}
    {% endfor %}
    <h1 class="display-4">Update <small class="text-muted font-italic">company</small></h1>
    <hr>
    {{ form.company( class_ = "mt-5 table table-hover") }}
    <h1 class="display-4">Update <small class="text-muted font-italic">contact</small></h1>
    <hr>  
    {{ form.contact( class_ = "mt-5 table table-hover") }}
    <div class="text-center">
      {{ form.submit }}
      <a href="{{ url_for('companies_page') }}" class="btn btn-secondary">Cancel</a>
    </div>
  </form>

.. code-block:: Delete company
  <form action="{{ request.path }}" method="POST">
    <h3>Are you sure to delete your company?</h3>
    <button type="submit" class="btn btn-primary">Submit</button>
    <a href="{{ url_for('companies_page') }}" class="btn btn-secondary">Cancel</a>
  </form>

.. code-block:: Details about company
{% if company %}

<div class="container">
  <div class="row">
    <div class="col-12 row">
      <div class="col-6">
        <h1 class="display-4">Company </h1>
        <hr >
        <ul>
          <li>Name: {{ company["name"] }}</li>
          <li>Information: {{ company["information"] }}</li>
          <li>Mission: {{ company["mission"] }}</li>
          <li>Vision: {{ company["vision"] }}</li>
          <li>Abbrevation: {{ company["abbrevation"] }}</li>
          <li>Foundation Date: {{ company["foundation_date"] }}</li>
          <li>Company Type: {{ company["type"] }}</li>
        </ul>
      </div>
      <div class="col-6">
        <h1 class="display-4 ">Founder</h1>
        <hr >
        {% if founder %}
          <div class="text-center">
            <img src="{{ founder['path'] }}" class="img-fluid round-circle" width="250" height="250">
          </div>
          <ul>
            <li>Founder: {{ founder['name'] }} {{ founder['surname']  }}  </li>
            <li>Gender: {{ founder['gender'] }}</li>
            <li>Birthday: {{ founder['birthday'] }}</li>
            <li>Education Level: {{ founder['educationlevel'] }}</li>
          </ul>
        {% else %}
          <p>This company has no founder yet.</p>
        {% endif %}
      </div>
    </div>
  </div>
    <h1 class="display-4 ">Contact to Company</h1>
    <hr >
    <ul>
      <li>Phone Number: {{ contact['phonenumber '] }}</li>
      <li>Email: {{ contact['email'] }}</li>
      <li>Fax: {{ contact['fax'] }}</li>
      <li>2nd Phone Number: {{ contact['homephone'] }}</li>
      <li>Work Mail: {{ contact['workmail'] }}</li>
    </ul>
</div>

{% endif %}

CARD
---------------

Card class is connected to user class with respect to company and to connect to company for specialize card for the company.
- Primary Key: CARD_ID 
- Non-relational Key: POINTS, CARD_NUMBER( UNIQUE ), IS_ACTIVE, COLOR, ACTIVATION_DATE( now ), EXPIRE_DATE( default = added 1 year from now )
- Foreign Key(table_name): USER_ID(USERACCOUNT), COMPANY_ID(COMPANY)

DB Functions
===============

- check_card_number(card_number)
- get_all_cards()
- get_card(card_key)
- get_card_by_user(user_key)
- add_card(card)
- update_card(card)
- delete_card(card_key)

Forms
===============

- Card( class ), CardForm( instanced from Card )



ORDER
---------------

Order class is connected to restaurant for meals and user account for who ordered the meals.
- Primary Key: ORDER_ID 
- Non-relational Key: PRICE( total price ), NOTE, TYPE( CASH OR CREDIT CARD ), RATE, CREATED_AT( now ), END_AT, is_delivered( 0 means not delievered )
- Foreign Key(table_name): RESTAURANT_ID(RESTAURANT), USER_ID(USERACCOUNT)

DB Functions
===============

- get_all_orders()
- get_order(key, type)
- get_detailed_order_food(key, type)
- get_order_details(order_key)
- add_order(order)
- update_order(order)
- update_order_delivered(order_id)
- update_stock_by_order_key(order_id):
- delete_order(order_key)

Forms
===============

- Order( class ), OrderForm( instanced from Order )


ORDER_FOOD
---------------

Order food class is connected to restaurant for meals and user account for who ordered the meals.
- Primary Key: ORDER_ID, FOOD_ID
- Non-relational Key: AMOUNT( ordered food amount )
- Foreign Key(table_name): FOOD_ID(FOOD), ORDER_ID(ORDERS)

DB Functions
===============
- connect_order_and_food(orderfood)


COMMENT
---------------

Comment class is connected to delivered order and user account who comment
- Primary Key: COMMENT_ID 
- Non-relational Key: TITLE, DESCRIPTION, CREATED_AT( now ), SPEED ( 0=slow : 1=fast ), TASTE( 0=tasteful : 1=not tasteful )
- Foreign Key(table_name): ORDER_ID(ORDERS), USER_ID(USERACCOUNT)

Functions
===============

- make_comment_to_order(comment)
- get_order_related_comments(key)


Forms
===============

- Comment( class ), CommentForm( instanced from Comment )
