Parts Implemented by Uğur Demir
********************************
Location
==========

Location table was initially implemented as table to hold location information of both users on consumer level 
and branches of bussinesses. It consists of 6 tables with 3 main tables and 3 side tables. These tables are highly connected
to each other with a single table connecting the entire block to the rest of the system. Apart from their non-key columns
main tables have foreign keys refrencing each other. One of the foreign keys of Location table references the main table Province
and one of the Province's foreign keys reference the other main table Country. The start of the development the system was planned as 
usable from different countries. Initialy location was suppose to be a side table however in order to provide everyone with three main
tables we were forced to expand upon it leaving to this not so efficient way of generation location information of users. 
Entries to Provinces and Countries tables cannot be done by the normal users they have to be done by the admins. Normal users can generate
locations using the provinces and countries already created and additionally entering their address details. In an ideal world, since
the amount of countries and provinces withing them would not be changing too much, having these two tables filled with static information
from a reliable and detailed enough source would have sufficed. 

Structure
=========
Each main table has it's own CRUD pages. Inputs are controlled by flask-WTForms.
.. figure:: file_order.png
        :scale: 50 %
        :alt: html files per table
        After the delete operation the user is redirected to the main 
        index.html so there is no delete.html.

The database operations are done in an another file called the {table_name}_model.py. Necessary queries are defined
and executed using the functions within the model files. 

Database operations
=============
The returning values from a query had to be formatted in most cases before being sent to html. I used two main methods format incoming data
from the tables.

    .. code-block:: python

        def get_results(cursor):
            desc = cursor.description
            column_names = [col[0] for col in desc]
            data = [dict(zip(column_names,row)) for row in cursor.fetchall()] #array of dict
            #data[0].values() values of the first row
            res = []
            for i in data:
                res.append(i.values())
            cursor.close()
            return (res) #2d array 

Return value of get_results(cursor) is a 2d array which can be directly sent to html.

    .. code-block:: python

            desc = list(cursor.description[i][0] for i in range(0 ,len(cursor.description)))
            table = list(cursor.fetchone())
            result = dict(zip(desc, table))
            return result

In this one the returning result is a dictionary with table's column names as key values.

Unfinished / Problematic Features
==============
* Only the create location page was suppose to be accessable by the users, however the lack of authentcation allows anyone with the url can access the main pages of these tables and
do alterations. 
* While creating a location absance of javascript to hide option according to selected country allows users to combine a country with any of the provinces
. Plan was to filter the selectField options with java script once a country was selected but I was not able to built this feature. 
* Updating operation on locations doesn't work.