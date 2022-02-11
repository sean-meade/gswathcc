import requests
from datetime import datetime
import sqlite3

# creating file path
dbfile = 'database/weatherData.db'
# Create a SQL connection to our SQLite database
con = sqlite3.connect(dbfile)

# creating cursor
cur = con.cursor()

# reading all table names
table_list = [a for a in cur.execute("SELECT * FROM weatherentry")]
# here is you table list
print(table_list)

# Be sure to close the connection
con.close()