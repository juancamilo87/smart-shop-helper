import json

from flask import Flask, request, Response, g, jsonify
from flask.ext.restful import Resource, Api, abort
from werkzeug.exceptions import NotFound,  UnsupportedMediaType
from geopy.distance import vincenty

from utils import RegexConverter
import database

from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper


def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            print('got here3')
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                print('got options')
                resp = current_app.make_default_options_response()
            else:
                print('got options2')
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                print('got her2e')
                return resp

            h = resp.headers
            print('got here')
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator


DEFAULT_DB_PATH = 'db/shop.db'

#Constants for hypermedia formats and profiles
COLLECTIONJSON = "application/vnd.collection+json"
HAL = "application/hal+json"
FORUM_USER_PROFILE = "http://atlassian.virtues.fi:8090/display/PWP/Exercise+3#Exercise3-Forum_User"
FORUM_MESSAGE_PROFILE = "http://atlassian.virtues.fi:8090/display/PWP/Exercise+3#Exercise3-Forum_Message"
ATOM_THREAD_PROFILE = "https://tools.ietf.org/html/rfc4685"

days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

#Define the application and the api
app = Flask(__name__)
app.debug = True
#Set the database API. Change the DATABASE value from app.config to modify the
#database to be used (for instance for testing)
app.config.update({'DATABASE':database.ShopDatabase(DEFAULT_DB_PATH)})
#Start the RESTful API.
api = Api(app)


def create_error_response(status_code, title, message, resource_type=None):
    response = jsonify(title=title, message=message, resource_type=resource_type)
    response.status_code = status_code
    return response

@app.errorhandler(404)
def resource_not_found(error):
    return create_error_response(404, "Resource not found", "This resource url does not exit")

@app.errorhandler(500)
def unknown_error(error):
    return create_error_response(500, "Error", "The system has failed. Please, contact the administrator")

@app.before_request
def set_database():
    '''Stores an instance of the database API before each request in the flas.g
    variable accessible only from the application context'''
    g.db = app.config['DATABASE']


#Define the resources
class Item(Resource):

    def get(self, item_id):

        item_db = g.db.get_item(item_id)

        if(item_db is None or not item_db):
            return create_error_response(404,"No Item", "The Item is not in the system")

        theItem = {}
        category_db = g.db.get_category(item_db['category_id'])
        theItem['category'] = category_db['name']
        theItem['name'] = item_db['name']
        theItem['description'] = item_db['description']
        theItem['item_id'] = 'itm-'+str(item_db['id'])
        theItem['prices_uri'] = api.url_for(ItemPriceList,item_id=theItem['item_id'])

        return Response(json.dumps(theItem), status=200)
    

    def put(self, item_id):
        #CHECK THAT MESSAGE EXISTS

        item_db = g.db.get_item(item_id)

        if(item_db is None or not item_db):
            return create_error_response(404,"No Item", "The Item is not in the system")
        


        #PARSE THE REQUEST
        #Extract the request body. In general would be request.data
        #Since the request is JSON I use request.get_json
        #get_json returns a python dictionary after serializing the request body
        #get_json returns None if the body of the request is not formatted
        # using JSON
        input = request.get_json(force=True)
        if(input is None):
            return create_error_response(415, "Unsupported Media Type",
                                     "Use a JSON compatible format",
                                     "Item")

        #It throws a BadRequest exception, and hence a 400 code if the JSON is 
        #not wellformed
        try: 
            price = input['price']
            store_id = input['store_id']
            if not price or not store_id:
                abort(400)

            store_db = g.db.get_store(store_id)
            if(store_db is None or not store_db):
                return create_error_response(400,"No Store", "The Store is not in the system")

            price_id = g.db.update_price(price,item_id,store_id)

            if not g.db.update_price(price,item_id,store_id):
                abort(400)

            response = {}
            response['item_uri'] = api.url_for(Item,item_id=item_id)
            response['prices_uri'] = api.url_for(ItemPriceList,item_id=item_id)

            return Response(json.dumps(response), status=200)
            
            #CHECK THAT DATA RECEIVED IS CORRECT
            
        except: 
            #This is launched if either title or body does not exist or the 
            #template.data is not there. 

            abort(400)
   
    @crossdomain(origin='*')
    def delete(self, item_id):

        if g.db.delete_item(item_id):
            return '', 200
        else:
            #Send error message
            return create_error_response(404,"No Item","The Item is not in the system")
    
    @crossdomain(origin='*')
    def options(self, item_id):
        return item_id


