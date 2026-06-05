"""
test_db.py  –  Run this file standalone to verify your MySQL connection
and inspect the students table before launching app.py
"""
import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "port": 3307,
    "user": "root",
    "password": "Vishumaanu#0508",   # ← change this
    "database": "student_placement_db"
}

def test_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print("✅  Connected to MySQL successfully!")
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT COUNT(*) AS total FROM students")
        row = cur.fetchone()
        print(f"📊  Total students in table: {row['total']}")
        cur.execute("SELECT * FROM students LIMIT 5")
        rows = cur.fetchall()
        print("\n🔍  First 5 rows preview:")
        for r in rows:
            print("   ", r)
        cur.close()
        conn.close()
    except mysql.connector.Error as e:
        print(f"❌  Connection failed: {e}")

if __name__ == "__main__":
    test_connection()
