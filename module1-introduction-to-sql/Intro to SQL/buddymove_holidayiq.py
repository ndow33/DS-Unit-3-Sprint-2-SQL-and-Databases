import pandas as pd
import sqlite3

location = 'buddymove_holidayiq.csv'
df = pd.read_csv(location)
print(df.head())

conn = sqlite3.connect("buddymove_holidayiq.sqlite3")
print(conn)

# df.to_sql("review", conn) This line is commented out because we use it only once to create the database

c = conn.cursor()
print("CURSOR: ", c)

# How many rows
query = "SELECT count(Sports) as total_rows FROM review;"
total_rows = c.execute(query).fetchall()
print("Total Rows: ", total_rows)

# How many users reviewed 100+ nature and 100+ shopping?
query = "SELECT count(Sports) as nature_and_shopping FROM review WHERE (Nature >= 100) & (Shopping >= 100);"
nature_and_shopping = c.execute(query).fetchall()
print("Users who reviewed at least 100 Nature in the category also reviewed at least 100 in the Shopping category: ", nature_and_shopping)
