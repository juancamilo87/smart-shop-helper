import sqlite3, unittest

from .database_api_tests_common import BaseTestCase, db, db_path

class PriceDbAPITestCase(BaseTestCase):
    '''
            The format of the Price dictionary is the following:
            {
            'id':,
            'value':,
            'item_id':,
            'store_id':,
            'timestamp':
            }
            
            where:
             - id: id of the Price
             - value: value of the Price
             - item_id: id of the item the price belongs to
             - store_id: id of the store the price belongs to
             - timestamp: time of the creation or update of this price
    '''
    #the strip function removes the tabs generated.
    price1_id = 1
    price1_value = 0.98
    price1_item_id = 1
    price1_store_id = 1
    price1_timestamp = 1234915418.000000
    price1 = {
              'id':price1_id,
              'value':price1_value,
              'item_id':price1_item_id,
              'store_id':price1_store_id,
              'timestamp':price1_timestamp
             }

    price2_id = 2
    price2_value = 1.10
    price2_item_id = 1
    price2_store_id = 2
    price2_timestamp = 1234915419.000000
    price2 = {
              'id':price2_id,
              'value':price2_value,
              'item_id':price2_item_id,
              'store_id':price2_store_id,
              'timestamp':price2_timestamp
             }


    prices = [price1, price2]

    new_price1_value = 0.89
    new_price1_item_id = 2
    new_price1_store_id = 1
    new_price1 = {
              'id':3,
              'value':new_price1_value,
              'item_id':new_price1_item_id,
              'store_id':new_price1_store_id,
              'timestamp':price2_timestamp
             }

    new_price2_value = 0.87
    new_price2_item_id = 2
    new_price2_store_id = 1
    new_price2 = {
              'id':3,
              'value':new_price2_value,
              'item_id':new_price2_item_id,
              'store_id':new_price2_store_id,
              'timestamp':price2_timestamp
             }

    initial_size = 2
 
    @classmethod
    def setUpClass(cls):
        print "Testing ", cls.__name__

    def test_prices_table_created(self):
        '''
        Checks that the table initially contains 2 prices (check 
        shop_data_dump.sql)
        '''
        print '('+self.test_prices_table_created.__name__+')', \
              self.test_prices_table_created.__doc__
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query1 = 'SELECT * FROM prices'
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
            prices = cur.fetchall()
            #Assert
            self.assertEquals(len(prices), self.initial_size)
        if con:
            con.close()

    def test_create_prices_object(self):
        '''
        Check that the method create_pruces_object works return adequate values
        for the first database row.
        '''
        print '('+self.test_create_prices_object.__name__+')', \
              self.test_create_prices_object.__doc__
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM prices'
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
            price = db._create_prices_object(row)
            self.assertDictContainsSubset(price, self.price1)

    def test_get_prices(self):
        '''
        Test get_prices
        '''
        print '('+self.test_get_prices.__name__+')', \
              self.test_get_prices.__doc__
        #Test with existing items
        prices = db.get_prices('1')
        self.assertListEqual(prices, self.prices)

    def test_create_price(self):
        '''
        Test that I can add new prices
        '''
        print '('+self.test_create_price.__name__+')', \
              self.test_create_price.__doc__
        price_id = db.update_price(self.new_price1_value, self.new_price1_item_id, \
                                    self.new_price1_store_id)
        self.assertIsNotNone(price_id)

        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM prices \
                          WHERE price_id = ?'
        #Connects to the database.
        con = sqlite3.connect(db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement        
            pvalue = (price_id,)
            cur.execute(query, pvalue)
            #Extrac the row
            row = cur.fetchone()
            #Test the method
            new_price_value = row['value']
            new_price_item_id = row['item_id']
            new_price_store_id = row['store_id']
            self.assertEquals(price_id, self.new_price1['id'])
            self.assertEquals(new_price_value, self.new_price1['value'])
            self.assertEquals(new_price_item_id, self.new_price1['item_id'])
            self.assertEquals(new_price_store_id, self.new_price1['store_id'])
    
    def test_update_price(self):
        '''
        Test that I can update a price
        '''
        print '('+self.test_update_price.__name__+')', \
              self.test_update_price.__doc__
        price_id = db.update_price(self.new_price2_value, self.new_price2_item_id, \
                                    self.new_price2_store_id)
        self.assertIsNotNone(price_id)

        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM prices \
                          WHERE price_id = ?'
        #Connects to the database.
        con = sqlite3.connect(db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement        
            pvalue = (price_id,)
            cur.execute(query, pvalue)
            #Extrac the row
            row = cur.fetchone()
            #Test the method
            new_price_value = row['value']
            new_price_item_id = row['item_id']
            new_price_store_id = row['store_id']
            self.assertEquals(price_id, self.new_price2['id'])
            self.assertEquals(new_price_value, self.new_price2['value'])
            self.assertEquals(new_price_item_id, self.new_price2['item_id'])
            self.assertEquals(new_price_store_id, self.new_price2['store_id'])


    def test_create_price_of_nonexisting_item(self):
        '''
        Test that I can not add new prices of nonexisting items
        item_id = '5'
        '''
        print '('+self.test_create_price_of_nonexisting_item.__name__+')', \
              self.test_create_price_of_nonexisting_item.__doc__

        with self.assertRaises(ValueError):
            db.update_price(self.new_price2_value, '5', \
                                    self.new_price2_store_id)

    def test_create_price_of_nonexisting_store(self):
        '''
        Test that I can not add new prices of nonexisting store
        store_id = '5'
        '''
        print '('+self.test_create_price_of_nonexisting_item.__name__+')', \
              self.test_create_price_of_nonexisting_item.__doc__

        with self.assertRaises(ValueError):
            db.update_price(self.new_price2_value, self.new_price2_item_id, \
                                    '5')

if __name__ == '__main__':
    print 'Start running tests'
    unittest.main()
