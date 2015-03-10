import sqlite3, unittest

from .database_api_tests_common import BaseTestCase, db, db_path

class StoreDbAPITestCase(BaseTestCase):
    '''
            The format of the Store dictionary is the following:
            {
            'id':,
            'name':'',
            'address':'',
            'latitude':,
            'longitude':,
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
    #the strip function removes the tabs generated.
    store1_id = 1
    store1_name = 'Tokmanni'
    store1_address = 'Kaijonharju 16'
    store1_latitude = 65.0587568
    store1_longitude = 25.4775946
    store1_schedule_id = 1
    store1 = {
                'id':store1_id,
                'name':store1_name,
                'address':store1_address,
                'latitude':store1_latitude,
                'longitude':store1_longitude,
                'schedule_id':store1_schedule_id
             }

    store2_id = 2
    store2_name = 'Sale'
    store2_address = 'Kaijonharju 25'
    store2_latitude = 65.0600145
    store2_longitude = 25.4792039
    store2_schedule_id = 2
    store2 = {
                'id':store2_id,
                'name':store2_name,
                'address':store2_address,
                'latitude':store2_latitude,
                'longitude':store2_longitude,
                'schedule_id':store2_schedule_id
             }
             
    new_store1_id = 3
    new_store1_name = 'Prisma'
    new_store1_address = 'Kaijonharju 34'
    new_store1_latitude = 65.0541145
    new_store1_longitude = 25.4558150
    new_store1_schedule_id = 1
    new_store1 = {
                'id':new_store1_id,
                'name':new_store1_name,
                'address':new_store1_address,
                'latitude':new_store1_latitude,
                'longitude':new_store1_longitude,
                'schedule_id':new_store1_schedule_id
             }

    new_store2_name = 'R-Kioski'
    new_store2_address = 'Kaijonharju 26'
    new_store2_latitude = 65.0600145
    new_store2_longitude = 25.4792039
    new_store2_schedule_id = 1

    new_store3_name = 'R-Kioski 2'
    new_store3_address = 'Kaijonharju 26'
    new_store3_latitude = 65.9200145
    new_store3_longitude = 25.4792039
    new_store3_schedule_id = 10

    initial_size = 2
 
    @classmethod
    def setUpClass(cls):
        print "Testing ", cls.__name__

    def test_stores_table_created(self):
        '''
        Checks that the table initially contains 2 stores (check 
        shop_data_dump.sql)
        '''
        print '('+self.test_stores_table_created.__name__+')', \
              self.test_stores_table_created.__doc__
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query1 = 'SELECT * FROM stores'
        #Connects to the database.
        con = sqlite3.connect(db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement        
            cur.execute(query1)
            stores = cur.fetchall()
            #Assert
            self.assertEquals(len(stores), self.initial_size)
        if con:
            con.close()

    def test_create_stores_object(self):
        '''
        Check that the method create_stores_object works return adequate values
        for the first database row.
        '''
        print '('+self.test_create_stores_object.__name__+')', \
              self.test_create_stores_object.__doc__
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM stores'
        #Connects to the database.
        con = sqlite3.connect(db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement        
            cur.execute(query)
            #Extrac the row
            row = cur.fetchone()
            #Test the method
            store = db._create_store_object(row)
            self.assertDictContainsSubset(store, self.store1)

    def test_get_store(self):
        '''
        Test get_store
        '''
        print '('+self.test_get_store.__name__+')', \
              self.test_get_store.__doc__
        #Test with existing stores
        store = db.get_store(self.store2_id)
        self.assertDictContainsSubset(store, self.store2)

    def test_create_store(self):
        '''
        Test that I can add new stores
        '''
        print '('+self.test_create_store.__name__+')', \
              self.test_create_store.__doc__
        store_id = db.create_store(self.new_store1_name, \
                                         self.new_store1_address, \
                                         self.new_store1_latitude, \
                                         self.new_store1_longitude, \
                                         self.new_store1_schedule_id)
        self.assertIsNotNone(store_id)

        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM stores \
                          WHERE store_id = ?'
        #Connects to the database.
        con = sqlite3.connect(db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement        
            pvalue = (store_id,)
            cur.execute(query, pvalue)
            #Extrac the row
            row = cur.fetchone()
            #Test the method
            new_store_name = row['name']
            new_store_address = row['address']
            new_store_latitude = row['latitude']
            new_store_longitude = row['longitude']
            new_store_schedule_id = row['schedule_id']
            self.assertEquals(store_id, self.new_store1['id'])
            self.assertEquals(new_store_name, self.new_store1['name'])
            self.assertEquals(new_store_address, self.new_store1['address'])
            self.assertEquals(new_store_latitude, self.new_store1['latitude'])
            self.assertEquals(new_store_longitude, self.new_store1['longitude'])
            self.assertEquals(new_store_schedule_id, self.new_store1['schedule_id'])
    
    def test_create_existing_store(self):
        '''
        Test that I cannot add two stores with the same coordinates (latitude, longitude)
        '''
        print '('+self.test_create_existing_store.__name__+')', \
              self.test_create_existing_store.__doc__
        with self.assertRaises(sqlite3.IntegrityError):
            db.create_store(self.new_store2_name, \
                                 self.new_store2_address, \
                                 self.new_store2_latitude, \
                                 self.new_store2_longitude, \
                                 self.new_store2_schedule_id)

    def test_create_store_with_nonexisting_schedule(self):
        '''
        Test that I can not add new stores with nonexisting schedules
        schedule_id = '10'
        '''
        print '('+self.test_create_store_with_nonexisting_schedule.__name__+')', \
              self.test_create_store_with_nonexisting_schedule.__doc__

        
        with self.assertRaises(ValueError):
           db.create_store(self.new_store3_name, \
                                 self.new_store3_address, \
                                 self.new_store3_latitude, \
                                 self.new_store3_longitude, \
                                 self.new_store3_schedule_id)

if __name__ == '__main__':
    print 'Start running tests'
    unittest.main()
