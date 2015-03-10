

from datetime import datetime
import time, sqlite3, sys, re, os

DEFAULT_DB_PATH = 'db/shop.db'
DEFAULT_DATA_DUMP = "db/shop_data_dump.sql"

class ShopDatabase(object):
    '''
    API to access Forurm database. 
    '''
    

    def __init__(self, db_path=None):
        '''
        db_path is the address of the path with respect to the calling script.
        If db_path is None, DEFAULT_DB_PATH is used instead.
        '''
        super(ShopDatabase, self).__init__()
        if db_path is not None:
            self.db_path = db_path
        else:
            self.db_path = DEFAULT_DB_PATH
        

    #Setting up the database. Used for the tests.
    #SETUP, POPULATE and DELETE the database
    def clean(self):
        '''
        Purge the database removing old values.
        '''
        os.remove(self.db_path)

    def create_all_tables(self):
        '''
        Create all tables programmatically, without using an external sql.
        It prints error messages in console if any of the tables could not be
        created.
        '''
        self.create_categories_table()
        self.create_items_table()
        self.create_times_table()
        self.create_schedules_table()
        self.create_stores_table()
        self.create_prices_table()

    def load_init_values(self):
        '''
        Populate the database with initial values. It creates 
        ''' 
        self.create_all_tables()
        self.load_table_values_from_dump()

    def load_table_values_from_dump(self, dump=None):
        '''
        Populate programmatically the tables from a dump file.
        dump is the  path to the .sql dump file. If it is None,  
        DEFAULT_DATA_DUMP is used instead.
        '''
        con = sqlite3.connect(self.db_path)
        if dump is None:
            dump = DEFAULT_DATA_DUMP
        with open (dump) as f:
            sql = f.read()
            cur = con.cursor()
            cur.executescript(sql)  

    #MANAGING THE CONNECTIONS:
    def check_foreign_keys_status(self):
        '''
        Checks the status of foreign keys
        '''
        con = None
        try:
            #Connects (and creates if necessary) to the database. Gets a connection object
            con = sqlite3.connect(self.db_path)
            #Get the cursor object. It allows to execute SQL code and traverse the result set
            cur = con.cursor()   
            #Execute the pragma command
            cur.execute('PRAGMA foreign_keys')
            #We know we retrieve just one record: use fetchone()
            data = cur.fetchone()
             
            print "Foreign Keys status: %s" % data               
             
        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]
            sys.exit(1)
             
        finally:
            if con:
                con.close()
        return data

    def create_categories_table (self):
        '''
        Print an error message in the console if it could not be created. 
        creates categories table
        categories table has 3 columns: id (Primary key, integer),
        name (text),  description (text)
        '''
        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'CREATE TABLE categories (category_id INTEGER PRIMARY KEY AUTOINCREMENT, \
                                 name TEXT UNIQUE, description TEXT)'
        '''
        connects (and creates if necessary) to the database. gets a
        connection object
        '''
        con = sqlite3.connect(self.db_path)
        with con:
            '''
            get the cursor object. It allows to execute SQL code
            and traverse the result set
            '''
            cur = con.cursor()
            try:
                cur.execute(keys_on)        
                #execute the statement
                cur.execute(stmnt)
            except sqlite3.Error, excp:
                print "Error %s:" % excp.args[0]
        return None

    def create_items_table (self):
        '''
        Print an error message in the console if it could not be created. 
        creates items table
        items table has 4 columns: id (Primary key, integer),
        name (text),  category_id (FK categories table), description (text)
        '''
        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'CREATE TABLE items (item_id INTEGER PRIMARY KEY AUTOINCREMENT, \
                                 name TEXT, category_id INTEGER, descr_item TEXT, \
                                 UNIQUE(category_id, name), FOREIGN KEY(category_id) \
                                 REFERENCES categories(category_id) ON DELETE CASCADE)'
        '''
        connects (and creates if necessary) to the database. gets a
        connection object
        '''
        con = sqlite3.connect(self.db_path)
        with con:
            '''
            get the cursor object. It allows to execute SQL code
            and traverse the result set
            '''
            cur = con.cursor()
            try:
                cur.execute(keys_on)        
                #execute the statement
                cur.execute(stmnt)
            except sqlite3.Error, excp:
                print "Error %s:" % excp.args[0]
        return None

    def create_times_table (self):
        '''
        Print an error message in the console if it could not be created. 
        creates times table
        times table has 3 columns: id (Primary key, integer),
        open (real),  close (real)
        '''
        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'CREATE TABLE times (time_id INTEGER PRIMARY KEY AUTOINCREMENT, \
                                 open REAL, close REAL, \
                                 UNIQUE(open, close))'
        '''
        connects (and creates if necessary) to the database. gets a
        connection object
        '''
        con = sqlite3.connect(self.db_path)
        with con:
            '''
            get the cursor object. It allows to execute SQL code
            and traverse the result set
            '''
            cur = con.cursor()
            try:
                cur.execute(keys_on)        
                #execute the statement
                cur.execute(stmnt)
            except sqlite3.Error, excp:
                print "Error %s:" % excp.args[0]
        return None

    def create_schedules_table (self):
        '''
        Print an error message in the console if it could not be created. 
        creates schedules table
        schedules table has 8 columns: id (Primary key, integer),
        monday (integer),  tuesday (integer), wednesday (integer),
        thrusday (integer), friday (integer), saturday (integer),
        sunday (integer)
        '''
        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'CREATE TABLE schedules (schedule_id INTEGER PRIMARY KEY AUTOINCREMENT, \
                                monday_id INTEGER, tuesday_id INTEGER, \
                                wednesday_id INTEGER, thursday_id INTEGER, \
                                friday_id INTEGER, saturday_id INTEGER, \
                                sunday_id INTEGER, \
                                UNIQUE(monday_id, tuesday_id, \
                                    wednesday_id, thursday_id, friday_id, \
                                    saturday_id, sunday_id), \
                                FOREIGN KEY(monday_id) REFERENCES times(time_id) ON DELETE CASCADE, \
                                FOREIGN KEY(tuesday_id) REFERENCES times(time_id) ON DELETE CASCADE, \
                                FOREIGN KEY(wednesday_id) REFERENCES times(time_id) ON DELETE CASCADE, \
                                FOREIGN KEY(thursday_id) REFERENCES times(time_id) ON DELETE CASCADE, \
                                FOREIGN KEY(friday_id) REFERENCES times(time_id) ON DELETE CASCADE, \
                                FOREIGN KEY(saturday_id) REFERENCES times(time_id) ON DELETE CASCADE, \
                                FOREIGN KEY(sunday_id) REFERENCES times(time_id) ON DELETE CASCADE)'
        '''
        connects (and creates if necessary) to the database. gets a
        connection object
        '''
        con = sqlite3.connect(self.db_path)
        with con:
            '''
            get the cursor object. It allows to execute SQL code
            and traverse the result set
            '''
            cur = con.cursor()
            try:
                cur.execute(keys_on)        
                #execute the statement
                cur.execute(stmnt)
            except sqlite3.Error, excp:
                print "Error %s:" % excp.args[0]
        return None

    def create_stores_table (self):
        '''
        Print an error message in the console if it could not be created. 
        creates stores table
        stores table has 6 columns: id (Primary key, integer),
        name (text),  address (text), latitude (real),
        longitude (real), schedule (integer)
        '''
        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'CREATE TABLE stores (store_id INTEGER PRIMARY KEY AUTOINCREMENT, \
                                name TEXT, address TEXT UNIQUE, \
                                latitude REAL, longitude REAL, \
                                schedule_id INTEGER, UNIQUE(latitude, longitude), \
                                FOREIGN KEY(schedule_id) REFERENCES schedules(schedule_id) ON DELETE CASCADE)'
        '''
        connects (and creates if necessary) to the database. gets a
        connection object
        '''
        con = sqlite3.connect(self.db_path)
        with con:
            '''
            get the cursor object. It allows to execute SQL code
            and traverse the result set
            '''
            cur = con.cursor()
            try:
                cur.execute(keys_on)        
                #execute the statement
                cur.execute(stmnt)
            except sqlite3.Error, excp:
                print "Error %s:" % excp.args[0]
        return None


    def create_prices_table (self):
        '''
        Print an error message in the console if it could not be created. 
        creates items table
        prices table has 5 columns: id (Primary key, integer),
        value (real),  item_id (FK items table), store_id (FK stores table),
        timestamp (integer)
        '''
        keys_on = 'PRAGMA foreign_keys = ON'
        stmnt = 'CREATE TABLE prices (price_id INTEGER PRIMARY KEY AUTOINCREMENT, \
                                 value REAL, item_id INTEGER, store_id TEXT, \
                                 timestamp INTEGER, UNIQUE(item_id, store_id), \
                                 FOREIGN KEY(item_id) REFERENCES items(item_id) ON DELETE CASCADE, \
                                 FOREIGN KEY(store_id) REFERENCES stores(store_id) ON DELETE CASCADE)'
        '''
        connects (and creates if necessary) to the database. gets a
        connection object
        '''
        con = sqlite3.connect(self.db_path)
        with con:
            '''
            get the cursor object. It allows to execute SQL code
            and traverse the result set
            '''
            cur = con.cursor()
            try:
                cur.execute(keys_on)        
                #execute the statement
                cur.execute(stmnt)
            except sqlite3.Error, excp:
                print "Error %s:" % excp.args[0]
        return None

    def get_categories(self):
        '''
        Return a list of Categories of the database. Each category is serialized as a 
        dictionary that contains 3 keys: the id, the name and the description.
        Return None if the database has no categories. 
        '''
        #Create the SQL Statements
        #SQL Statement for activating foreign keys
        keys_on = 'PRAGMA foreign_keys = ON'
          #SQL Statement for retrieving the categories
        query = 'SELECT categories.* FROM categories'
        #Connects to the database. Gets a connection object
        con = sqlite3.connect(self.db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)        
            #Execute main SQL Statement
            cur.execute(query)
            #Process the results
            rows = cur.fetchall()
            if rows is None:
                return None
            #Process the response.
            categories = []
            for row in rows:
                categories.append(self._create_categories_object(row))
            return categories

    def _create_categories_object(self, row):
        '''
        It takes a database Row and transform it into a python dictionary.
        Dictionary has the following format:
            {'id':,'name':''
             'description':''
             }
            where:
             - id: id of the Category
             - name: name of the category
             - description: description of the category
        '''
        return {'id':row['category_id'],
                'name':row['name'],
                'description':row['description']}

    def get_items(self, category_id):
        '''
        Return a list of items for a category of the database. Each item is serialized as a 
        dictionary that contains 4 keys: the id, the name, the category id, and the description.
        Return None if the database has no items for the category.
        raises ValueError if the category id given does not exist
        '''

        
        #Create the SQL Statements
        #SQL Statement for activating foreign keys
        keys_on = 'PRAGMA foreign_keys = ON'
          #SQL Statement for retrieving the categories
        query1 = 'SELECT * FROM categories \
                    WHERE category_id = ?'
        query2 = 'SELECT * FROM items \
                    WHERE category_id = ?'
        #Connects to the database. Gets a connection object
        con = sqlite3.connect(self.db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)        
            #Execute main SQL Statement
            pvalue = (category_id)
            cur.execute(query1, pvalue)
            #Process the results
            rows = cur.fetchall()
            if rows is None:
                raise ValueError("The category does not exist")

            cur.execute(query2, pvalue)
            rows = cur.fetchall()

            if rows is None:
                return None
            #Process the response.
            items = []
            for row in rows:
                items.append(self._create_items_object(row))
            return items

    def _create_items_object(self, row):
        '''
        It takes a database Row and transform it into a python dictionary.
        Dictionary has the following format:
            {'id':,'name':'', 'category_id':,
             'description':''
             }
            where:
             - id: id of the Item
             - name: name of the item
             - category_id: id of the category the item belongs to
             - description: description of the item
        '''
        return {'id':row['item_id'],
                'name':row['name'],
                'category_id':row['category_id'],
                'description':row['descr_item']}

    def get_prices(self, item_id):
        '''
        Return a list of prices for an item of the database. Each price is serialized as a 
        dictionary that contains 5 keys: the id, the price, the item id, the store id, and the timestamp.
        Return None if the database has no prices for the item.
        raises ValueError if the item id given does not exist
        '''

        
        #Create the SQL Statements
        #SQL Statement for activating foreign keys
        keys_on = 'PRAGMA foreign_keys = ON'
          #SQL Statement for retrieving the categories
        query1 = 'SELECT * FROM items \
                    WHERE item_id = ?'
        query2 = 'SELECT * FROM prices \
                    WHERE item_id = ?'
        #Connects to the database. Gets a connection object
        con = sqlite3.connect(self.db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)        
            #Execute main SQL Statement
            pvalue = (item_id)
            cur.execute(query1, item_id)
            #Process the results
            rows = cur.fetchall()
            if rows is None:
                raise ValueError("The item does not exist")

            cur.execute(query2, pvalue)
            rows = cur.fetchall()

            if rows is None:
                return None
            #Process the response.
            prices = []
            for row in rows:
                prices.append(self._create_prices_object(row))
            return prices

    def _create_prices_object(self, row):
        '''
        It takes a database Row and transform it into a python dictionary.
        Dictionary has the following format:
            {'id':,'value':, 'item_id':,'store_id':,
             'timestamp':
             }
            where:
             - id: id of the Price
             - value: value of the Price
             - item_id: id of the item the price belongs to
             - store_id: id of the store the price belongs to
             - timestamp: time of the creation or update of this price
        '''
        return {'id':row['price_id'],
                'value':row['value'],
                'item_id':row['item_id'],
                'store_id':row['store_id'],
                'timestamp':row['timestamp']}

    def get_store(self, store_id):
        '''
        Return a store of the database given its id. The store is serialized as a 
        dictionary that contains 6 keys: the id, the name, the address, the latitude, the longitude and the schedule id.
        Return None if the database has no store with this id.
        '''

        
        #Create the SQL Statements
        #SQL Statement for activating foreign keys
        keys_on = 'PRAGMA foreign_keys = ON'
          #SQL Statement for retrieving the categories
        query = 'SELECT * FROM stores \
                    WHERE store_id = ?'
        #Connects to the database. Gets a connection object
        con = sqlite3.connect(self.db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)        
            #Execute main SQL Statement
            pvalue = (store_id)
            cur.execute(query, store_id)
            #Process the results
            row = cur.fetchone()
            if row is None:
                return None

            return self._create_store_object(row)

    def _create_store_object(self, row):
        '''
        It takes a database Row and transform it into a python dictionary.
        Dictionary has the following format:
            {'id':,'name':'', 'address':'','latitude':,'longitude':,
             'schedule_id':
             }
            where:
             - id: id of the store
             - name: name of the store
             - address: address of the store
             - latitude: latitude of the store
             - longitude: longitude of the store
             - schedule_id: id of the schedule of the store
        '''
        return {'id':row['store_id'],
                'name':row['name'],
                'address':row['address'],
                'latitude':row['latitude'],
                'longitude':row['longitude'],
                'schedule_id':row['schedule_id']}

    def get_schedule(self, schedule_id):
        '''
        Return a schedule of the database given its id. The schedule is serialized as a 
        dictionary that contains 8 keys: the id, the monday id, the tuesday id, the wednesday id, the thursday id,
        the friday id, the saturday id and the sunday id.
        Return None if the database has no schedule with this id.
        '''

        
        #Create the SQL Statements
        #SQL Statement for activating foreign keys
        keys_on = 'PRAGMA foreign_keys = ON'
          #SQL Statement for retrieving the categories
        query = 'SELECT * FROM schedules \
                    WHERE schedule_id = ?'
        #Connects to the database. Gets a connection object
        con = sqlite3.connect(self.db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)        
            #Execute main SQL Statement
            pvalue = (schedule_id)
            cur.execute(query, schedule_id)
            #Process the results
            row = cur.fetchone()
            if row is None:
                return None

            return self._create_schedule_object(row)

    def _create_schedule_object(self, row):
        '''
        It takes a database Row and transform it into a python dictionary.
        Dictionary has the following format:
            {'id':,'monday_id':, 'tuesday_id':,'wednesday_id':,
             'thursday_id':','friday_id':,'saturday_id':,'sunday_id':
             }
            where:
             - id: id of the schedule
             - monday_id: time id for monday
             - tuesday_id: time id for tuesday
             - wednesday_id: time id for wednesday
             - thursday_id: time id for thursday
             - friday_id: time id for friday
             - saturday_id: time id for saturday
             - sunday_id: time id for sunday
        '''
        return {'id':row['schedule_id'],
                'monday_id':row['monday_id'],
                'tuesday_id':row['tuesday_id'],
                'wednesday_id':row['wednesday_id'],
                'thursday_id':row['thursday_id'],
                'friday_id':row['friday_id'],
                'saturday_id':row['saturday_id'],
                'sunday_id':row['sunday_id']}

    def get_time(self, time_id):
        '''
        Return a time of the database given its id. The time is serialized as a 
        dictionary that contains 3 keys: the id, the opening time and the closing time.
        Return None if the database has no time with this id.
        '''

        
        #Create the SQL Statements
        #SQL Statement for activating foreign keys
        keys_on = 'PRAGMA foreign_keys = ON'
          #SQL Statement for retrieving the categories
        query = 'SELECT * FROM times \
                    WHERE time_id = ?'
        #Connects to the database. Gets a connection object
        con = sqlite3.connect(self.db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)        
            #Execute main SQL Statement
            pvalue = (time_id)
            cur.execute(query, time_id)
            #Process the results
            row = cur.fetchone()
            if row is None:
                return None

            return self._create_time_object(row)

    def _create_time_object(self, row):
        '''
        It takes a database Row and transform it into a python dictionary.
        Dictionary has the following format:
            {'id':,'open':, 'close':
             }
            where:
             - id: id of the time
             - open: hour when it opens
             - close: hour when it closes
        '''
        return {'id':row['row_id'],
                'open':row['open'],
                'close':row['close']}

    def create_category(self, name, description=""):
        '''
        Create a new category with the data provided as arguments. 
        INPUT:    
            - name: the category's name
            - description: the category's description
        OUTPUT: 
            - returns the id of the created category
        raises ShopDatabaseError if the database could not be modified.
        '''
        
        #Create the SQL Statements
          #SQL Statement for activating foreign keys
        keys_on = 'PRAGMA foreign_keys = ON'
          #SQL Statement for extracting the userid given a nickname
        query = 'INSERT INTO categories(name, description)\
                  VALUES(?,?)'
       
        
        #Connects to the database. Gets a connection object
        con = sqlite3.connect(self.db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)        

            
            
            pvalue = (name,description)
            cur.execute(query, pvalue)
            
            lid = cur.lastrowid
            return lid

    def create_item(self, name, category_id, descr_item=""):
        '''
        Create a new item with the data provided as arguments. 
        INPUT:    
            - name: the item's name
            - category_id: the category id the item belongs to
            - descr_item: the item's description
        OUTPUT: 
            - returns the id of the created item
        raises ShopDatabaseError if the database could not be modified.
        raises ValueError if the category does not exist
        '''
        
        #Create the SQL Statements
          #SQL Statement for activating foreign keys
        keys_on = 'PRAGMA foreign_keys = ON'
          #SQL Statement for extracting the userid given a nickname
        query1 = 'SELECT * FROM categories \
                    WHERE category_id = ?'
        query2 = 'INSERT INTO items(name, category_id, descr_item)\
                  VALUES(?,?,?)'
       
        
        #Connects to the database. Gets a connection object
        con = sqlite3.connect(self.db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)        

            pvalue = (category_id)
            cur.execute(query1, pvalue)

            row = cur.fetchone()
            if row is None:
                raise ValueError("The category does not exist")
            
            pvalue = (name,category_id,descr_item)
            cur.execute(query2, pvalue)
            
            lid = cur.lastrowid
            return lid

    def update_price(self, value, item_id, store_id):
        '''
        Create a new item with the data provided as arguments. 
        INPUT:    
            - name: the item's name
            - category_id: the category id the item belongs to
            - descr_item: the item's description
        OUTPUT: 
            - returns the id of the created item
        raises ShopDatabaseError if the database could not be modified.
        raises ValueError if the item_id does not exist
        raises ValueError if the store_id does not exist
        '''
        
        #Create the SQL Statements
          #SQL Statement for activating foreign keys
        keys_on = 'PRAGMA foreign_keys = ON'
          #SQL Statement for extracting the userid given a nickname
        query1 = 'SELECT * FROM items \
                    WHERE item_id = ?'
        query2 = 'SELECT * FROM stores \
                    WHERE store_id = ?'
        query3 = 'SELECT * FROM prices \
                  WHERE item_id = ? AND store_id = ?'
        query4 = 'INSERT INTO prices(value, item_id, store_id, timestamp)\
                  VALUES(?,?,?,?)'
        query5 = 'UPDATE prices SET value = ?, timestamp = ? \
                  WHERE price_id = ?'

        
        #temporal variables for messages table 
        #timestamp will be used for lastlogin and regDate.
        timestamp = time.mktime(datetime.now().timetuple())

        #Connects to the database. Gets a connection object
        con = sqlite3.connect(self.db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)        

            pvalue = (item_id)
            cur.execute(query1, pvalue)

            row = cur.fetchone()
            if row is None:
                raise ValueError("The item does not exist")
            
            pvalue = (store_id)
            cur.execute(query2, pvalue)

            row = cur.fetchone()
            if row is None:
                raise ValueError("The store does not exist")

            pvalue = (item_id, store_id)
            cur.execute(query3, pvalue)

            row = cur.fetchone()
            if row is None:
                pvalue = (value, item_id, store_id, timestamp)
                cur.execute(query4, pvalue)
                
                lid = cur.lastrowid
                return lid
            else:
                price_id = row['price_id']
                pvalue = (value, timestamp, price_id)
                cur.execute(query5, pvalue)
                return price_id


            

    def create_store(self, name, address, latitude, longitude, schedule_id):
        '''
        Create a new store with the data provided as arguments. 
        INPUT:    
            - name: the store's name
            - address: the store's address
            - latitude: the store's latitude
            - longitude: the store's longitude
            - schedule_id: the id of the schedule that belongs to the store
        OUTPUT: 
            - returns the id of the created store
        raises ShopDatabaseError if the database could not be modified.
        raises ValueError if the schedule_id does not exist
        '''
        
        #Create the SQL Statements
          #SQL Statement for activating foreign keys
        keys_on = 'PRAGMA foreign_keys = ON'
          #SQL Statement for extracting the userid given a nickname
        query1 = 'SELECT * FROM schedules \
                    WHERE schedule_id = ?'
        query2 = 'INSERT INTO stores(name, address, latitude, longitude, schedule_id)\
                  VALUES(?,?,?,?,?)'
       
        
        #Connects to the database. Gets a connection object
        con = sqlite3.connect(self.db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)        

            pvalue = (schedule_id)
            cur.execute(query1, pvalue)

            row = cur.fetchone()
            if row is None:
                raise ValueError("The schedule does not exist")
            
            pvalue = (name, address, latitude, longitude, schedule_id)
            cur.execute(query2, pvalue)
            
            lid = cur.lastrowid
            return lid

    def create_schedule(self, monday_id, tuesday_id, wednesday_id, thursday_id, friday_id, saturday_id, sunday_id):
        '''
        Create a new schedule with the data provided as arguments. 
        INPUT:    
            - monday_id: the time id for monday
            - tuesday_id: the time id for tuesday
            - wednesday_id: the time id for wednesday
            - thursday_id: the time id for thursday
            - friday_id: the time id for friday
            - saturday_id: the time id for saturday
            - sunday_id: the time id for sunday
        OUTPUT: 
            - returns the id of the created schedule
        raises ShopDatabaseError if the database could not be modified.
        raises ValueError if the monday_id does not exist on the times table
        raises ValueError if the tuesday_id does not exist on the times table
        raises ValueError if the wednesday_id does not exist on the times table
        raises ValueError if the thursday_id does not exist on the times table
        raises ValueError if the friday_id does not exist on the times table
        raises ValueError if the saturday_id does not exist on the times table
        raises ValueError if the sunday_id does not exist on the times table
        '''
        
        #Create the SQL Statements
          #SQL Statement for activating foreign keys
        keys_on = 'PRAGMA foreign_keys = ON'
          #SQL Statement for extracting the userid given a nickname
        query1 = 'SELECT * FROM times \
                    WHERE time_id = ?'
        query2 = 'INSERT INTO schedules(monday_id, tuesday_id, wednesday_id, thursday_id, friday_id, saturday_id, sunday_id)\
                  VALUES(?,?,?,?,?,?,?)'
       
        
        #Connects to the database. Gets a connection object
        con = sqlite3.connect(self.db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)        

            pvalue = (monday_id)
            cur.execute(query1, pvalue)

            row = cur.fetchone()
            if row is None:
                raise ValueError("The time for monday does not exist")

            pvalue = (tuesday_id)
            cur.execute(query1, pvalue)

            row = cur.fetchone()
            if row is None:
                raise ValueError("The time for tuesday does not exist")


            pvalue = (wednesday_id)
            cur.execute(query1, pvalue)

            row = cur.fetchone()
            if row is None:
                raise ValueError("The time for wednesday does not exist")


            pvalue = (thursday_id)
            cur.execute(query1, pvalue)

            row = cur.fetchone()
            if row is None:
                raise ValueError("The time for thursday does not exist")


            pvalue = (friday_id)
            cur.execute(query1, pvalue)

            row = cur.fetchone()
            if row is None:
                raise ValueError("The time for friday does not exist")


            pvalue = (saturday_id)
            cur.execute(query1, pvalue)

            row = cur.fetchone()
            if row is None:
                raise ValueError("The time for saturday does not exist")


            pvalue = (sunday_id)
            cur.execute(query1, pvalue)

            row = cur.fetchone()
            if row is None:
                raise ValueError("The time for sunday does not exist")
            
            pvalue = (monday_id, tuesday_id, wednesday_id, thursday_id, friday_id, saturday_id, sunday_id)
            cur.execute(query2, pvalue)
            
            lid = cur.lastrowid
            return lid

    def create_time(self, p_open, p_close):
        '''
        Create a new time with the data provided as arguments. 
        INPUT:    
            - open: the opening time for this time
            - description: the closing time for this time
        OUTPUT: 
            - returns the id of the created time
        raises ShopDatabaseError if the database could not be modified.
        '''
        
        #Create the SQL Statements
          #SQL Statement for activating foreign keys
        keys_on = 'PRAGMA foreign_keys = ON'
          #SQL Statement for extracting the userid given a nickname
        query = 'INSERT INTO times(open, close)\
                  VALUES(?,?)'
       
        
        #Connects to the database. Gets a connection object
        con = sqlite3.connect(self.db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)        

            
            
            pvalue = (p_open, p_close)
            cur.execute(query, pvalue)
            
            lid = cur.lastrowid
            return lid