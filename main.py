import sqlite3

con = sqlite3.connect("coffee.sqlite")
cur = con.cursor()
result = cur.execute(f"SELECT * FROM Coffee ").fetchall()
print(result)
con.close()
