import pymysql

# 1. 假設你爬下一個班級的成績了
list_scores = [40, 60, 70, 90]

# 2. 檢查資料庫 NTC 是否存在
db = pymysql.connect(host="localhost",
                 user="root",
                 password="ntC1234#31#")

cursor = db.cursor()
cursor.execute("SHOW DATABASES LIKE 'ntc'")
result = cursor.fetchone()

if result is None:
    print("create database ntc")
    cursor.execute("CREATE DATABASE ntc")
    cursor.execute("SHOW DATABASES")
else:
    print("drop and connect")
    cursor.execute("DROP DATABASE ntc")
    cursor.execute("CREATE DATABASE ntc")
    cursor.execute("SHOW DATABASES")

db = pymysql.connect(host="localhost",
    user="root",
    password="ntC1234#31#",
    database="ntc")

cursor = db.cursor()

# 3. 替這個 NTC 新增一個表單
## cursor.execute("DROP TABLE sites")
cursor.execute("CREATE TABLE score (name VARCHAR(255), value INT)")
cursor.execute("SHOW TABLES")

# 4. 將這幾筆資料存入 Table 內
index = 0
for input_value in list_scores:
    index = index + 1
    sql = "INSERT INTO score (name, value) VALUES (%s, %s)"
    val = (str(index), str(input_value))
    cursor.execute(sql, val)
    db.commit()

# 5. 移除不及格的學生，他下學期不用來了
sql = "DELETE FROM score WHERE value < 60"
cursor.execute(sql)
db.commit()

# 6. Show 出移除被當學生後的所有的欄位
cursor.execute("SELECT * FROM score")
result = cursor.fetchall()

for x in result:
  print(x)

db.close()
