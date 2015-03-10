import sqlite3, unittest

from .database_api_tests_common import BaseTestCase, db, db_path

class CategoryDbAPITestCase(BaseTestCase):
    '''
            The format of the Category dictionary is the following:
            {
            'id':,
            'name':'',
            'description':''
            }
            
            where:
             - id: unique identifier of the category
             - name: name of the category
             - description: description of the category
    '''
    #the strip function removes the tabs generated.
    category1_name = 'Milk'
    category1_id = 1
    category1_description = 'Categories of milk'
    category1 = {
                  'id':category1_id,
                  'name':category1_name,
                  'description':category1_description
                }

    category2_name = 'Fruit'
    category2_id = 2
    category2_description = 'Different kinds of fruit'
    category2 = {
                  'id':category2_id,
                  'name':category2_name,
                  'description':category2_description
                }


    categories = [category1, category2]

    new_category1_name = 'Chicken'
    new_category1_description = 'Different kinds of chicken'
    new_category1 = {
                    'id':3,
                    'name':new_category1_name,
                    'description':new_category1_description
                    }

    new_category2_name = 'Bread'
    new_category2 = {
                    'id':3,
                    'name':new_category2_name,
                    'description':None
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
        self.assertListEqual(categories, self.categories)

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
            self.assertEquals(category_id, self.new_category1['id'])
            self.assertEquals(new_category_name, self.new_category1['name'])
            self.assertEquals(new_category_description, self.new_category1['description'])
    
    def test_create_existing_category(self):
        '''
        Test that I cannot add two categories with the same name
        '''
        print '('+self.test_create_existing_category.__name__+')', \
              self.test_create_existing_category.__doc__
        with self.assertRaises(sqlite3.IntegrityError):
            db.create_category(self.category1_name, self.new_category1_description)

    def test_create_category_without_description(self):
        '''
        Test that I can add new categories without description
        '''
        print '('+self.test_create_category_without_description.__name__+')', \
              self.test_create_category_without_description.__doc__

        category_id = db.create_category(self.new_category2_name)
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
            self.assertEquals(category_id, self.new_category2['id'])
            self.assertEquals(new_category_name, self.new_category2['name'])
            self.assertEquals(new_category_description, self.new_category2['description'])

if __name__ == '__main__':
    print 'Start running tests'
    unittest.main()
