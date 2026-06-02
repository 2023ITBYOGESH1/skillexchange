import sqlite3
import random

conn = sqlite3.connect('instance/skillswap.db')
c = conn.cursor()

# Get new user IDs (excluding old users 1-7)
c.execute("SELECT id, username FROM users WHERE id NOT IN (1,2,3,4,5,6,7)")
new_users = c.fetchall()
print("New users:", new_users)

# Get some skills to reassign
c.execute("SELECT id, title FROM skills WHERE user_id IN (1,2,3,4,5,6,7) LIMIT 30")
skills = c.fetchall()

# Reassign some skills to new users
updated = 0
for skill_id, title in skills[:20]:  # Reassign 20 skills
    random_user = random.choice(new_users)
    c.execute("UPDATE skills SET user_id = ? WHERE id = ?", (random_user[0], skill_id))
    print(f"  {title} -> {random_user[1]}")
    updated += 1

conn.commit()

# Show results
print(f"\n{updated} skills reassigned to new users")

# Show all users with skill count
c.execute('''SELECT u.username, COUNT(s.id) as skill_count 
             FROM users u LEFT JOIN skills s ON u.id = s.user_id 
             GROUP BY u.id ORDER BY skill_count DESC''')
print("\nUsers with skills:")
for r in c.fetchall():
    print(f"  {r[0]}: {r[1]} skills")

conn.close()
