Parts Implemented by Mehmet Can Gün
************************************

CODE STRUCTURE
---------------

We basically implement the MVC pattern, which is Modal, View, Controller approach. This method provides us to use our methods by calling in a structure.

Models Folder
===============

Containing database connection codes for forms.

* company.py
* card.py
* order.py

Pages Folder
===============

Containing pages to be connected with views page.

* company.py
* card.py
* order.py

Forms Folder in Pages Folder
==============================

Containing wtfforms forms to be called in pages and used in views.

Also, forms contains validations.

* company_form.py
* card_form.py
* order_form.py
* comment_form.py


views.py
===============

Containing the pages for import to use in urls.

.. literalinclude:: ../../../views.py
  :lines: 4,8,13
  :linenos:
  :language: python
  :caption: views.py


util.py
===============

| This file is used only for adding 'list' into Flask urls in order to convert urls in spite of html markup.
| Basically, if you send list with link, then the url shows data seperated by comma.
| [util.py]_ ListConventer is implemented with BaseConverter 
| In the 4-5 lines of **server.py**, adding the list to flask map structure

.. literalinclude:: ../../../util.py
  :linenos:
  :language: python
  :caption: util.py

.. literalinclude:: ../../../server.py
  :lines: 6-12
  :linenos:
  :language: python
  :caption: server.py


COMPANY
---------------

Company class is connected to user class as a founder info and to contact info to keep companies information to the system.

* Primary Key: COMPANY_ID
* Non-relational Key
  
  * NAME
  * INFORMATION
  * MISSION 
  * ABBREVATION 
  * FOUNDATION_DATE  
  * TYPE( Limited or Anonymous )

* Foreign Key(table_name)

  * USER_ID(USERACCOUNT)
  * CONTACT_ID(CONTACT_INFO)

Database Functions
===================

.. literalinclude:: ../../../models/company.py
  :lines: 6-16
  :linenos:
  :caption: This method get all companies in **index page of company**
  :language: python

.. literalinclude:: ../../../models/company.py
  :lines: 40-51
  :linenos:
  :language: python
  :caption: This method get company in **detail page of company**

.. literalinclude:: ../../../models/company.py
  :lines: 66-74
  :linenos:
  :language: python
  :caption: This method add company in **add page of company**

.. literalinclude:: ../../../models/company.py
  :lines: 76-81
  :linenos:
  :language: python
  :caption: This method update company in **update page of company**

.. literalinclude:: ../../../models/company.py
  :lines: 90-95
  :linenos:
  :language: python
  :caption: This method delete company in **delete page of company**

Other functions
=================

.. literalinclude:: ../../../models/company.py
  :lines: 53-64
  :linenos:
  :language: python
  :caption: Getting **contact information** of company by **contact_id**

.. literalinclude:: ../../../models/company.py
  :lines: 90-95
  :linenos:
  :language: python
  :caption: Getting **id and name** of companies to show in card list as choices.

.. literalinclude:: ../../../models/company.py
  :lines: 27-38
  :linenos:
  :language: python
  :caption: Getting company by **user key**.

.. literalinclude:: ../../../models/company.py
  :lines: 90-95
  :linenos:
  :language: python
  :caption: **Update the founder** information of company.

Forms
===============

Company and Founder Form using in pages are made with wtfforms components.

.. literalinclude:: ../../../pages/forms/company_form.py
  :lines: 1-20, 76-81
  :linenos:
  :language: python
  :caption: import section of company_form.

.. literalinclude:: ../../../pages/forms/company_form.py
  :lines: 26-68
  :linenos:
  :language: python
  :caption: Company Abstract Class

.. literalinclude:: ../../../pages/forms/company_form.py
  :lines: 71-74
  :linenos:
  :language: python
  :caption: CompanyForm Class instanced from Company and ContactInfo class

.. literalinclude:: ../../../pages/forms/company_form.py
  :lines: 83-89
  :linenos:
  :language: python
  :caption: Founder( class )

.. literalinclude:: ../../../pages/forms/company_form.py
  :lines: 91-93
  :linenos:
  :language: python
  :caption: FounderForm( instanced from Founder )

Pages
===============
Pages connected to forms, views and call database operations.

.. literalinclude:: ../../../pages/company.py
  :lines: 9-16
  :linenos:
  :language: python
  :caption: Company Index Page

