"""Migration script to add signature columns to the database"""
import sqlite3
import os

def migrate():
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'skillswap.db')
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if column exists in users table
    cursor.execute("PRAGMA table_info(users)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'signature_image' not in columns:
        print("Adding signature_image column to users table...")
        cursor.execute("ALTER TABLE users ADD COLUMN signature_image VARCHAR(255)")
        print("✓ Added signature_image column to users table")
    else:
        print("signature_image column already exists in users table")
    
    # Check if column exists in certificates table
    cursor.execute("PRAGMA table_info(certificates)")
    columns = [col[1] for col in cursor.fetchall()]
    
    if 'instructor_signature' not in columns:
        print("Adding instructor_signature column to certificates table...")
        cursor.execute("ALTER TABLE certificates ADD COLUMN instructor_signature VARCHAR(255)")
        print("✓ Added instructor_signature column to certificates table")
    else:
        print("instructor_signature column already exists in certificates table")
    
    conn.commit()
    conn.close()
    print("\nMigration completed successfully!")

if __name__ == "__main__":
    migrate()

