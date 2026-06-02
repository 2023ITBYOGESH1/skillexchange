import sqlite3

conn = sqlite3.connect('instance/skillswap.db')
c = conn.cursor()

c.execute("SELECT id, username, email FROM users ORDER BY id")
users = c.fetchall()

print("=" * 60)
print("ALL USERS - USERNAME & PASSWORD")
print("=" * 60)
print(f"\n{'ID':<5} {'Username':<20} {'Password':<15}")
print("-" * 40)

for user in users:
    print(f"{user[0]:<5} {user[1]:<20} {'password123':<15}")

print("\n" + "=" * 60)
print(f"Total Users: {len(users)}")
print("Password for ALL users: password123")
print("=" * 60)

conn.close()

