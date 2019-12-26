Developer Guide
===============

Database Design
---------------

In the database, information about the application and the user's of the application are stored. 
The Useraccount Table stores information about the account. Each user has a membership type, a username and password, a join and last entry date, and a security question answer. The passwords of the users are encrypted. Each user also has a person in the Person Table. Each person has a name and surname, a date of birth, education level, and a gender. Each person has contact information in the Contactinformation Table. The person's phone number, email, and several other fields are stored. Each contact info has a social media information in the Socialmedia table. Each social media row contains links to facebook, twitter, and several other links. Each person also has an image in the Photo Table, and each contact info has a location info in the Locations Table.


General Method is used in Company, Card and Order and Comment pages.

* If the method does not end with _key or _id, this means the data is type of tuple.
* Tuple format is starting the data collected from user, and _id or _key will be send at the end of the tuple.
* If the getting data from database, then return dictionary key which is named in called table and value related to the key.

Company Table is connected to a founder saved in Useraccount table and contact information. 

* After login as a boss, the founder key will be saved from session user_id information.
* In the create page of company, listing the forms about company details and contact information. After calling POST method if it pass the validations, contact information will be saved to database via imported creating contact code.

Card Table is connected to a company and a customer saved in Useraccount table.

* Login as a boss, enter customer username if the username exits and enter the card details if it is valid, then getting user_id by customer and adding with details of the card to tuple to create.

Order Table is connected to a restaurant and a customer.

* After the meals selected and amount is selected by user, the order is created. Then the returning order_id is to make many-to-many relationship between order and food.

Order_Food Table is conntected to Order table to make many-to-many relations between order and food, also this makes different values for amount of the food for selling by customer. Also, this means that order_id and food_id are primary key.

* Order_id and getting food_id and amount related to food_id, then adding process is called for every food. 

Comment is connected to a order and a customer to make a comment after delivered status is updated.

* While clicking the comment, order_id will be passed by GET method and user fill the comment details.
* In the POST method, get data of order_id as parameter, then add tuple to the database.

Code
----

The application was coded with Python using the Flask framework. Flask is a Python Framework designed to implement web applications. Other packages used were wtforms, colour, and passlib.



.. toctree::

   member1
   member2
   member3
   member4