class ItemList(Resource):
    @crossdomain(origin='*')
    def get(self):

        categories_db = g.db.get_categories()

        if(categories_db is None or not categories_db):
            return create_error_response(204,"No Categories", "There are no categories in the system")

        collection = []
        for category in categories_db:
            theCategory = {}
            theCategory['category'] = category['name']
            item_collection = []
            category_id = category['id']
            items_db = g.db.get_items(category_id)
            for item in items_db:
                theItem = {}
                theItem['name'] = item['name']
                item_id = item['id']
                theItem['item_uri'] = api.url_for(Item, item_id='itm-'+str(item_id))
                item_collection.append(theItem)

            theCategory['items'] = item_collection
            collection.append(theCategory)

        return Response(json.dumps(collection), status=200)

        
    def post(self):


        input = request.get_json(force=True)
        if(input is None):
            return create_error_response(415, "Unsupported Media Type",
                                     "Use a JSON compatible format",
                                     "ItemList")

        #It throws a BadRequest exception, and hence a 400 code if the JSON is 
        #not wellformed
        try: 
            category = input['category']
            name = input['name']
            description = input['description']

            if not category or not name or not description:
                abort(400)

            category_db = g.db.get_category_by_name(category)
            print('fds')
            if(category_db is None):
                category_id = g.db.create_category(category)
            else:
                category_id = category_db['id']

            item_id = g.db.create_item(name, category_id, description)
            if(item_id is None):
                abort(400)

            result = {}
            result['item_uri'] = api.url_for(Item,item_id='itm-'+str(item_id))
            result['prices_uri'] = api.url_for(ItemPriceList,item_id='itm-'+str(item_id))
            
            return Response(json.dumps(result), status=200)
            
            #CHECK THAT DATA RECEIVED IS CORRECT
            
        except: 
            #This is launched if either title or body does not exist or the 
            #template.data is not there. 
            abort(400)

class ItemPriceList(Resource): 
    @crossdomain(origin='*')
    def get(self, item_id):
        '''
        Get a the item price list in the system with id item_id.

        INPUT parameters:
          None

        OUTPUT: 
         * Media type: Collection+JSON: 
             http://amundsen.com/media-types/collection/
           - Extensions: template validation and value-types
             https://github.com/collection-json/extensions
         * Profile: Forum_Message
           http://atlassian.virtues.fi:8090/display/PWP
           /Exercise+3#Exercise3-Forum_Message

        Link relations used in items: None
        Semantic descriptions used in items: headline
        Link relations used in links: users-all
        Semantic descriptors used in template: headline, articleBody, author, 
        editor.

        NOTE: 
        Now articleBody links to the column body in the database
        Now headline links to the column title in the database
        Now author links to the column sender in the database.

        '''

        #Extract messages from database
        price_db = g.db.get_prices(item_id)


        if(price_db is None):
            return create_error_response(204,"No Prices", "The Item has no prices in the system")
        if(not price_db):
            return create_error_response(404,"No Item", "The Item does not exist in the system")
        #FILTER AND GENERATE RESPONSE
        price_list = []
        
        for price in price_db: 
            the_price = {}
            the_price['price'] = price['value']
            the_price['timestamp'] = price['timestamp']
            store_id = price['store_id']
            the_price['store_uri'] = api.url_for(Store, store_id='str-'+str(store_id))
            price_list.append(the_price)

        
        return Response(json.dumps(price_list), status=200)
        
