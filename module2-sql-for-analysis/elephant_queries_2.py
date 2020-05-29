import os
import psycopg2
from psycopg2.extras import DictCursor
from psycopg2.extras import execute_values
from dotenv import load_dotenv
import pandas as pd
import json

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


#
# CREATE NEW TABLE
#

table_name = "test_table2"

print("-------------------")
query = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
  id SERIAL PRIMARY KEY,
  name varchar(40) NOT NULL,
  data JSONB
);
"""
print("SQL:", query)
cursor.execute(query)

#
# INSERT SOME DATA
#


insertion_query = f"INSERT INTO {table_name} (name, data) VALUES %s"

my_dict = { "a": 1, "b": ["dog", "cat", 42], "c": 'true' }

df = pd.DataFrame([
  ['A rowwwww', 'null'],
  ['Another row, with JSONNNNN', json.dumps(my_dict)],
  ['Third row', "null"],
  ["Pandas Row", "null"]
])

records = df.to_dict("records") 
list_of_tuples = [(r[0], r[1]) for r in records]

execute_values(cursor, insertion_query, list_of_tuples)

#
# QUERY THE TABLE
#

print("-------------------")
query = f"SELECT * FROM {table_name};"
print("SQL:", query)
cursor.execute(query)
for row in cursor.fetchall():
    print(row)

# ACTUALLY SAVE THE TRANSACTIONS
connection.commit()

cursor.close()
connection.close()
