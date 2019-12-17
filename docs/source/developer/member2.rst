Parts Implemented by Metehan Seyran
================================

Food Table
-------------

Food table stores the information about every meal added to the website. Table consist of 2 foregin and 5 non-foreign keys. Foreign keys reference from photo table, which holds photos of the items, and nutritional_value table, which holds nutritional value for that specific meal. 

Ingredient Table
---------------

Ingredient table stores information about every ingredient that has been added to the website. The table has 2 foreign keys and 5 non key columns. Foreign keys are referencing to photos, which holds the photo path, and nutritional_value, which holds nutritional values such as carbohydrates, calories, etc. for every ingredient.

Restaurant Table
-------------------

Restaurant table holds information about restaurant. It has 2 foreign keys and 5 non key columns. Foreign key references to company table, which holds companies. The second one references to table contactinfo, which holds contact information such as phone number, email, address, etc.. 

Nutritional_value Table
--------------------

Nutritional value table holds nutritional values for ingredients or meals, depends on who is referencing to. It has 1 primary key and 5 non key columns. 

Ingredient_for_food table
----------------------

Ingredient_for_food table holds ingredients for every meal and amount of each ingredient. It has 2 primary keys and 1 non key column which holds amount of ingredient. This table is used as an array, because each meal have different ingredients and to check whether we can supply a meal or not, we should check stock table whether we have enough ingrediets to prepare that meal. 

Stock table
-------------------

Stock table holds stock value for every restaurant. It has 2 primary keys and 2 non key columns which hold expire date for ingredients and how many of ingredients left in stock. This table is also used as an array. Since every restaurant needs a ingredient stock to keep its ingredients safe and close in case of a delivery. Every restaurant have different ingredients, so for every restaurant id, there will be different ingredients ids , expire dates and how many are left. 

Structure
-------------------

For every main table the code structure is almost similar. Every table does the same  operations (CRUD), that is why they are similar. There will be structure for ingredient table. 

Read operations
-------------------
Read Operation returns every ingredient in database. It presented in html by using tables. Code block for redirecting to meal page;

.. code-block:: python

        def show_ingredients():
            ing_table = show_all_ingredients()
            return render_template("/ingredients/read_ingd.html", ing_table = ing_table, userType = session['membershiptype'])

The Code Block for retrieving all ingredients from database;

.. code-block:: python
        def show_all_ingredients():
            with dbapi2.connect(DB_URL) as connection:
                with connection.cursor() as cursor:
                    statement = "select ingredient_id, path, ingredient_name, ingredient_type, unit_weight, ingredient_volume, temperature_for_stowing from (photo inner join ingredient on photo_id = id);"
                    cursor.execute(statement)
                    ingred_table = cursor.fetchall()
                    connection.commit()
                    return ingred_table

Add operations
-------------------
In add operation, wtforms library was used. The library consists of different fields for input and equivalent for <input> tag. The ingredient form consisted of these items;

.. code-block:: python

        class Ingredient_Form(FlaskForm):
            ingred_name = StringField("Name", validators=[DataRequired(message=msg), Length(min=3, max=50, message="Name lenght must be between 4-30!")], render_kw={'placeholder': "Ingredient Name (eg. Potato)",  "class" : "form-control"})
            ingred_type = StringField("Type", validators=[DataRequired(message=msg), ], render_kw={"placeholder":"Ingredient Type (eg. Vegetable)",  "class" : "form-control"})
            unit_weight = FloatField("Unit Weight", validators=[DataRequired(message=msg), NumberRange(min=0)], render_kw={'placeholder': "Unit Weight (g)",  "class" : "form-control"})
            volume = FloatField("Volume", validators=[DataRequired(message=msg), NumberRange(min=0)], render_kw={'placeholder': "Volume",  "class" : "form-control"})
            ideal_temp = FloatField("Ideal Temperature", validators=[NumberRange(min=-10, max=50), DataRequired(message=msg)], render_kw={'placeholder': "Ideal Temperature (in Celcius)",  "class" : "form-control"})

The view function to add an ingredient;

.. code-block:: python

        def add_ingredient_page():
            _form = Ingredient_Page()
            if request.method == "GET":
                return render_template("/ingredients/add_ingd.html", form = _form)
            else:
                print(request.form)
                photo_path = "./static/" + request.files["photo-photo"].filename
                data = {"ingredient_name" : request.form['ingredient-ingred_name'], "ingredient_type": request.form['ingredient-ingred_type'], "unit_weight": request.form['ingredient-unit_weight'], "volume": request.form['ingredient-volume'], "ideal_temp": request.form['ingredient-ideal_temp'], "protein": request.form['nutrition-protein'], "carbohydrates": request.form['nutrition-carbohydrates'], "fat": request.form["nutrition-fat"], "cholesterol": request.form['nutrition-cholesterol'], "calories": request.form['nutrition-calories'], "photo_path": photo_path, "rest_id": request.form['restaurant-restaurant'], 'stock': request.form['restaurant-stock'], 'expire_date': request.form['restaurant-expire_date']}
                add_ingredient(data)
                request.files["photo-photo"].save("./static/" + request.files["photo-photo"].filename)
                return redirect(url_for('show_ingredients'))

