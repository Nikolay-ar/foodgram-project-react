import csv
import sqlite3

connection = sqlite3.connect('db.sqlite3')
cursor = connection.execute('select * from recipes_ingredient')

with open('ingredients.csv', 'r', encoding="utf8") as fin:
    dr = csv.DictReader(fin)
    headers = dr.fieldnames
    to_db = [(i['name'], i['measurement_unit']) for i in dr]
print(to_db)
cursor.executemany(
    "INSERT INTO recipes_ingredient (id, name, measurement_unit) "
    "VALUES (NULL, ?, ?);", to_db)

connection.commit()
connection.close()
