import pymysql
 
db = pymysql.connect(host="localhost",
                     user="root",
                     password="ntC1234#31#")
 
cursor = db.cursor()
cursor.execute("SELECT VERSION()")
data = cursor.fetchone()
 
print ("Database version : " + str(data))
 
db.close()
