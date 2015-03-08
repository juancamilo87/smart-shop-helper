

from datetime import datetime
import time, sqlite3, sys, re, os

class ShopDatabase(object):
    '''
    API to access Forurm database. 
    '''
    

    def __init__(self, db_path):
        '''
        db_path is the address of the path with respect to the calling script.
        If db_path is None, DEFAULT_DB_PATH is used instead.
        '''
        super(ShopDatabase, self).__init__()
        self.db_path = db_path
        

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

    #MANAGING THE CONNECTIONS:
    def check_foreign_keys_status(self):
        '''
        Checks the status of foreign keys
        '''
        con = None
        try:
            #Connects (and creates if necessary) to the database. Gets a connection object
            con = sqlite3.connect('db_path')
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
        con = sqlite3.connect('shop.db')
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
        con = sqlite3.connect('shop.db')
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
        con = sqlite3.connect('shop.db')
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
        con = sqlite3.connect('shop.db')
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
                                FOREIGN KEY(schedule_id) REFERENCES schedule(schedule_id) ON DELETE CASCADE)'
        '''
        connects (and creates if necessary) to the database. gets a
        connection object
        '''
        con = sqlite3.connect('shop.db')
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
        con = sqlite3.connect('shop.db')
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