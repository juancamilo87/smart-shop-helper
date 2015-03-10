import sqlite3, unittest

from .database_api_tests_common import BaseTestCase, db, db_path

class TimeDbAPITestCase(BaseTestCase):
    '''
            The format of the Time dictionary is the following:
            {
            'id':,
            'open':,
            'close':
            }
            
            where:
             - id: unique identifier of the time
             - open: time at which it opens
             - close: time at which it closes
    '''
    #the strip function removes the tabs generated.
    time1_open = 8
    time1_close = 20
    time1_id = 1
    time1 = {
                  'id':time1_id,
                  'open':time1_open,
                  'close':time1_close
                }

    time2_open = 8
    time2_close = 22
    time2_id = 2
    time2 = {
                  'id':time2_id,
                  'open':time2_open,
                  'close':time2_close
                }

    new_time1_open = 9
    new_time1_close = 20
    new_time1 = {
                    'id':3,
                    'open':new_time1_open,
                    'close':new_time1_close
                }

    initial_size = 2
 
    @classmethod
    def setUpClass(cls):
        print "Testing ", cls.__name__

    def test_times_table_created(self):
        '''
        Checks that the table initially contains 2 times (check 
        shop_data_dump.sql)
        '''
        print '('+self.test_times_table_created.__name__+')', \
              self.test_times_table_created.__doc__
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query1 = 'SELECT * FROM times'
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
            times = cur.fetchall()
            #Assert
            self.assertEquals(len(times), self.initial_size)
        if con:
            con.close()

    def test_create_times_object(self):
        '''
        Check that the method create_times_object works return adequate values
        for the first database row.
        '''
        print '('+self.test_create_times_object.__name__+')', \
              self.test_create_times_object.__doc__
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM times'
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
            time = db._create_time_object(row)
            self.assertDictContainsSubset(time, self.time1)

    def test_get_time(self):
        '''
        Test get_time
        '''
        print '('+self.test_get_time.__name__+')', \
              self.test_get_time.__doc__
        #Test with existing categories
        time = db.get_time(self.time2_id)
        self.assertDictContainsSubset(time, self.time2)

    def test_create_time(self):
        '''
        Test that I can add new times
        '''
        print '('+self.test_create_time.__name__+')', \
              self.test_create_time.__doc__
        time_id = db.create_time(self.new_time1_open, self.new_time1_close)
        self.assertIsNotNone(time_id)

        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM times \
                          WHERE time_id = ?'
        #Connects to the database.
        con = sqlite3.connect(db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement        
            pvalue = (time_id,)
            cur.execute(query, pvalue)
            #Extrac the row
            row = cur.fetchone()
            #Test the method
            new_time_open = row['open']
            new_time_close = row['close']
            self.assertEquals(time_id, self.new_time1['id'])
            self.assertEquals(new_time_open, self.new_time1['open'])
            self.assertEquals(new_time_close, self.new_time1['close'])
    
    def test_create_existing_time(self):
        '''
        Test that I cannot add two items with the same open and close
        '''
        print '('+self.test_create_existing_time.__name__+')', \
              self.test_create_existing_time.__doc__

        with self.assertRaises(sqlite3.IntegrityError):
            db.create_time(self.time1_open, self.time1_close)

if __name__ == '__main__':
    print 'Start running tests'
    unittest.main()
