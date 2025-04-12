# reset_usage_counts.py
import sqlite3
from config import Config
import os

DB_PATH = os.path.join(os.getcwd(), 'result_portal.db')

def reset_usage_counts():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("UPDATE access_codes SET usage_count = 0")
        cursor.execute("UPDATE access_codes SET assigned_to = null")
        conn.commit()
        conn.close()
        print("✅ All access code usage counts have been reset to 0.")
        print("✅ All access code assigned_to have been reset to null.")
    except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    reset_usage_counts()
