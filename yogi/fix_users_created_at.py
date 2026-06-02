import sqlite3
from datetime import datetime
# Direct SQLite approach (matches existing fix scripts) - no app import needed
conn = sqlite3.connect('instance/skillswap.db')
c = conn.cursor()

# Find users with NULL created_at
c.execute("SELECT id, username FROM users WHERE created_at IS NULL")
null_users = c.fetchall()

print(f"Found {len(null_users)} users with NULL created_at")

if null_users:
    now = datetime.utcnow()
    
    for user_id, username in null_users:
        c.execute("UPDATE users SET created_at = ? WHERE id = ?", (now, user_id))
        print(f"  Fixed: {username} (ID: {user_id})")
    
    conn.commit()
    print("\nUsers created_at fixed!")
else:
    print("No users with NULL created_at found.")

# Verify
c.execute("SELECT COUNT(*) FROM users WHERE created_at IS NULL")
remaining = c.fetchone()[0]
print(f"Remaining NULL created_at in users: {remaining}")

conn.close()
print("Done!")

