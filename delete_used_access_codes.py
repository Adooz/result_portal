# delete_used_access_codes.py
import sqlite3
import os

DB_PATH = os.path.join(os.getcwd(), 'result_portal.db')

def delete_used_codes():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Delete codes where usage_count > 0 or assigned_to is not NULL
        cursor.execute("""
            DELETE FROM access_codes
            WHERE usage_count > 0 OR assigned_to IS NOT NULL
        """)

        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()

        print(f"✅ Deleted {deleted_count} used access code(s).")
    except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    delete_used_codes()
