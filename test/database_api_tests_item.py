import sqlite3, unittest

from .database_api_tests_common import BaseTestCase, db, db_path

class ItemDbAPITestCase(BaseTestCase):
    '''
            The format of the Item dictionary is the following:
            {
            'id':,
            'name':'',
            'category_id':,
            'description':''
            }
            
            where:
             - id: unique identifier of the item
             - name: name of the item
             - category_id: unique identifier of the category the item belongs to
             - description: description of the item
    '''
    #the strip function removes the tabs generated.
    item1_name = 'High Fat'
    item1_id = 1
    item1_category_id = 1
    item1_description = 'High Fat milk'
    item1 = {
                  'id':item1_id,
                  'name':item1_name,
                  'category_id':item1_category_id,
                  'description':item1_description
                }

    item2_name = 'Low Fat'
    item2_id = 2
    item2_category_id = 1
    item2_description = 'Low Fat Milk'
    item2 = {
                  'id':item2_id,
                  'name':item2_name,
                  'category_id':item2_category_id,
                  'description':item2_description
                }


    items = [item1, item2]

    new_item1_name = 'Banana'
    new_item1_description = 'Banana'
    new_item1_category_id = 2
    new_item1 = {
                    'id':3,
                    'name':new_item1_name,
                    'category_id':new_item1_category_id,
                    'description':new_item1_description
                    }

    new_item2_name = 'Orange'
    new_item2_category_id = 2
    new_item2 = {
                    'id':3,
                    'name':new_item2_name,
                    'category_id':new_item2_category_id,
                    'description':None
                    }

    initial_size = 2
 
    @classmethod
    def setUpClass(cls):
        print "Testing ", cls.__name__

    def test_items_table_created(self):
        '''
        Checks that the table initially contains 2 items (check 
        shop_data_dump.sql)
        '''
        print '('+self.test_items_table_created.__name__+')', \
              self.test_items_table_created.__doc__
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query1 = 'SELECT * FROM items'
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
            items = cur.fetchall()
            #Assert
            self.assertEquals(len(items), self.initial_size)
        if con:
            con.close()

    def test_create_items_object(self):
        '''
        Check that the method create_items_object works return adequate values
        for the first database row.
        '''
        print '('+self.test_create_items_object.__name__+')', \
              self.test_create_items_object.__doc__
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM items'
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
            item = db._create_items_object(row)
            self.assertDictContainsSubset(item, self.item1)

    def test_get_items(self):
        '''
        Test get_items
        '''
        print '('+self.test_get_items.__name__+')', \
              self.test_get_items.__doc__
        #Test with existing items
        items = db.get_items('1')
        self.assertListEqual(items, self.items)

    def test_create_item(self):
        '''
        Test that I can add new items
        '''
        print '('+self.test_create_item.__name__+')', \
              self.test_create_item.__doc__
        item_id = db.create_item(self.new_item1_name, self.new_item1_category_id, \
                                    self.new_item1_description)
        self.assertIsNotNone(item_id)

        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM items \
                          WHERE item_id = ?'
        #Connects to the database.
        con = sqlite3.connect(db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement        
            pvalue = (item_id,)
            cur.execute(query, pvalue)
            #Extrac the row
            row = cur.fetchone()
            #Test the method
            new_item_name = row['name']
            new_item_category_id = row['category_id']
            new_item_description = row['descr_item']
            self.assertEquals(item_id, self.new_item1['id'])
            self.assertEquals(new_item_name, self.new_item1['name'])
            self.assertEquals(new_item_category_id, self.new_item1['category_id'])
            self.assertEquals(new_item_description, self.new_item1['description'])
    
    def test_create_existing_item(self):
        '''
        Test that I cannot add two items with the same name and category_id
        '''
        print '('+self.test_create_existing_item.__name__+')', \
              self.test_create_existing_item.__doc__
        with self.assertRaises(sqlite3.IntegrityError):
            db.create_item(self.item1_name, self.item1_category_id, \
                                    self.item1_description)

    def test_create_item_without_description(self):
        '''
        Test that I can add new items without description
        '''
        print '('+self.test_create_item_without_description.__name__+')', \
              self.test_create_item_without_description.__doc__

        item_id = db.create_item(self.new_item2_name, self.new_item2_category_id)
        self.assertIsNotNone(item_id)

        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM items \
                          WHERE item_id = ?'
        #Connects to the database.
        con = sqlite3.connect(db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement        
            pvalue = (item_id,)
            cur.execute(query, pvalue)
            #Extrac the row
            row = cur.fetchone()
            #Test the method
            new_item_name = row['name']
            new_item_category_id = row['category_id']
            new_item_description = row['descr_item']
            self.assertEquals(item_id, self.new_item2['id'])
            self.assertEquals(new_item_name, self.new_item2['name'])
            self.assertEquals(new_item_category_id, self.new_item2['category_id'])
            self.assertEquals(new_item_description, self.new_item2['description'])

    def test_create_item_of_nonexisting_category(self):
        '''
        Test that I can not add new items of nonexisting category
        category_id = '5'
        '''
        print '('+self.test_create_item_without_description.__name__+')', \
              self.test_create_item_without_description.__doc__

        with self.assertRaises(ValueError):
            db.create_item('Beef', '10') 

if __name__ == '__main__':
    print 'Start running tests'
    unittest.main()
