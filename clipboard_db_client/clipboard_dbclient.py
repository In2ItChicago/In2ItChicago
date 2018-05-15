from couchbase.cluster import Cluster, PasswordAuthenticator
from couchbase.n1ql import N1QLQuery
from couchbase.exceptions import ArgumentError, CouchbaseNetworkError
from flask import Flask, request, jsonify
import uuid
import json
import time
import os
import sys

app = Flask(__name__)
bucket = None

def get_env_var(name):
    try:
        return os.environ[name]
    except KeyError:
        print('Error: {0} not set. If this value was recently set, close all python processes and try again'.format(name))
        sys.exit(1)

num_retries = 10
docker_ip = get_env_var('DOCKER_IP')
db_client_ip = get_env_var('DB_CLIENT_IP')

connection_string = 'couchbase://' + docker_ip
print('Couchbase connection string is ' + connection_string)
# It takes a while for couchbase to accept incoming connections, so give it several tries
for _ in range(num_retries):
    try:
        print('Attempting to connect to couchbase...')
        cluster = Cluster(connection_string)
        cluster.authenticate(PasswordAuthenticator('admin', 'clipboard'))
        bucket = cluster.open_bucket('event')
        break
    except CouchbaseNetworkError:
        time.sleep(5)
if bucket == None:
    print('Could not connect to couchbase. Exiting.')
    sys.exit(1)
else:
    print('Connection successful')

@app.route('/putevents', methods=['POST'])
def put_events():
    request_obj = request.get_json()
    try:
        data = bucket.insert_multi({str(uuid.uuid4()): val for val in request_obj})
        errors = [value.errstr for value in data.values() if not value.success]
        if len(errors) > 0:
            return jsonify(errors), 500
        return 'success', 200
    except ArgumentError as ex:
        return jsonify(ex.message), 400

@app.route('/getevents', methods=['GET'])
def get_events():
    args = request.args
    
    try:
        query = N1QLQuery('''
            SELECT
                address,
                category,
                description,
                start_timestamp,
                end_timestamp,
                organization,
                price,
                title,
                url
            FROM event 
            WHERE start_timestamp >= $start_timestamp
            AND end_timestamp <= $end_timestamp
            AND (organization = $organization OR $organization = "")''',
            start_timestamp=int(args.get('start_timestamp')),
            end_timestamp=int(args.get('end_timestamp')),
            organization=args.get('organization', ''))
        
        result = bucket.n1ql_query(query)
        #for row in result:
        #    print(row)
        return jsonify([row for row in result]), 200
    except ValueError as v:
        return jsonify(v.args[0]), 400

    

if __name__ == '__main__':
    app.debug = True
    app.run(host=db_client_ip, port=5000)