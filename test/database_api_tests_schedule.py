import sqlite3, unittest

from .database_api_tests_common import BaseTestCase, db, db_path

class ScheduleDbAPITestCase(BaseTestCase):
    '''
            The format of the Schedule dictionary is the following:
            {
            'id':,
            'monday_id':,
            'tuesday_id':,
            'wednesday_id':,
             'thursday_id':,
             'friday_id':,
             'saturday_id':,
             'sunday_id':
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
    #the strip function removes the tabs generated.
    schedule1_monday_id = 1
    schedule1_tuesday_id = 1
    schedule1_wednesday_id = 1
    schedule1_thursday_id = 1
    schedule1_friday_id = 1
    schedule1_saturday_id = 2
    schedule1_sunday_id = 2
    schedule1_id = 1
    schedule1 = {
                    'id':schedule1_id,
                    'monday_id':schedule1_monday_id,
                    'tuesday_id':schedule1_tuesday_id,
                    'wednesday_id':schedule1_wednesday_id,
                    'thursday_id':schedule1_thursday_id,
                    'friday_id':schedule1_friday_id,
                    'saturday_id':schedule1_saturday_id,
                    'sunday_id':schedule1_sunday_id
                }

    schedule2_monday_id = 1
    schedule2_tuesday_id = 1
    schedule2_wednesday_id = 1
    schedule2_thursday_id = 1
    schedule2_friday_id = 2
    schedule2_saturday_id = 2
    schedule2_sunday_id = 2
    schedule2_id = 2
    schedule2 = {
                    'id':schedule2_id,
                    'monday_id':schedule2_monday_id,
                    'tuesday_id':schedule2_tuesday_id,
                    'wednesday_id':schedule2_wednesday_id,
                    'thursday_id':schedule2_thursday_id,
                    'friday_id':schedule2_friday_id,
                    'saturday_id':schedule2_saturday_id,
                    'sunday_id':schedule2_sunday_id
                }

    new_schedule1_monday_id = 1
    new_schedule1_tuesday_id = 1
    new_schedule1_wednesday_id = 1
    new_schedule1_thursday_id = 2
    new_schedule1_friday_id = 1
    new_schedule1_saturday_id = 2
    new_schedule1_sunday_id = 2
    new_schedule1_id = 3
    new_schedule1 = {
                    'id':new_schedule1_id,
                    'monday_id':new_schedule1_monday_id,
                    'tuesday_id':new_schedule1_tuesday_id,
                    'wednesday_id':new_schedule1_wednesday_id,
                    'thursday_id':new_schedule1_thursday_id,
                    'friday_id':new_schedule1_friday_id,
                    'saturday_id':new_schedule1_saturday_id,
                    'sunday_id':new_schedule1_sunday_id
                    }

    new_schedule2_monday_id = 1
    new_schedule2_tuesday_id = 5
    new_schedule2_wednesday_id = 1
    new_schedule2_thursday_id = 2
    new_schedule2_friday_id = 1
    new_schedule2_saturday_id = 2
    new_schedule2_sunday_id = 2

    initial_size = 2
 
    @classmethod
    def setUpClass(cls):
        print "Testing ", cls.__name__

    def test_schedules_table_created(self):
        '''
        Checks that the table initially contains 2 schedules (check 
        shop_data_dump.sql)
        '''
        print '('+self.test_schedules_table_created.__name__+')', \
              self.test_schedules_table_created.__doc__
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query1 = 'SELECT * FROM schedules'
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
            schedules = cur.fetchall()
            #Assert
            self.assertEquals(len(schedules), self.initial_size)
        if con:
            con.close()

    def test_create_schedules_object(self):
        '''
        Check that the method create_shedules_object works return adequate values
        for the first database row.
        '''
        print '('+self.test_create_schedules_object.__name__+')', \
              self.test_create_schedules_object.__doc__
        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM schedules'
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
            schedule = db._create_schedule_object(row)
            self.assertDictContainsSubset(schedule, self.schedule1)

    def test_get_schedule(self):
        '''
        Test get_schedule
        '''
        print '('+self.test_get_schedule.__name__+')', \
              self.test_get_schedule.__doc__
        #Test with existing schedules
        schedule = db.get_schedule(self.schedule2_id)
        self.assertDictContainsSubset(schedule, self.schedule2)

    def test_create_schedule(self):
        '''
        Test that I can add new schedules
        '''
        print '('+self.test_create_schedule.__name__+')', \
              self.test_create_schedule.__doc__
        schedule_id = db.create_schedule(self.new_schedule1_monday_id, \
                                         self.new_schedule1_tuesday_id, \
                                         self.new_schedule1_wednesday_id, \
                                         self.new_schedule1_thursday_id, \
                                         self.new_schedule1_friday_id, \
                                         self.new_schedule1_saturday_id, \
                                         self.new_schedule1_sunday_id)
        self.assertIsNotNone(schedule_id)

        #Create the SQL Statement
        keys_on = 'PRAGMA foreign_keys = ON'
        query = 'SELECT * FROM schedules \
                          WHERE schedule_id = ?'
        #Connects to the database.
        con = sqlite3.connect(db_path)
        with con:
            #Cursor and row initialization
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            #Provide support for foreign keys
            cur.execute(keys_on)
            #Execute main SQL Statement        
            pvalue = (schedule_id,)
            cur.execute(query, pvalue)
            #Extrac the row
            row = cur.fetchone()
            #Test the method
            new_schedule_monday_id = row['monday_id']
            new_schedule_tuesday_id = row['tuesday_id']
            new_schedule_wednesday_id = row['wednesday_id']
            new_schedule_thursday_id = row['thursday_id']
            new_schedule_friday_id = row['friday_id']
            new_schedule_saturday_id = row['saturday_id']
            new_schedule_sunday_id = row['sunday_id']
            self.assertEquals(schedule_id, self.new_schedule1['id'])
            self.assertEquals(new_schedule_monday_id, self.new_schedule1['monday_id'])
            self.assertEquals(new_schedule_tuesday_id, self.new_schedule1['tuesday_id'])
            self.assertEquals(new_schedule_wednesday_id, self.new_schedule1['wednesday_id'])
            self.assertEquals(new_schedule_thursday_id, self.new_schedule1['thursday_id'])
            self.assertEquals(new_schedule_friday_id, self.new_schedule1['friday_id'])
            self.assertEquals(new_schedule_saturday_id, self.new_schedule1['saturday_id'])
            self.assertEquals(new_schedule_sunday_id, self.new_schedule1['sunday_id'])
    
    def test_create_existing_schedule(self):
        '''
        Test that I cannot add two schedules with the same time ids
        '''
        print '('+self.test_create_existing_schedule.__name__+')', \
              self.test_create_existing_schedule.__doc__
        
        with self.assertRaises(sqlite3.IntegrityError):
            db.create_schedule(self.schedule1_monday_id, \
                                         self.schedule1_tuesday_id, \
                                         self.schedule1_wednesday_id, \
                                         self.schedule1_thursday_id, \
                                         self.schedule1_friday_id, \
                                         self.schedule1_saturday_id, \
                                         self.schedule1_sunday_id)

    def test_create_schedule_with_nonexisting_time(self):
        '''
        Test that I can not add new schedules of nonexisting time
        tuesday_id = '5'
        '''
        print '('+self.test_create_schedule_with_nonexisting_time.__name__+')', \
              self.test_create_schedule_with_nonexisting_time.__doc__

        
        with self.assertRaises(ValueError):
            db.create_schedule(self.new_schedule2_monday_id, \
                               self.new_schedule2_tuesday_id, \
                               self.new_schedule2_wednesday_id, \
                               self.new_schedule2_thursday_id, \
                               self.new_schedule2_friday_id, \
                               self.new_schedule2_saturday_id, \
                               self.new_schedule2_sunday_id)

if __name__ == '__main__':
    print 'Start running tests'
    unittest.main()
