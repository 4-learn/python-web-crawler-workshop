import pymysql

db = pymysql.connect(host="localhost",
                     user="root",
                     password="ntC1234#31#",
                     database="ntc3")

cursor = db.cursor()

# cursor.execute("DROP DATABASE ntc")
# cursor.execute("SHOW DATABASES")
# cursor.execute("CREATE DATABASE ntc")
# cursor.execute("SHOW DATABASES")

# cursor.execute("DROP TABLE sites")
cursor.execute("CREATE TABLE sites (name VARCHAR(255), url VARCHAR(255))")
cursor.execute("SHOW TABLES")

for x in cursor:
  print(x)