class Store(Resource):
    @crossdomain(origin='*')
    def get(self, store_id):
        '''
        Get a store in the system with id store_id.

        INPUT parameters:
          None

        OUTPUT: 
         * Media type: Collection+JSON: 
             http://amundsen.com/media-types/collection/
           - Extensions: template validation and value-types
             https://github.com/collection-json/extensions
         * Profile: Forum_Message
           http://atlassian.virtues.fi:8090/display/PWP
           /Exercise+3#Exercise3-Forum_Message

        Link relations used in items: None
        Semantic descriptions used in items: headline
        Link relations used in links: users-all
        Semantic descriptors used in template: headline, articleBody, author, 
        editor.

        NOTE: 
        Now articleBody links to the column body in the database
        Now headline links to the column title in the database
        Now author links to the column sender in the database.

        '''

        #Extract messages from database
        store_db = g.db.get_store(store_id)


        if(store_db is None or not store_db):
            return create_error_response(404,"No Store", "The Store does not exist in the system")
        #FILTER AND GENERATE RESPONSE




        envelope = {}
        theStore = {}
        theStore['name'] = store_db['name']
        theStore['address'] = store_db['address']
        theStore['latitude'] = store_db['latitude']
        theStore['longitude'] = store_db['longitude']
        theStore['store_id'] = "str-"+str(store_db['id'])
        schedule_id = store_db['schedule_id']
        schedule_db = g.db.get_schedule(schedule_id)
        day_ids = []
        day_ids.append(schedule_db['monday_id'])
        day_ids.append(schedule_db['tuesday_id'])
        day_ids.append(schedule_db['wednesday_id'])
        day_ids.append(schedule_db['thursday_id'])
        day_ids.append(schedule_db['friday_id'])
        day_ids.append(schedule_db['saturday_id'])
        day_ids.append(schedule_db['sunday_id'])
        schedule = {}
        theStore['schedule'] = schedule

        i = 0
        for day_id in day_ids:
            time_db = g.db.get_time(day_id)
            time = {}
            time['opening'] = time_db['open']
            time['closing'] = time_db['close']
            schedule[days[i]] = time
            i = i + 1

        envelope['store'] = theStore
        
        return Response(json.dumps(envelope), status=200)
        

    def put(self, store_id):

        input = request.get_json(force=True)
        if(input is None):
            return create_error_response(415, "Unsupported Media Type",
                                     "Use a JSON compatible format",
                                     "Store")
        store_db = g.db.get_store(store_id)

        if store_db is None or not store_db:
            return create_error_response(404, "No Store",
                                     "The Store is not in the system",
                                     "Store")

        try: 
            schedule = {}

            error_response = []
            for day in days:

                times = input[day]
                if not times:
                    error = {}
                    error['day'] = day
                    error_response.append(error)
                else:
                    open = times['opening']
                    close = times['closing']
                    if not open or not close:
                        error = {}
                        error['day'] = day
                        error_response.append(error)
                    else:
                        if open <-1 or open > 24 or close < -1 or close > 24:
                            error = {}
                            error['day'] = day
                            error_response.append(error)
                        else:
                            day_read = {}
                            day_read['open'] = open
                            day_read[ 'close'] = close
                            schedule[day] = day_read
            schedule_ids = []
            if not error_response:
                for day in days:

                    theDay = schedule[day]
                    
                    open = theDay['open']
                    close = theDay['close']
                    time_id = g.db.get_time_from_details(open, close)
                    if time_id is None:
                        time_id = g.db.create_time(open, close)

                    schedule_ids.append(time_id)

                schedule_id = g.db.get_schedule_from_details(schedule_ids[0], schedule_ids[1],schedule_ids[2], schedule_ids[3],schedule_ids[4], schedule_ids[5],schedule_ids[6])

                if schedule_id is None:
                    schedule_id = g.db.create_schedule(schedule_ids[0], schedule_ids[1],schedule_ids[2], schedule_ids[3],schedule_ids[4], schedule_ids[5],schedule_ids[6])

                g.db.update_store_schedule(store_id, schedule_id)
                
                result = {}
                result['store_uri'] = api.url_for(Store,store_id=store_id)

                return Response(json.dumps(result), status=200)

            else:
                return Response(json.dumps(error_response), status=400)

        except: 
            abort(400)

    def delete(self, store_id):
        
        if g.db.delete_store(store_id):
            return '', 200
        else:
            #Send error message
            return create_error_response(404,"No Store","The Store is not in the system")

