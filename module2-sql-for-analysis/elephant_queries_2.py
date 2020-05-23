import os
import psycopg2
from psycopg2.extras import DictCursor
from dotenv import load_dotenv

load_dotenv() # reads the contents of the .env file and adds them to the envrionment

DB_NAME = os.getenv("DB_NAME", default = "Set the DB_NAME")
DB_USER = os.getenv("DB_USER", default = "Set the DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD", default = "Set the DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", default = "Set the DB_HOST")


### Connect to ElephantSQL-hosted PostgreSQL
connection = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST)
                        
print("CONNECTION", type(connection))

### A "cursor", a structure to iterate over db records to perform queries
cursor = connection.cursor(cursor_factory=DictCursor)
print("CURSOR", type(cursor))

### An example query
cursor.execute('SELECT * from test_table;')
### Note - nothing happened yet! We need to actually *fetch* from the cursor
result = cursor.fetchall()
for row in result:
    print("--------")
    print(type(row))
    print(row)