.. literalinclude:: ../../../pages/company.py
  :lines: 18-47
  :linenos:
  :language: python
  :caption: Company Add Page

.. literalinclude:: ../../../pages/company.py
  :lines: 49-58
  :linenos:
  :language: python
  :caption: Company Delete Page

.. literalinclude:: ../../../pages/company.py
  :lines: 60-107
  :linenos:
  :language: python
  :caption: Company Update Page

.. literalinclude:: ../../../pages/company.py
  :lines: 109-126
  :linenos:
  :language: python
  :caption: Company Details Page

.. literalinclude:: ../../../pages/company.py
  :lines: 128-149
  :linenos:
  :language: python
  :caption: Company Set Founder Page

Views
===============

.. literalinclude:: ../../../templates/companies/index.html
  :lines: 16-52
  :linenos:
  :language: html
  :caption: List Companies if companies exists.

.. literalinclude:: ../../../templates/companies/create.html
  :lines: 6-28
  :linenos:
  :language: html
  :caption: Adding Company after join as Boss.

.. literalinclude:: ../../../templates/companies/update.html
  :lines: 6-26
  :linenos:
  :language: html
  :caption: Update details about company.

.. literalinclude:: ../../../templates/companies/set_founder.html
  :lines: 6-24
  :linenos:
  :language: html
  :caption: Update details about boss of company.

.. literalinclude:: ../../../templates/companies/delete.html
  :lines: 6-11
  :linenos:
  :language: html
  :caption: Confirm the delete operation.

.. literalinclude:: ../../../templates/companies/details.html
  :lines: 4-52
  :linenos:
  :language: html
  :caption: Lists details about company information, boss information and contact information


CARD
---------------

| Card class is connected to user class with respect to company and to connect to company for specialize card for the company.

* Primary Key: CARD_ID 
* Non-relational Key:

  * POINTS
  * CARD_NUMBER( UNIQUE )
  * IS_ACTIVE
  * COLOR 
  * ACTIVATION_DATE( now ), 
  * EXPIRE_DATE( default = added 1 year from now )

* Foreign Key(table_name)
  
  * USER_ID(USERACCOUNT)
  * COMPANY_ID(COMPANY)

Database Functions
===================

.. literalinclude:: ../../../models/card.py
  :lines: 15-25
  :linenos:
  :caption: This method get all cards in **index page of card**
  :language: python

.. literalinclude:: ../../../models/card.py
  :lines: 27-38
  :linenos:
  :language: python
  :caption: This method get card in **detail page of card**

.. literalinclude:: ../../../models/card.py
  :lines: 53-61
  :linenos:
  :language: python
  :caption: This method add card in **add page of card**

.. literalinclude:: ../../../models/card.py
  :lines: 63-68
  :linenos:
  :language: python
  :caption: This method update card in **update page of card**

.. literalinclude:: ../../../models/card.py
  :lines: 70-75
  :linenos:
  :language: python
  :caption: This method delete card in **delete page of card**

Other functions
=================

.. literalinclude:: ../../../models/card.py
  :lines: 6-13
  :linenos:
  :language: python
  :caption: This method checks the card number does exist or not in cards.

.. literalinclude:: ../../../models/card.py
  :lines: 40-51
  :linenos:
  :language: python
  :caption: Getting card information by user_key in order to use in my_card page.


Forms
===============

CardForm is used in pages.

.. literalinclude:: ../../../pages/forms/card_form.py
  :lines: 1-37
  :linenos:
  :language: python
  :caption: import section of card_form

.. literalinclude:: ../../../pages/forms/card_form.py
  :lines: 39-72
  :linenos:
  :language: python
  :caption: Card class for Form

.. literalinclude:: ../../../pages/forms/card_form.py
  :lines: 74-81
  :linenos:
  :language: python
  :caption: CardForm includes Card class


Pages
===============
Pages connected to forms, views and call database operations.

.. literalinclude:: ../../../pages/card.py
  :lines: 23-30
  :linenos:
  :language: python
  :caption: Card Index Page

.. literalinclude:: ../../../pages/card.py
  :lines: 32-64
  :linenos:
  :language: python
  :caption: Card Add Page

.. literalinclude:: ../../../pages/card.py
  :lines: 66-75
  :linenos:
  :language: python
  :caption: Card Delete Page