class StoreList(Resource):
    '''
    Resource StoreList implementation
    '''
    @crossdomain(origin='*')
    def get(self):
        '''
        Get all stores in the system.

        INPUT parameters:
          None

        OUTPUT: 
         * Media type: Collection+JSON: 
             http://amundsen.com/media-types/collection/
           - Extensions: template validation and value-types
             https://github.com/collection-json/extensions
         * Profile: Forum_Message
           http://atlassian.virtues.fi:8090/display/PWP
           /Exercise+3#Exercise3-Forum_Message

        Link relations used in items: None
        Semantic descriptions used in items: headline
        Link relations used in links: users-all
        Semantic descriptors used in template: headline, articleBody, author, 
        editor.

        NOTE: 
        Now articleBody links to the column body in the database
        Now headline links to the column title in the database
        Now author links to the column sender in the database.

        '''

        parameters = request.args
        radius = int(parameters.get('radius', -1))
        latitude = float(parameters.get('latitude', -1))
        longitude = float(parameters.get('longitude', -1))
        #Extract messages from database
        stores_db = g.db.get_stores()

        #FILTER AND GENERATE RESPONSE

        #Create the envelope
        envelope = {}
        collection = {}
        envelope["collection"] = collection
        #Create the items
        stores = []
        for store in stores_db: 
            print("Error")
            _store_id = store['id']
            _latitude = store['latitude']
            _longitude = store['longitude']
            _url = api.url_for(Store, store_id="str-"+str(_store_id))

            current = (latitude, longitude)
            store_location = (_latitude, _longitude)
            distance = vincenty(current, store_location).kilometers
            
            new_store = {}
            new_store['href'] = _url
            new_store['distance'] = distance
            if distance <= radius:
                stores.append(new_store)

        collection['stores'] = stores
        
        if len(stores) > 0:
            return Response(json.dumps(collection), status=200)
        else:
            return Response(status=204)

        

    def post(self):

        input = request.get_json(force=True)
        if(input is None):
            return create_error_response(415, "Unsupported Media Type",
                                     "Use a JSON compatible format",
                                     "StoreList")
        
        try: 
            json_schedule = input['schedule']

            if not json_schedule:
                abort(400)
            print('fds')
            schedule = {}
            error_response = []
            for day in days:
                times = json_schedule[day]
                if not times:
                    error = {}
                    error['day'] = day
                    error_response.append(error)
                else:
                    open = times['opening']
                    close = times['closing']
                    if not open or not close:
                        error = {}
                        error['day'] = day
                        error_response.append(error)
                    else:
                        if open <-1 or open > 24 or close < -1 or close > 24:
                            error = {}
                            error['day'] = day
                            error_response.append(error)
                        else:
                            day_read = {}
                            day_read['open'] = open
                            day_read[ 'close'] = close
                            schedule[day] = day_read
            schedule_ids = []
            if not error_response:
                for day in days:
                    theDay = schedule[day]
                    open = theDay['open']
                    close = theDay['close']
                    time_id = g.db.get_time_from_details(open, close)
                    if time_id is None:
                        time_id = g.db.create_time(open, close)

                    schedule_ids.append(time_id)

                schedule_id = g.db.get_schedule_from_details(schedule_ids[0], schedule_ids[1],schedule_ids[2], schedule_ids[3],schedule_ids[4], schedule_ids[5],schedule_ids[6])

                if schedule_id is None:
                    schedule_id = g.db.create_schedule(schedule_ids[0], schedule_ids[1],schedule_ids[2], schedule_ids[3],schedule_ids[4], schedule_ids[5], schedule_ids[6])
                
                print(schedule_id)
                
                name = input['name']
                address = input['address']
                latitude = input['latitude']
                longitude = input['longitude']

                if not name or not address or not latitude or not longitude:
                    abort(400)
                print('fds')
                store_id = g.db.create_store(name, address, latitude, longitude, schedule_id)

                if store_id is None or not store_id:
                    abort(400)
                print('fds')
                result = {}
                result['store_uri'] = api.url_for(Store,store_id="str-"+str(store_id))
                return Response(json.dumps(result), status=200)

            else:
                return Response(json.dumps(error_response), status=400)

        except: 
            abort(400)


#Add the Regex Converter so we can use regex expressions when we define the
#routes
app.url_map.converters['regex'] = RegexConverter


#Define the routes
api.add_resource(Item, '/shop/api/items/<regex("itm-\d{1,}"):item_id>/',
                 endpoint='item')
api.add_resource(ItemList, '/shop/api/items/',
                 endpoint='item_list')
api.add_resource(ItemPriceList, '/shop/api/items/<regex("itm-\d{1,}"):item_id>/pricelist/',
                 endpoint='item_price_list')
api.add_resource(Store, '/shop/api/stores/<regex("str-\d{1,}"):store_id>/',
                 endpoint='store')
api.add_resource(StoreList, '/shop/api/stores/',
                 endpoint='store_list')

#Start the application
#DATABASE SHOULD HAVE BEEN POPULATED PREVIOUSLY
if __name__ == '__main__':
    #Debug True activates automatic code reloading and improved error messages
    #app.run(debug=True)
    app.run(host='0.0.0.0')
