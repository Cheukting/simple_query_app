#import mysql.connector
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
import pandas as pd
import os
import subprocess
import time
import csv

CONFIG = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'port': '3306',
    'database': 'production'
}

DTYPE_MAP = {
    "float64": "FLOAT",
    "int64": "INT",
    "datetime64[ns]": "DATETIME",
    "object": "VARCHAR(255)",
}

COMPOSE_PATH = os.path.dirname(__file__) #the folder containing docker-compose.yml

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
    return try_connection(20)

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
    file = pd.read_csv(file_name)
    if "email" not in file.columns:
        raise ValueError("No email column in input file")
    ## TODO: imprement loading csv by chunk for really big file
    ## TODO: check inout format (e.g. email is a valid email)
    return file.drop_duplicates(subset=['email']) #email need to be unique

def load_file_to_db(file, engine, name="users"):
    """Load the given DataFame into the data base using the engine
    If table `name` does not exist, it will be created"""

    tables = engine.table_names()
    connection = engine.connect()
    if name not in tables:
        column_string = ", ".join([f"{col_name} {DTYPE_MAP[str(dtype)]}" for col_name, dtype in file.dtypes.items()])
        connection.execute(f"CREATE TABLE {name} ({column_string},"
                           "UNIQUE KEY unique_email (email))")
    sql = f"INSERT INTO {name} ({', '.join([col_name for col_name in file.columns])}) " \
          f"VALUES ({', '.join(['%s' for col_name in file.columns])})"
    duplicate_idx = []
    for idx in range(file.shape[0]):
        row = file.iloc[idx]
        try:
            connection.execute(sql, [val.item() if not isinstance(val, str) else val for val in row])
        except IntegrityError:
            duplicate_idx.append(idx)
    connection.close()
    return duplicate_idx

def look_up_from_db(item, value, engine, table):
    """Query and return the data matching the given `value` in the `item` field
    using the engine. Return as a DataFrame"""
    try:
        query = f"SELECT * FROM {table} WHERE {item} = '{value}'"
        df = pd.read_sql(query, con=engine)
        return df
    except:
        return None
