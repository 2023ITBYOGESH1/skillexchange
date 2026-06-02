import sqlite3

conn = sqlite3.connect('instance/skillswap.db')
c = conn.cursor()

# Get all users
c.execute("SELECT id, username FROM users WHERE email LIKE '%@demo.com'")
demo_users = c.fetchall()

print(f"Found {len(demo_users)} demo.com emails to convert to Gmail")

for user_id, username in demo_users:
    gmail = f"{username}@gmail.com"
    c.execute("UPDATE users SET email = ? WHERE id = ?", (gmail, user_id))
    print(f"  {username} -> {gmail}")

conn.commit()

# Show all emails
print("\n" + "=" * 70)
print("ALL USERS - GMAIL ADDRESSES")
print("=" * 70)

c.execute("SELECT id, username, email FROM users ORDER BY id")
for user in c.fetchall():
    print(f"{user[0]:<5} {user[1]:<20} {user[2]}")

print("=" * 70)
print("All emails now use @gmail.com!")
conn.close()


