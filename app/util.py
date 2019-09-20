#import mysql.connector
from sqlalchemy import create_engine
import pandas as pd
import os
import subprocess
import time

CONFIG = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'port': '3306',
    'database': 'production'
}

COMPOSE_PATH = os.path.dirname(os.path.dirname(__file__)) #the folder containing docker-compose.yml

def connect_db():
    """Connecting to the database and return the engine"""

    engine = create_engine('mysql+pymysql://{user}:{password}@{host}:{port}/{database}'
                               .format(**CONFIG))
    engine.table_names() #make sure the connection is successful
    return engine

def try_connection(max_try):
    """Try the connection for `max_try` number of times.
    Return if the connection is successful"""
    try_count = 0
    while try_count < max_try:
        try:
            connect_db()
            return True
        except:
            time.sleep(1)
            try_count += 1
    return False

def spin_up_db():
    """State the docker container for the database.
    Make sure it is running and connetable then return True, else False"""
    subprocess.call(["docker-compose", "up", "-d"], cwd=COMPOSE_PATH)
    time.sleep(10)
    return try_connection(10)

def stop_db():
    """Stop the database container without deleting the volumn"""
    subprocess.call(["docker-compose", "down"], cwd=COMPOSE_PATH)
    time.sleep(10)

def delete_db():
    """Stop the database container and delete the volumn"""
    subprocess.call(["docker-compose", "down", "-v"], cwd=COMPOSE_PATH)
    time.sleep(10)

def read_file(file_name):
    """Given the path of a file, it will be loaded and returned as DataFrame
    Duplicates of emails will be altomatically removed"""

    header = ['firstname','lastname','email']
    file = pd.read_csv(file_name,
                       usecols=header,
                       dtype={col: 'str' for col in header})[header]
    ## TODO: imprement loading csv by chunk for really big file
    ## TODO: check inout format (e.g. email is a valid email)
    return file.drop_duplicates(subset=['email']) #email need to be unique

def load_file_to_db(file, engine):
    """Load the given DataFame into the data base using the engine
    If table `users` does not exist, it will be created"""

    tables = engine.table_names()
    connection = engine.connect()
    if 'users' not in tables:
        connection.execute("CREATE TABLE users (firstname VARCHAR(255), lastname VARCHAR(255), email VARCHAR(225))")
                       #"CONSTRAINT username PRIMARY KEY (email)")
    sql = "INSERT INTO users (firstname, lastname, email) VALUES (%s, %s, %s)"
    for idx in range(file.shape[0]):
        row = file.iloc[idx]
        connection.execute(sql, [row.firstname, row.lastname, row.email])
    connection.close()

def look_up_from_db(item, value, engine):
    """Query and return the data matching the given `value` in the `item` field
    using the engine. Return as a DataFrame"""
    try:
        query = f"SELECT * FROM users WHERE {item} = '{value}'"
        df = pd.read_sql(query, con=engine)
        return df[['firstname','lastname','email']]
    except:
        return None
