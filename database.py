import sqlite3

class Database:
    def __init__(self, db_name="dht11.db"):
        self.name = ""
        self.db_name = db_name
        print(f"Database connected: {self.db_name}")

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def createTable(self):
        con = self.get_connection()
        cur = con.cursor()
        cur.execute("""
                        CREATE TABLE IF NOT EXISTS readings (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            temperature REAL,
                            humidity REAL,
                            timestamp DATETIME DEFAULT (datetime('now', '+8 hours'))
                        )
                    """)
        con.commit()
        con.close()


    def insert_data(self, temperature, humidity):
        con = self.get_connection()
        cur = con.cursor()
        cur.execute(
            "INSERT INTO readings (temperature, humidity) VALUES (?, ?)", (temperature, humidity)
        )
        con.commit()
        con.close()

    def fetch_latest(self):
        con = self.get_connection()
        cur = con.cursor()
        cur.execute("""
                        SELECT id, temperature, humidity, timestamp
                        FROM readings
                        ORDER BY id DESC
                        LIMIT 1
                    """)
        row = cur.fetchone()
        con.close()
        return row
