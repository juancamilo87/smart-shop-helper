# **SMART SHOPPING HELPER: BACK END SYSTEM**
A crowd-sourced project, Smart Shopping Helper is here to give you the cheapest prices for items at the nearest locations to you. The Back end system is the core part of the project which includes the database with the following methods:

### *GET*
- get_categories()
- get_items(category_id)
- get_prices(item_id)
- get_store(store_id)
- get_schedule(schedule_id)
- get_time(time_id)

### *CREATE*
- create_category(name, description)
- create_item(category_id, name, description)
- create_store(name, address, latitude, longitude, schedule_id)
- create_schedule(monday_id, tuesday_id, wednesday_id, thursday_id, friday_id, saturday_id, sunday_id)
- create_time(open, close)

### *UPDATE*
update_price(value, item_id, store_id)

### All the above methods work on the *defined database tables*
category, items, prices, stores, schedules, times

## **DEPENDENCIES** (External Libraries)
The external library we used was Sqlite3.

## **DATABASE INTERFACE**
The database is accessed through the database.py file in the folder shop inside the smart_shop_helper package. The methods defined in the ShopDatabase class permit to get data from the database, create data and add into the database and also update/modify the database (update limited to Table prices). The database API receives a set of keyword arguments.  The data returned by the database methods are usually encapsulated in python dictionaries.  Methods are described in the source code.

## **SETUP**
- Have sqlite3.exe on the root of the project (the file is on the repository).
- Install python on the PC.

## **Populate and setup the database**
- Use the method create_all_tables() from database.py
Or
- Use the method load_init_values() from database.py if you want the DB full
Or
- Create the DB using sqlite3
- Use the dump file db/shop_data_dump.sql to create the database.

## **Run tests**
Use the files inside the folder test. There is a file for each table:

- database_api_tests_category.py
- database_api_tests_item.py
- database_api_tests_price.py
- database_api_tests_schedule.py
- database_api_tests_store.py
- database_api_tests_time.py


