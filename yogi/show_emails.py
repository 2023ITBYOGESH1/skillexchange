import sqlite3

conn = sqlite3.connect('instance/skillswap.db')
c = conn.cursor()

c.execute("SELECT id, username, email FROM users ORDER BY id")
users = c.fetchall()

print("=" * 70)
print("ALL USERS - USERNAME & GMAIL ADDRESS")
print("=" * 70)
print(f"\n{'ID':<5} {'Username':<20} {'Gmail Address':<35}")
print("-" * 70)

for user in users:
    print(f"{user[0]:<5} {user[1]:<20} {user[2]:<35}")

print("\n" + "=" * 70)
print(f"Total Users: {len(users)}")
print("=" * 70)

conn.close()

