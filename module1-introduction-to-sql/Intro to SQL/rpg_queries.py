import os
import sqlite3

# construct a path to wherever your database exists
# DB_FILEPATH = "chinook.db"
# DB_FILEPATH = os.path.join(os.path.dirname(__file__), "..", "rpg_db.sqlite3")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "rpg_db.sqlite3")
# with sqlite3.connect(db_path) as db:


print(os.getcwd())

connection = sqlite3.connect(db_path)
print("CONNECTION:", connection)

cursor = connection.cursor()
print("CURSOR", cursor)
# How many total Characters are there?
query = "SELECT count(distinct character_id) as character_count FROM charactercreator_character;"
total_characters = cursor.execute(query).fetchall()
print("Total Characters: ", total_characters)

# How many of each specific subclass?
# Clerics
query = "SELECT count(distinct character_ptr_id) as cleric_count FROM charactercreator_cleric;"
total_clerics = cursor.execute(query).fetchall()
print("Total Clerics: ", total_clerics)

# Fighters
query = "SELECT count(distinct character_ptr_id) as fighter_count FROM charactercreator_fighter;"
total_fighters = cursor.execute(query).fetchall()
print("Total Fighters: ", total_fighters)

# Mages
query = "SELECT count(distinct character_ptr_id) as mage_count FROM charactercreator_mage;"
total_mage = cursor.execute(query).fetchall()
print("Total Mages: ", total_mage)

# Necromancers
query = "SELECT count(distinct mage_ptr_id) as necro_count FROM charactercreator_necromancer;"
total_necro = cursor.execute(query).fetchall()
print("Total Necromancers: ", total_necro)

# Thieves
query = "SELECT count(distinct character_ptr_id) as thief_count FROM charactercreator_thief;"
total_thief = cursor.execute(query).fetchall()
print("Total Thieves: ", total_thief)

# How many total items
query = "SELECT count(distinct item_id) as item_count FROM armory_item;"
total_items = cursor.execute(query).fetchall()
print("Total Items: ", total_items)

# How many of the Items are weapons? How many are not?
query = "SELECT count(distinct item_ptr_id) as weapon_count FROM armory_weapon;"
total_weapons = cursor.execute(query).fetchall()
print("Total Weapons: ", total_weapons)

# How many items does each character have?
query = "SELECT character_id,count(distinct item_id) as items_per_character FROM charactercreator_character_inventory GROUP BY character_id LIMIT 20;"
items_per_character = cursor.execute(query).fetchall()
print("Items per Character: ", items_per_character)

# How many weapons does each character have?
query = "SELECT character_id,count(distinct item_id) as weapons_per_character FROM charactercreator_character_inventory WHERE item_id > 137 GROUP BY character_id LIMIT 20;"
weapons_per_character = cursor.execute(query).fetchall()
print("Weapons per Character: ", weapons_per_character)

# On average, how many items does each character have?
query = "SELECT AVG(items_per_character) as avg_items FROM (SELECT character_id,count(distinct item_id) as items_per_character FROM charactercreator_character_inventory GROUP BY character_id);"
avg_items = cursor.execute(query).fetchall()
print("AVG Items per Character: ", avg_items)

# On average, how many weapons does each character have?
query = "SELECT AVG(weapons_per_character) as avg_weapons FROM (SELECT character_id,count(distinct item_id) as weapons_per_character FROM charactercreator_character_inventory WHERE item_id > 137 GROUP BY character_id);"
avg_weapons = cursor.execute(query).fetchall()
print("AVG Weapons per Character: ", avg_weapons)