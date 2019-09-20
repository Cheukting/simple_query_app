#import mysql.connector
from sqlalchemy import create_engine
import pandas as pd
import docker

server_config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'port': '3306',
    'database': 'production'
}

def connect_db():
    engine = create_engine('mysql+pymysql://{user}:{password}@{host}:{port}/{database}'
                               .format(**server_config))
    return engine

def read_file(file_name):
    header = ['firstname','lastname','email']
    file = pd.read_csv(file_name,
                       usecols=header,
                       dtype={col: 'str' for col in header})[header]
    return file.drop_duplicates(subset=['email']) #email need to be unique

def load_file_to_db(file, engine):
    #connection = create_engine('mysql+pymysql://{user}:{password}@{host}:{port}/{database}'
    #                           .format(**server_config)).connect()
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
    #connection = create_engine('mysql+pymysql://{user}:{password}@{host}:{port}/{database}'
    #                           .format(**server_config)).connect()
    query = f"SELECT * FROM users WHERE {item} = '{value}'"
    df = pd.read_sql(query, con=engine)
    return df[['firstname','lastname','email']]
