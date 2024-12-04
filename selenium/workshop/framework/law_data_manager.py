from datetime import datetime, timedelta
import random
import pymysql

class LawDataManager:
    def __init__(self, db_host, db_user, db_password, db_name):
        self.db_host = db_host
        self.db_user = db_user
        self.db_password = db_password
        self.db_name = db_name
        self.laws_data = []

    def connect_to_db(self):
        return pymysql.connect(
            host=self.db_host,
            user=self.db_user,
            password=self.db_password,
            db=self.db_name
        )

    def drop_and_create_db(self):
        conn = pymysql.connect(
            host=self.db_host,
            user=self.db_user,
            password=self.db_password
        )
        cur = conn.cursor()

        cur.execute(f"DROP DATABASE IF EXISTS {self.db_name}")
        cur.execute(f"CREATE DATABASE {self.db_name}")
        conn.commit()
        conn.close()

    def insert_laws(self):
        conn = self.connect_to_db()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS laws (
                id INT AUTO_INCREMENT PRIMARY KEY,
                chapter VARCHAR(255),
                article_number VARCHAR(255),
                article_link VARCHAR(255),
                content TEXT
            )
        """)

        for law in self.laws_data:
            sql = """
                INSERT INTO laws (chapter, article_number, article_link, content)
                VALUES (%s, %s, %s, %s)
            """
            cur.execute(sql, (
                law['chapter'],
                law['article_number'],
                law['article_link'],
                law['content']
            ))

        conn.commit()
        conn.close()

    def show_laws_data(self):
        conn = self.connect_to_db()
        cur = conn.cursor()

        cur.execute("SELECT * FROM laws LIMIT 5")
        results = cur.fetchall()

        for row in results:
            print(f"ID: {row[0]}")
            print(f"Chapter: {row[1]}")
            print(f"Article Number: {row[2]}")
            print(f"Article Link: {row[3]}")
            print(f"Content: {row[4]}")
            print("---")

        conn.close()
