import mysql.connector
import pandas as pd
import docker

server_config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'port': '3306',
    'database': 'production'
}

def start_db():
    pass

def read_file(file_name):
    header = ['firstname','lastname','email']
    file = pd.read_csv(file_name,
                       usecols=header,
                       dtype={col: 'str' for col in header})[header]
    return file.drop_duplicates(subset=['email']) #email need to be unique

def load_file_to_db(file, config=None):
    if config is None:
        config = server_config
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    if ('users',) not in tables:
        cursor.execute("CREATE TABLE users (firstname VARCHAR(255), lastname VARCHAR(255), email VARCHAR(225))"
                       "CONSTRAINT username PRIMARY KEY (email)")
    results = [{name: color} for (name, color) in cursor]
    sql = "INSERT INTO users (firstname, lastname, email) VALUES (%s, %s, %s)"
    for idx in range(file.shape[0]):
        row = file.iloc[idx]
        cursor.execute(sql, (row.firstname,row.lastname,row.email))
    cursor.close()
    connection.close()

def look_up_from_db(item, value, config=None):
    if config is None:
        config = server_config
    connection = mysql.connector.connect(**config)
    query = f"SELECT * FROM users WHERE {item} = '{value}''"
    df = pd.read_sql(query, con=connection)
    return df['firstname','lastname','email']
