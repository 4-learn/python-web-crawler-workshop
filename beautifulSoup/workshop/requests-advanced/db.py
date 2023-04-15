import pymysql

# 連接資料庫
def create_db():
  db = pymysql.connect(host="localhost",
    user="root",
    password="ntC1234#31#")

  cursor = db.cursor()
  cursor.execute("SHOW DATABASES LIKE 'ettoday'")
  result = cursor.fetchone()

  if result is not None:
      cursor.execute("DROP DATABASE ettoday")

  db = pymysql.connect(host="localhost",
    user="root",
    password="ntC1234#31#")

  # cursor = db.cursor()
  cursor.execute("SHOW DATABASES LIKE 'ettoday'")
  result = cursor.fetchone()

  if result is None:
    cursor.execute("CREATE DATABASE ettoday")
    cursor.execute("SHOW DATABASES")

def create_table():
    db = pymysql.connect(host="localhost",
    user="root",
    password="ntC1234#31#",
    database="ettoday")

    cursor = db.cursor()
    ## cursor.execute("DROP TABLE sites")
    cursor.execute("CREATE TABLE news (title VARCHAR(255), content VARCHAR(255))")
    cursor.execute("SHOW TABLES")

def insert_data(title, content):
    db = pymysql.connect(host="localhost",
    user="root",
    password="ntC1234#31#",
    database="ettoday")

    cursor = db.cursor()
    sql = "INSERT INTO news (title, content) VALUES (%s, %s)"
    val = (title, content[:254])
    cursor.execute(sql, val)
    db.commit()

def show_data():
  db = pymysql.connect(host="localhost",
    user="root",
    password="ntC1234#31#",
    database="ettoday")

  cursor = db.cursor()
  cursor.execute("SELECT * FROM news")
  result = cursor.fetchall()

  for x in result:
    print(x)

