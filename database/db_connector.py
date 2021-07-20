# Based on flask starter app from https://github.com/osu-cs340-ecampus/flask-starter-app
# Required: 
# pip install flask-mysqldb
# pip install python-dotenv

import MySQLdb as MySQL
import os
from dotenv import load_dotenv, find_dotenv

# Find and locate .env file in root directory
load_dotenv(find_dotenv())

# Retrieve environmental variables from .env
host = os.environ.get("DB_HOST")
port = os.environ.get("DB_PORT")
user = os.environ.get("DB_USER")
pw = os.environ.get("DB_PW")
db = os.environ.get("DB_NAME")

# Connect to database
# Note: Disable Firewall or this may not work
def connect_to_db(host = host, port=port, user = user, pw = pw, db = db):
    db_connection = MySQL.connect(
        host = host, 
        port = int(port), 
        user = user,
        passwd = pw, 
        db = db
    )
    return db_connection

# Run query
def run_query(db_connection = None, query = None, query_params = ()):
    if db_connection is None:
        print("No connection to the database found!")
        return None

    if query is None or len(query.strip()) == 0:
        print("Error: Query is empty")
        return None

    # Create cursor to execute query
    cursor = db_connection.cursor(MySQL.cursors.DictCursor)
    # Execute query, query_params is tuple
    cursor.execute(query, query_params)
    # Save changes
    db_connection.commit()
    return cursor

if __name__ == '__main__':
    # Sample query 
    db = connect_to_db()
    query = "SELECT * from Animals;"
    results = run_query(db, query)
    print("Printing results of %s" % query)

    for r in results.fetchall():
        print(r)