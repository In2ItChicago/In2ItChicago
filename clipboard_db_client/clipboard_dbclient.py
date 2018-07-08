from pymongo import MongoClient, errors, ASCENDING
from flask import Flask, request, jsonify, Response, make_response
from db_locks import UpdateLock, QueryLock
from bson import json_util, ObjectId, BSON
from bson.json_util import dumps
import uuid
import json
import time
import os
import sys
import itertools

app = Flask(__name__)
events = None

def get_env_var(name):
    try:
        return os.environ[name]
    except KeyError:
        print('Error: {0} not set. If this value was recently set, close all python processes and try again'.format(name))
        sys.exit(1)

db_client_ip = get_env_var('DB_CLIENT_IP')

try:
    print('Attempting to connect to MongoDB...')
    # 'clipboard_db' is the name of the database service in docker-config.yaml. This value will resolve to the IP given to the database by Docker
    mongo_ip = 'clipboard_db' if db_client_ip == '0.0.0.0' else get_env_var('DOCKER_IP')
    client = MongoClient(mongo_ip, 27017)
    clipboard_db = client.clipboard
    if not 'clipboard' in client.database_names():
        print('No configuration found for clipboard database. Creating...')
        clipboard_db.create_collection('event')
        # TODO: Figure out if we should use a value besides ASCENDING
        clipboard_db.event.create_index([('start_timestamp', ASCENDING), ('end_timestamp', ASCENDING), ('organization', ASCENDING)])
        print('Database creation successful')
    else:
        print('Connection successful')
    events = clipboard_db.event
except errors.ServerSelectionTimeoutError as ex:
    print(f'Could not connect to MongoDB: {ex.args[0]}. Exiting.')
    sys.exit(1)

update_lock = UpdateLock()
query_lock = QueryLock()

@app.route('/status', methods=['GET'])
def status():
    # This is used to ping the service and wait for it to become available on startup
    return 'available', 200

@app.route('/putevents', methods=['POST'])
def put_events():
    request_obj = request.get_json()
    if len(request_obj) == 0:
        return 'Error: request contains no data', 400
    try:
        organizations = list({ obj['organization'] for obj in request_obj })
    except KeyError:
        return 'One or more documents sent for insertion do not contain the "organization" property', 400
    with update_lock:
        query_lock.wait_for_clearance()
        events = clipboard_db.event

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
            
            result = clipboard_db.event.find({ 
                '$and': and_clause
            })
            
            result_list = [r for r in result]
            for r in result_list:
                # _id objects can't be serialized to json, so use the str representation
                r['_id'] = str(r['_id'])
            
            return jsonify(result_list), 200
        except Exception as ex:
            print(ex)
            return jsonify(ex), 400

    

if __name__ == '__main__':
    app.debug = True
    app.run(host=db_client_ip, port=5000)