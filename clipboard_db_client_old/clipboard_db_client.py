from pymongo import MongoClient, errors, ASCENDING
from flask_pymongo import PyMongo
from flask import Flask, request, jsonify, Response, make_response
from db_locks import UpdateLock, QueryLock
from bson import json_util, ObjectId, BSON
from bson.json_util import dumps
from datetime import datetime
from clipboardcommonlib import shared_config
import uuid
import json
import time
import os
import sys
import itertools

def get_env_var(name):
    try:
        return os.environ[name]
    except KeyError:
        print('Error: {0} not set. If this value was recently set, close all python processes and try again'.format(name))
        sys.exit(1)

config = shared_config.Config()
app = Flask(__name__)
#date_format = '%Y-%m-%d'
#time_format = '%H:%M'
#mongo_ip = 'clipboard_db' if db_client_ip == 'clipboard_db_client' else get_env_var('DOCKER_IP')
#mongo_port = 27017

app.config['MONGO_DBNAME'] = 'clipboard'
app.config['MONGO_URI'] = config.db_url

mongo = PyMongo(app)

def create_db():
    print('No configuration found for clipboard database. Creating...')
    mongo.db.create_collection('event')
    # TODO: Figure out if we should use a value besides ASCENDING
    mongo.db.event.create_index([('start_timestamp', ASCENDING), ('end_timestamp', ASCENDING), ('organization', ASCENDING)])
    print('Database creation successful')

def setup_db():
    print('Attempting to connect to MongoDB...')
    try:
        if not 'clipboard' in mongo.db.client.list_database_names():
            create_db()
        else:
            print('Connection successful')
    except errors.ServerSelectionTimeoutError as ex:
        print(f'Could not connect to MongoDB: {ex.args[0]}. Exiting.')
        sys.exit(1)

def date_from_timestamp(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime(config.display_date_format)

def time_from_timestamp(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime(config.display_time_format)

def transform_result(mongo_result):
    # _id objects can't be serialized to json, so use the str representation
    # also, change "_id" to "id"
    mongo_result['id'] = str(mongo_result.pop('_id'))
    start_timestamp = mongo_result.pop('start_timestamp')
    end_timestamp = mongo_result.pop('end_timestamp')
    mongo_result['start_time'] = time_from_timestamp(start_timestamp)
    mongo_result['start_date'] = date_from_timestamp(start_timestamp)
    mongo_result['end_time'] = time_from_timestamp(end_timestamp)
    mongo_result['end_date'] = date_from_timestamp(end_timestamp)

    return mongo_result

update_lock = UpdateLock()
query_lock = QueryLock()

@app.route('/status', methods=['GET'])
def status():
    # This is used to ping the service and wait for it to become available on startup
    return 'available', 200

@app.route('/putevents', methods=['POST'])
def put_events():
    events = mongo.db.event
    request_obj = request.get_json()
    if len(request_obj) == 0:
        return 'Error: request contains no data', 400
    try:
        organizations = list({ obj['organization'] for obj in request_obj })
    except KeyError:
        return 'One or more documents sent for insertion do not contain the "organization" property', 400
    with update_lock:
        query_lock.wait_for_clearance()
        
        query = {'organization' : {'$in': organizations }}
        events_to_delete = [event for event in events.find(query)]
        events.delete_many(query)
        try:
            # Using ordered=False may increase performance and we don't care about the order of inserts
            events.insert_many(request_obj, ordered=False)
        except Exception:
            #TODO: Make sure this exception is logged when we figure out a logging system
            inserted_events = [event for event in events.find(query)]
            if len(inserted_events) == 0 and len(events_to_delete) > 0:
                events.insert_many(events_to_delete)

        return 'success', 200
        

@app.route('/getevents', methods=['GET'])
def get_events():
    events = mongo.db.event
    update_lock.wait_for_clearance()
    with query_lock:
        args = request.args
        
        try:
            start_timestamp = int(args.get('start_timestamp'))
            end_timestamp = int(args.get('end_timestamp'))
            organization = args.get('organization')

            # Yo dawg, we heard you like json so we put json in your query language so you can query with json while you query for json
            and_clause = [ 
                    {
                        'start_timestamp': { 
                            '$gte': start_timestamp 
                        } 
                    }, 
                    { 
                        'end_timestamp': { 
                            '$lte': end_timestamp 
                        } 
                    }
                ]
            if organization != None and len(organization) > 0:
                and_clause.append({
                    'organization': {
                        '$eq': organization
                    }
                })
            
            result = events.find({ 
                '$and': and_clause
            })
            
            result_list = [transform_result(r) for r in result]
            
            return jsonify(result_list), 200
        except Exception as ex:
            print(ex)
            return jsonify(ex), 400

    

if __name__ == '__main__':
    app.debug = True
    with app.app_context():
        setup_db()
    app.run(host=config.db_client_ip, port=5000)