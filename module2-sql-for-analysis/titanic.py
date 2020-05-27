import os
import psycopg2
from psycopg2.extras import DictCursor
from psycopg2.extras import execute_values
from dotenv import load_dotenv
import pandas as pd
import json
import numpy as np

load_dotenv() # reads the contents of the .env file and adds them to the environment

psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)

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

# Read passenger data from the csv file
CSV_FILEPATH = os.path.join(os.path.dirname(__file__), "titanic.csv")

df = pd.read_csv(CSV_FILEPATH)
print(df.head())


# Create a table to store the passengers
table_name = "passengers"

print("-------------------")
table_creation = f"""
CREATE TABLE  IF NOT EXISTS {table_name} (
    id SERIAL PRIMARY KEY,
    "survived" int4,
    "pclass" int4,
    "name" text,
    "sex" text,
    "age" int4,
    "sib_spouse_count" int4,
    "parent_child_count" int4,
    "fare" float8
);
"""



print("SQL:", table_creation)
cursor.execute(table_creation)

# breakpoint()

# Insert Data into the passengers table
    
list_of_tuples = list(df.to_records(index=False))
insertion_query = f"INSERT INTO {table_name} (survived, pclass, name, sex, age, sib_spouse_count, parent_child_count, fare) VALUES %s"
execute_values(cursor, insertion_query, list_of_tuples)

# ACTUALLY SAVE THE TRANSACTIONS

connection.commit()
cursor.close()
connection.close()