.. literalinclude:: ../../../pages/card.py
  :lines: 77-116
  :linenos:
  :language: python
  :caption: Card Update Page

.. literalinclude:: ../../../pages/card.py
  :lines: 118-128
  :linenos:
  :language: python
  :caption: Card Details Page

.. literalinclude:: ../../../pages/card.py
  :lines: 130-140
  :linenos:
  :language: python
  :caption: My Card Page

Views
===============

.. literalinclude:: ../../../templates/cards/index.html
  :lines: 6-55
  :linenos:
  :language: html
  :caption: List Cards if cards exists.

.. literalinclude:: ../../../templates/cards/create.html
  :lines: 5-37
  :linenos:
  :language: html
  :caption: Adding Card after join as Boss and if a user is a customer.

.. literalinclude:: ../../../templates/cards/update.html
  :lines: 5-37
  :linenos:
  :language: html
  :caption: Update details about card.

.. literalinclude:: ../../../templates/cards/delete.html
  :lines: 4-12
  :linenos:
  :language: html
  :caption: Confirm the delete operation.

.. literalinclude:: ../../../templates/cards/details.html
  :lines: 4-37
  :linenos:
  :language: html
  :caption: Lists details about card and user information


ORDER
---------------

Order class is connected to restaurant for meals and user account for who ordered the meals.

* Primary Key: ORDER_ID 
* Non-relational Key

  * PRICE( total price )
  * NOTE
  * TYPE( CASH OR CREDIT CARD )
  * RATE 
  * CREATED_AT( now )
  * END_AT
  * is_delivered( 0 means not delievered )

* Foreign Key(table_name)
  
  * RESTAURANT_ID(RESTAURANT)
  * USER_ID(USERACCOUNT)

Database Functions
===================

.. literalinclude:: ../../../models/orders.py
  :lines: 8-18
  :linenos:
  :caption: This method get all orders in **index page of order**
  :language: python

.. literalinclude:: ../../../models/orders.py
  :lines: 20-36
  :linenos:
  :language: python
  :caption: This method get order in **detail page of order** by type such as restaurant, user or order key.

.. literalinclude:: ../../../models/orders.py
  :lines: 38-55
  :linenos:
  :language: python
  :caption: This method get order food details in **detail page of order** by type such as restaurant, user or order key.

.. literalinclude:: ../../../models/orders.py
  :lines: 57-68
  :linenos:
  :language: python
  :caption: This method get order details in **detail page of order**

.. literalinclude:: ../../../models/orders.py
  :lines: 70-80
  :linenos:
  :language: python
  :caption: This method get comments of the order in **detail page of order**

.. literalinclude:: ../../../models/orders.py
  :lines: 82-90
  :linenos:
  :language: python
  :caption: This method add order in **payment page of order**

.. literalinclude:: ../../../models/orders.py
  :lines: 106-111
  :linenos:
  :language: python
  :caption: This method update order in **update page of order**

.. literalinclude:: ../../../models/orders.py
  :lines: 130-135
  :linenos:
  :language: python
  :caption: This method delete order in **cancel page of order**


Other functions
=================

.. literalinclude:: ../../../models/orders.py
  :lines: 113-118
  :linenos:
  :language: python
  :caption: This method update **the delivered status** of the order.

.. literalinclude:: ../../../models/orders.py
  :lines: 120-129
  :linenos:
  :language: python
  :caption: This method calls if the order is delivered to customer, the stock update function from stock model to decrease the amount of foods.


Forms
===============

OrderForm is used in pages.

.. literalinclude:: ../../../pages/forms/order_form.py
  :lines: 1-14
  :linenos:
  :language: python
  :caption: import section of order_form

.. literalinclude:: ../../../pages/forms/order_form.py
  :lines: 16-50
  :linenos:
  :language: python
  :caption: Order class for Form

.. literalinclude:: ../../../pages/forms/order_form.py
  :lines: 51-53
  :linenos:
  :language: python
  :caption: OrderForm includes Order class


Pages
===============
Pages connected to forms, views and call database operations.

.. literalinclude:: ../../../pages/order.py
  :lines: 11-17
  :linenos:
  :language: python
  :caption: Order Index Page

