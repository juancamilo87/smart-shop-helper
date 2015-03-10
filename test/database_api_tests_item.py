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
    item1_name = 'Mystery'
    item1_id = 1
    item1_category_id = 1
    item1_description = ''
    item1 = {
                  'id':item1_id,
                  'name':item1_name,
                  'category_id':item1_category_id,
                  'description':item1_description
                }

    item2_name = 'Mystery'
    item2_id = 2
    item2_category_id = 1
    item2_description = ''
    item2 = {
                  'id':item2_id,
                  'name':item2_name,
                  'category_id':item2_category_id,
                  'description':item2_description
                }


    items = [item1, item2]

    new_item1_name = 'sully'
    new_item1_description = ''
    new_item1_category_id = 2
    new_item1 = {
                    'id':3,
                    'name':new_item1_name,
                    'category_id':,new_item1_category_id
                    'description':new_item1_description
                    }

    new_item2_name = 'sully'
    new_item2_category_id = 2
    new_item2 = {
                    'id':4,
                    'name':new_item2_name,
                    'category_id':,new_item2_category_id
                    'description':null
                    }

    initial_size = 2
 
    @classmethod
    def setUpClass(cls):
        print "Testing ", cls.__name__

    def test_categories_table_created(self):
        '''
        Checks that the table initially contains 2 categories (check 
        shop_data_dump.sql)
        '''
        print '('+self.test_categories_table_created.__name__+')', \
              self.test_categories_table_created.__doc__
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query1 = 'SELECT * FROM categories'
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
            categories = cur.fetchall()
            #Assert
            self.assertEquals(len(categories), self.initial_size)
        if con:
            con.close()

    def test_create_categories_object(self):
        '''
        Check that the method create_categories_object works return adequate values
        for the first database row.
        '''
        print '('+self.test_create_categories_object.__name__+')', \
              self.test_create_categories_object.__doc__
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM categories'
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
            category = db._create_categories_object(row)
            self.assertDictContainsSubset(category, self.category1)

    def test_get_categories(self):
        '''
        Test get_categories
        '''
        print '('+self.test_get_categories.__name__+')', \
              self.test_get_categories.__doc__
        #Test with existing categories
        categories = db.get_categories()
        self.assertDictContainsSubset(categories, self.categories)

    def test_create_category(self):
        '''
        Test that I can add new categories
        '''
        print '('+self.test_create_category.__name__+')', \
              self.test_create_category.__doc__
        category_id = db.create_category(self.new_category1_name, self.new_category1_description)
        self.assertIsNotNone(category_id)

        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM categories \
                          WHERE category_id = ?'
        #Connects to the database.
        con = sqlite3.connect(db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement        
            pvalue = (category_id,)
            cur.execute(query, pvalue)
            #Extrac the row
            row = cur.fetchone()
            #Test the method
            new_category_name = row['name']
            new_category_description = row['description']
            self.assertDictContainsSubset(category_id, self.new_category1['id'])
            self.assertDictContainsSubset(new_category_name, self.new_category1['name'])
            self.assertDictContainsSubset(new_category_description, self.new_category1['description'])
    
    def test_create_existing_category(self):
        '''
        Test that I cannot add two categories with the same name
        '''
        print '('+self.test_create_existing_category.__name__+')', \
              self.test_create_existing_category.__doc__
        category_id = db.create_category(self.new_category1_name, self.new_category1_description)
        self.assertIsNone(category_id)

    def test_create_category_without_description(self):
        '''
        Test that I can add new categories without description
        '''
        print '('+self.test_create_category_without_description.__name__+')', \
              self.test_create_category_without_description.__doc__

        category_id = db.create_category(self.new_category2_name, null)
        self.assertIsNotNone(category_id)

        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM categories \
                          WHERE category_id = ?'
        #Connects to the database.
        con = sqlite3.connect(db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement        
            pvalue = (category_id,)
            cur.execute(query, pvalue)
            #Extrac the row
            row = cur.fetchone()
            #Test the method
            new_category_name = row['name']
            new_category_description = row['description']
            self.assertDictContainsSubset(category_id, self.new_category2['id'])
            self.assertDictContainsSubset(new_category_name, self.new_category2['name'])
            self.assertDictContainsSubset(new_category_description, self.new_category2['description'])

if __name__ == '__main__':
    print 'Start running tests'
    unittest.main()
