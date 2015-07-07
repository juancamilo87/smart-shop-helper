# **SMART SHOPPING HELPER: BACK END SYSTEM**
A crowd-sourced project, Smart Shopping Helper is here to give you the cheapest prices for items at the nearest locations to you. The backend system is the core part of the project which includes the database with the following methods:

## DATABASE

### *GET*
- get_category(category_id)
- get_category_by_name(category_name)
- get_categories()
- get_item(item_id)
- get_items(category_id)
- get_prices(item_id)
- get_stores()
- get_store(store_id)
- get_schedule(schedule_id)
- get_schedule_from_details(monday_id, tuesday_id, wednesday_id, thursday_id, friday_id, saturday_id, sunday_id)
- get_time(time_id)
- get_time_from_details(open, close)

### *CREATE*
- create_category(name, description)
- create_item(category_id, name, description)
- create_store(name, address, latitude, longitude, schedule_id)
- create_schedule(monday_id, tuesday_id, wednesday_id, thursday_id, friday_id, saturday_id, sunday_id)
- create_time(open, close)

### *UPDATE*
- update_price(value, item_id, store_id)
- update_store_schedule(store_id, schedule_id)

### *DELETE*
- delete_item(item_id)
- delete_store(store_id)

#### All the above methods work on the *defined database tables*
category, items, prices, stores, schedules, times

### **DEPENDENCIES** (External Libraries)
The external library we used was Sqlite3.

### **DATABASE INTERFACE**
The database is accessed through the database.py file in the folder shop inside the smart_shop_helper package. The methods defined in the ShopDatabase class permit to get data from the database, create data and add into the database and also update/modify the database (update limited to Table prices). The database API receives a set of keyword arguments.  The data returned by the database methods are usually encapsulated in python dictionaries.  Methods are described in the source code.

### **SETUP**
- Have sqlite3.exe on the root of the project (the file is on the repository).
- Install python on the PC.

### **Populate and setup the database**
- Use the method create_all_tables() from database.py
Or
- Use the method load_init_values() from database.py if you want the DB full
Or
- Create the DB using sqlite3
- Use the dump file db/shop_data_dump.sql to create the database.

#### *The database file is already populated, so this is not necessary to run*

### **Run tests**
Use the files inside the folder test. There is a file for each table:

- database_api_tests_category.py
- database_api_tests_item.py
- database_api_tests_price.py
- database_api_tests_schedule.py
- database_api_tests_store.py
- database_api_tests_time.py

## **RESOURCES**

### **DESCRIPTION**

Resource | Path | Methods
-------- | ---- | -------
Item | /shop/api/items/ *item_id*/ | GET, PUT, DELETE
ItemList | /shop/api/items/ | GET, POST
ItemPriceList | /shop/api/items/ *item_id*/pricelist/ | GET
Store | /shop/api/stores/ *store_id*/ | GET, PUT, DELETE
StoreList | /shop/api/stores/ | GET, POST

- *item_id must be in the format itm-#*  
- *store_id must be in the format str-#*  

### **SETUP**

1. Install **geopy** on the computer which will be the server. (Command: pip install geopy). *Starting from Python versions 2.7.9 and 3.4.0, pip is already included in the regular install. If the python version is below 2.7.9, Download get-pip.py, being careful to save it as a .py file rather than .txt. Then, run it from the command prompt. Run python get-pip.py after that.*

2. Run the following command from the root folder of the project *python -m shop.resources*

**Now you should be able to access the resources methods using http://localhost:5000 + path**

## **CLIENT**

### **Android**

#### STEPS:
1. Open the port 5000 on the computer that is going to be the server.

2. Start the server on a computer connected to the same network as the Android device you are going to use.

3. Download the .apk file from Client/Android Client/Installer on the android device and run it.

4. At the beginning, you have to provide the server ip to the Android app. 
*If the server ip changes, the app data has to be cleared from the Android application so that it asks for it again.*

*Currently the app does not delete items from the cart, so to clear it, the app data has to be cleared.*

### **Web**

1. Start the server on a computer.
2. The files jquery.js, smh.js and default.html have to be on the same folder.
3. Open the file default.html on the same computer as the server. *If this is not possible, then change the ip from localhost to the appropiate ip in the code from the smh.js*
