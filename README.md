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

#Setting Up and running the application.
##STEPS:
1. Install **geopy** on the computer which will be the server. (Command: pip install geopy). *Starting from Python versions 2.7.9 and 3.4.0, pip is already included in the regular install. If the python version is below 2.7.9, Download get-pip.py, being careful to save it as a .py file rather than .txt. Then, run it from the command prompt. Run python get-pip.py after that.*

2. Download the .apk file from Client/Android Client/Installer on the android device and run it. The computer running the server and the phone must be on the same network. At the beginning, you have to provide the server ip to give access to the app. If the server ip changes, then app data has to be cleared from Android so that it asks for it again.

3. For some functions, like deleting an item or a store, there is a web interface implemented in html. The jquery.js and smh.js should be in the same folder as the .html file. (All the interfaces are still not working well. Only the items could be fetched for now. On certain request types, we get the following error - No 'Access-Control-Allow-Origin' header is present on the requested resource).
