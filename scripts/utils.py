import sqlite3
import pandas as pd

conn = sqlite3.connect("data/database.sqlite")
matches = pd.read_sql_query("SELECT * FROM Match WHERE division = 'E1'", conn)  # Championship