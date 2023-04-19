import pymysql

db = pymysql.connect(host="localhost",
                     user="root",
                     password="ntC1234#31#",
                     database="ntc3")

cursor = db.cursor()

# 創建資料庫 
## cursor.execute("DROP DATABASE ntc")
# cursor.execute("SHOW DATABASES")
# cursor.execute("CREATE DATABASE ntc")
# cursor.execute("SHOW DATABASES")

# 創建 table
## cursor.execute("DROP TABLE sites")
# cursor.execute("CREATE TABLE sites (name VARCHAR(255), url VARCHAR(255))")
# cursor.execute("SHOW TABLES")

# 插入資料 (column)
# sql = "INSERT INTO sites (name, url) VALUES (%s, %s)"
# val = ("test", "https://www.google.com")
# cursor.execute(sql, val)
# db.commit()

cursor.execute("SELECT * FROM sites")

result = cursor.fetchall()

for x in result:
  print(x)