And the SQL statement for inserting ingredient;

.. code-block:: python

        def add_ingredient(data):
            with dbapi2.connect(DB_URL) as connection:
                with connection.cursor() as cursor:
                    statement_photo = "insert into photo (path) values (%(img_path)s) returning id;"

                    cursor.execute(statement_photo, {'img_path': data['photo_path']})

                    photo_id = cursor.fetchone()[0]
                    statement_nutr = "insert into nutritional_value (protein, fat, carbohydrates, cholesterol, calories) values (%(protein)s, %(fat)s, %(carbohydrates)s, %(cholesterol)s, %(calories)s) RETURNING nutritional_value_id;"
                    
                    cursor.execute(statement_nutr, {'protein': data['protein'], 'fat': data['fat'], 'carbohydrates': data['carbohydrates'], 'cholesterol': data['cholesterol'], 'calories': data['calories']})
                    nutrition_id = cursor.fetchone()[0]
                    
                    statement_ing = "insert into ingredient (nutrition_id, photo_id, ingredient_name, ingredient_type, unit_weight, ingredient_volume, temperature_for_stowing) values (%(nutrition_id)s, %(photo_id)s, %(ingredient_name)s, %(ingredient_type)s, %(unit_weight)s, %(ingredient_volume)s, %(temperature_for_stowing)s) returning ingredient_id;"
                    cursor.execute(statement_ing, {'nutrition_id': nutrition_id, "photo_id": photo_id, 'ingredient_name': data['ingredient_name'], 'ingredient_type': data['ingredient_type'], 'unit_weight': data['unit_weight'], "ingredient_volume": data['volume'], "temperature_for_stowing": data['ideal_temp']})
                    ingredient_id = cursor.fetchone()[0]
                    print(data['expire_date'])
                    statement_stock = "insert into stock (ingredient_id, restaurant_id, expire_date, stock_left) values (%(ing_id)s, %(rest_id)s, %(date)s, %(stock)s);"
                    cursor.execute(statement_stock, {'ing_id': ingredient_id, 'rest_id': data['rest_id'], 'stock': data['stock'], 'date': data['expire_date']})
                    connection.commit()

Update & Delete operations
-------------------
Update and Delete operations are used in different pages. For update, a similar page to add ingredient page has been used. For delete, a page where asks user if user wants to delete an item, is used. In delete operation, the cascade operation made explicitly.

Here are the codes for update and delete ingredient;
Update:

.. code-block:: python

        def update_ingred(new_props, ingred_id):
            with dbapi2.connect(DB_URL) as connection:
                with connection.cursor() as cursor:
                    print(new_props['ingredient-ingred_name'])
                    statement = "update ingredient set ingredient_name=%(ingred_name)s, ingredient_type=%(ingred_type)s, unit_weight=%(weight)s, ingredient_volume=%(volume)s, temperature_for_stowing=%(temp)s where ingredient_id = %(ingred_id)s;"
                    cursor.execute(statement, {'ingred_name': new_props['ingredient-ingred_name'], 'ingred_type':new_props['ingredient-ingred_type'], 'weight':new_props['ingredient-unit_weight'], 'volume':new_props['ingredient-volume'], 'temp':new_props['ingredient-ideal_temp'], 'ingred_id': ingred_id})
                    connection.commit()

Delete:

.. code-block:: python

        def delete_ingred(ingred_id):
            with dbapi2.connect(DB_URL) as connection:
                with connection.cursor() as cursor:
                    statement = "select photo_id, nutrition_id from ingredient where (ingredient_id = %(ingred_id)s);"
                    cursor.execute(statement, {'ingred_id': ingred_id})

                    photo_id, nutrition_id = cursor.fetchone()
                    
                    statement5 = "delete from stock where ingredient_id = %(id)s;"
                    cursor.execute(statement5, {'id': ingred_id})

                    statementt6 = "delete from ingredients_for_food where ingredient_id = %(id)s;"
                    cursor.execute(statementt6, {'id': ingred_id})

                    statement4 = "delete from ingredient where ingredient_id=%(id)s;"
                    cursor.execute(statement4, {'id': ingred_id})

                    statement2 = "delete from photo where id = %(photo_id)s;"
                    cursor.execute(statement2, {'photo_id': photo_id})

                    statement3 = "delete from nutritional_value where(nutritional_value_id = %(nutr_id)s);"
                    cursor.execute(statement3, {'nutr_id': nutrition_id})

                    connection.commit()
