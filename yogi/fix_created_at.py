import sqlite3
from datetime import datetime

conn = sqlite3.connect('instance/skillswap.db')
c = conn.cursor()

# Find skills with NULL created_at
c.execute("SELECT id, title FROM skills WHERE created_at IS NULL")
null_skills = c.fetchall()

print(f"Found {len(null_skills)} skills with NULL created_at")

now = datetime.now().isoformat()

# Update them with current timestamp
for skill_id, title in null_skills:
    c.execute("UPDATE skills SET created_at = ? WHERE id = ?", (now, skill_id))
    print(f"  Fixed: {title}")

conn.commit()

# Verify no more NULLs
c.execute("SELECT COUNT(*) FROM skills WHERE created_at IS NULL")
remaining = c.fetchone()[0]
print(f"\nRemaining NULL created_at: {remaining}")

conn.close()
print("\nFixed!")

