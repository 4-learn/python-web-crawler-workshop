import pymysql

db = pymysql.connect(host="localhost",
                     user="root",
                     password="ntC1234#31#")

cursor = db.cursor()

# cursor.execute("DROP DATABASE ntc")
cursor.execute("SHOW DATABASES")
cursor.execute("CREATE DATABASE ntc3")
cursor.execute("SHOW DATABASES")

for x in cursor:
  print("---")
  print(x)