.. literalinclude:: ../../../pages/order.py
  :lines: 19-68
  :linenos:
  :language: python
  :caption: Payment Page

.. literalinclude:: ../../../pages/order.py
  :lines: 70-77
  :linenos:
  :language: python
  :caption: Order Cancel Page

.. literalinclude:: ../../../pages/order.py
  :lines: 79-112
  :linenos:
  :language: python
  :caption: Order Update Page

.. literalinclude:: ../../../pages/order.py
  :lines: 114-130
  :linenos:
  :language: python
  :caption: Order Details Page

.. literalinclude:: ../../../pages/order.py
  :lines: 132-143
  :linenos:
  :language: python
  :caption: My Orders Page shows ordered meals and details about it.

.. literalinclude:: ../../../pages/order.py
  :lines: 132-143
  :linenos:
  :language: python
  :caption: if the method is POST, Order Delivered be called and update the delivered status as 1 and call the update stock function to decrease the stock size.

Views
===============

.. literalinclude:: ../../../templates/orders/index.html
  :lines: 5-43
  :linenos:
  :language: html
  :caption: List Orders if orders exists.

.. literalinclude:: ../../../templates/orders/payment.html
  :lines: 5-70
  :linenos:
  :language: html
  :caption: Get the list from meal page then put the values to views with javascript. Then, the customer sells the food by selecting the amount and the order is starting.

.. literalinclude:: ../../../templates/orders/edit.html
  :lines: 5-27
  :linenos:
  :language: html
  :caption: Update details about order.

.. literalinclude:: ../../../templates/orders/cancel.html
  :lines: 4-12
  :linenos:
  :language: html
  :caption: The customer can cancel if the date between starting date and end date is not over.

.. literalinclude:: ../../../templates/orders/details.html
  :lines: 4-75
  :linenos:
  :language: html
  :caption: Lists details about order

.. literalinclude:: ../../../templates/orders/myorders.html
  :lines: 4-54
  :linenos:
  :language: html
  :caption: Lists details about order by the users

ORDER_FOOD
---------------

Order food class is connected to restaurant for meals and user account for who ordered the meals.

* Primary Key: ORDER_ID, FOOD_ID
* Non-relational Key: AMOUNT( ordered food amount )
* Foreign Key(table_name)
  
  * FOOD_ID(FOOD)
  * ORDER_ID(ORDERS)

Database Functions
===================

.. literalinclude:: ../../../models/orders.py
  :lines: 92-97
  :linenos:
  :language: python
  :caption: This method connect food and order in one table with the amount of food.



COMMENT
---------------

Comment class is connected to delivered order and user account who comment.

* Primary Key: COMMENT_ID 
* Non-relational Key
  
  * TITLE
  * DESCRIPTION
  * CREATED_AT( now )
  * SPEED ( 0=slow : 1=fast )
  * TASTE( 0=tasteful : 1=not tasteful )

* Foreign Key(table_name) 
  
  * ORDER_ID(ORDERS)
  * USER_ID(USERACCOUNT)

Database Functions
===================

.. literalinclude:: ../../../models/orders.py
  :lines: 99-105
  :linenos:
  :language: python
  :caption: This method provides to comment the order.

.. literalinclude:: ../../../models/orders.py
  :lines: 70-80
  :linenos:
  :language: python
  :caption: This method get comments of the order in **detail page of order**


Forms
===============

CommentForm is used in pages.

.. literalinclude:: ../../../pages/forms/comment_form.py
  :lines: 1-7
  :linenos:
  :language: python
  :caption: import section of comment_form

.. literalinclude:: ../../../pages/forms/comment_form.py
  :lines: 9-34
  :linenos:
  :language: python
  :caption: Comment class for Form

.. literalinclude:: ../../../pages/forms/comment_form.py
  :lines: 37-39
  :linenos:
  :language: python
  :caption: CommentForm includes Comment class


Pages
===============
Pages connected to forms, views and call database operations.

.. literalinclude:: ../../../pages/order.py
  :lines: 145-172
  :linenos:
  :language: python
  :caption: Comment to Order

Views
===============

.. literalinclude:: ../../../templates/orders/comment.html
  :lines: 5-32
  :linenos:
  :language: html
  :caption: Creating a comment page.


.. [util.py] https://exploreflask.com/en/latest/views.html#custom-converters