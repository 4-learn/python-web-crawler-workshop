import pymysql

class DatabaseManager:
    def __init__(self, host="localhost", user="root", password="ntC1234#31#"):
        self.db = pymysql.connect(host=host, user=user, password=password)
        self.cursor = self.db.cursor()
    
    def database_exists(self, dbname):
        self.cursor.execute(f"SHOW DATABASES LIKE '{dbname}'")
        result = self.cursor.fetchone()
        return result is not None

    def create_database_and_table(self, dbname, tablename):
        if self.database_exists(dbname):
            self.cursor.execute(f"DROP DATABASE {dbname}")
        self.cursor.execute(f"CREATE DATABASE {dbname}")
        self.cursor.execute(f"USE {dbname}")
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {tablename} (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                value INT
            )
        """)
        self.db.commit()

    def insert_data(self, tablename, name, value):
        sql = f"INSERT INTO {tablename} (name, value) VALUES (%s, %s)"
        self.cursor.execute(sql, (name, value))
        self.db.commit()

    def get_passing_scores(self, tablename, passing_score=60):
        sql = f"SELECT * FROM {tablename} WHERE value >= %s"
        self.cursor.execute(sql, (passing_score,))
        results = self.cursor.fetchall()
        return results

    def close_connection(self):
        self.cursor.close()
        self.db.close()

# 初始化資料庫管理器並執行 CRUD 操作
manager = DatabaseManager()
manager.create_database_and_table("NTC", "score")

# 插入成績數據
scores = [40, 60, 70, 90]
for i, score in enumerate(scores, start=1):
    manager.insert_data("score", f"student_{i}", score)

# 查詢並顯示及格成績
passing_scores = manager.get_passing_scores("score", passing_score=60)
for record in passing_scores:
    print(record)

# 關閉資料庫連接
manager.close_connection()
